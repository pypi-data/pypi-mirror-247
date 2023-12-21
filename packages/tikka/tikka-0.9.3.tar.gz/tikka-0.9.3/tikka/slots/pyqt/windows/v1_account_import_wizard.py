# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
import sys
from collections import OrderedDict
from typing import Optional

from duniterpy.key import SigningKey
from PyQt5.QtCore import QMutex, QSize, QTimer
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QWizard
from substrateinterface import Keypair, KeypairType

from tikka.domains.application import Application
from tikka.domains.entities.constants import (
    AMOUNT_UNIT_KEY,
    DATA_PATH,
    DERIVATION_PATH_MEMBER,
    WALLETS_PASSWORD_LENGTH,
)
from tikka.interfaces.adapters.repository.accounts import AccountsRepositoryInterface
from tikka.libs.secret import generate_alphabetic, sanitize_mnemonic_string
from tikka.slots.pyqt.entities.constants import (
    ADDRESS_MONOSPACE_FONT_NAME,
    DEBOUNCE_TIME,
    ICON_LOADER,
    SELECTED_UNIT_PREFERENCES_KEY,
)
from tikka.slots.pyqt.entities.worker import AsyncQWorker
from tikka.slots.pyqt.resources.gui.windows.v1_account_import_wizard_rc import (
    Ui_importAccountV1Wizard,
)


class V1AccountImportWizardWindow(QWizard, Ui_importAccountV1Wizard):
    """
    V1AccountImportWizardWindow class
    """

    def __init__(
        self, application: Application, mutex: QMutex, parent: Optional[QWidget] = None
    ):
        """
        Init import V1 account wizard window

        :param application: Application instance
        :param mutex: QMutex instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.mutex = mutex

        unit_preference = self.application.preferences_repository.get(
            SELECTED_UNIT_PREFERENCES_KEY
        )
        if unit_preference is not None:
            self.amount = self.application.amounts.get_amount(unit_preference)
        else:
            self.amount = self.application.amounts.get_amount(AMOUNT_UNIT_KEY)

        # source account
        self.source_account = None
        self.source_v1_address = None
        self.source_keypair = None
        self.source_wallet_password = generate_alphabetic(WALLETS_PASSWORD_LENGTH)

        # destination account
        self.destination_root_account = None
        self.destination_mnemonic = None
        self.destination_account = None
        self.destination_keypair = None

        self.display_identity_status = {
            "Created": self._("Created"),
            "Validated": self._("Validated"),
            "ConfirmedByOwner": self._("Confirmed"),
            "Unknown": self._("Unknown"),
        }

        # set monospace font to address fields
        self.monospace_font = QFont(ADDRESS_MONOSPACE_FONT_NAME)
        self.monospace_font.setStyleHint(QFont.Monospace)
        self.sourceAddressValueImportLabel.setFont(self.monospace_font)
        self.destinationAddressValueImportLabel.setFont(self.monospace_font)

        # animated loading icon
        self.loader_movie = QMovie(ICON_LOADER)
        self.loader_movie.setScaledSize(QSize(16, 16))
        self.loader_movie.start()

        # debounce timers
        self.source_debounce_timer = QTimer()
        self.destination_debounce_timer = QTimer()

        ##############################
        # ASYNC METHODS
        ##############################
        # Create a QWorker object
        self.fetch_source_from_network_async_qworker = AsyncQWorker(
            self.fetch_source_from_network, self.mutex
        )
        self.fetch_destination_from_network_async_qworker = AsyncQWorker(
            self.fetch_destination_from_network, self.mutex
        )
        self.import_source_into_destination_on_network_async_qworker = AsyncQWorker(
            self.import_source_into_destination_on_network, self.mutex
        )
        self.wizard_page2_init()

    def wizard_page2_init(self):
        """
        Initialize page 2 form

        :return:
        """
        # fonts
        self.sourceV1AddressValueLabel.setFont(self.monospace_font)
        self.sourceAddressValueLabel.setFont(self.monospace_font)

        # page next button status handling
        self.wizardPage2.isComplete = self.wizard_page2_is_complete

        # events
        self.sourceSecretIDLineEdit.textChanged.connect(
            self._on_source_secret_id_line_edit_changed
        )
        self.sourcePasswordIDLineEdit.textChanged.connect(
            self._on_source_password_id_line_edit_changed
        )
        self.sourceShowButton.clicked.connect(self.on_source_show_button_clicked)

        # debounce timer
        self.source_debounce_timer.timeout.connect(self._source_generate_address)

        ##############################
        # ASYNC METHODS
        ##############################
        self.fetch_source_from_network_async_qworker.finished.connect(
            self._on_finished_fetch_source_from_network
        )

    def wizard_page2_is_complete(self) -> bool:
        """
        Function to overload V1AccountImportWizardWindow->Page2->IsComplete() method

        :return:
        """
        result = False

        if (
            self.source_account is not None
            and self.source_keypair is not None
            and self.source_account.balance is not None
        ):
            result = True

        return result

    def _on_source_secret_id_line_edit_changed(self):
        """
        Triggered when text is changed in the secret ID field

        :return:
        """
        if self.source_debounce_timer.isActive():
            self.source_debounce_timer.stop()
        self.source_debounce_timer.start(DEBOUNCE_TIME)

    def _on_source_password_id_line_edit_changed(self):
        """
        Triggered when text is changed in the password ID field

        :return:
        """
        if self.source_debounce_timer.isActive():
            self.source_debounce_timer.stop()
        self.source_debounce_timer.start(DEBOUNCE_TIME)

    def _source_generate_address(self):
        """
        Generate address from ID

        :return:
        """
        # stop debounce_timer to avoid infinite loop
        if self.source_debounce_timer.isActive():
            self.source_debounce_timer.stop()

        self.sourceV1AddressValueLabel.setText("")
        self.sourceAddressValueLabel.setText("")
        self.sourceErrorLabel.setText("")

        secret_id = self.sourceSecretIDLineEdit.text().strip()
        password_id = self.sourcePasswordIDLineEdit.text().strip()
        if secret_id == "" or password_id == "":
            return

        signing_key = SigningKey.from_credentials(secret_id, password_id)
        self.source_v1_address = signing_key.pubkey
        self.sourceV1AddressValueLabel.setText(self.source_v1_address)

        try:
            self.source_keypair = Keypair.create_from_seed(
                seed_hex=signing_key.seed.hex(),
                ss58_format=self.application.currencies.get_current().ss58_format,
                crypto_type=KeypairType.ED25519,
            )
        except Exception as exception:
            logging.exception(exception)
            self.sourceErrorLabel.setText(self._("Error generating account wallet!"))
            self.sourceErrorLabel.setStyleSheet("color: red;")
            return

        self.source_account = self.application.accounts.get_instance(
            self.source_keypair.ss58_address
        )
        self.sourceAddressValueLabel.setText(self.source_account.address)

        # fetch if v1 account exists on network
        self.fetch_source_from_network_async_qworker.start()

    def on_source_show_button_clicked(self):
        """
        Triggered when user click on source show button

        :return:
        """
        if self.sourceSecretIDLineEdit.echoMode() == QLineEdit.Password:
            self.sourceSecretIDLineEdit.setEchoMode(QLineEdit.Normal)
            self.sourcePasswordIDLineEdit.setEchoMode(QLineEdit.Normal)
            self.sourceShowButton.setText(self._("Hide"))
        else:
            self.sourceSecretIDLineEdit.setEchoMode(QLineEdit.Password)
            self.sourcePasswordIDLineEdit.setEchoMode(QLineEdit.Password)
            self.sourceShowButton.setText(self._("Show"))

    def fetch_source_from_network(self):
        """
        Fetch last account data from the network

        :return:
        """
        self.sourceErrorLabel.setMovie(self.loader_movie)

        try:
            balance = self.application.accounts.fetch_balance_from_network(
                self.source_account.address
            )
        except Exception:
            # keep balance from cache DB if network failure
            balance = self.source_account.balance

        if balance is None:
            return

        self.source_account.balance = balance
        self.source_account.identity_index = (
            self.application.identities.fetch_index_from_network(
                self.source_account.address
            )
        )
        if self.source_account.identity_index is not None:
            self.application.identities.fetch_from_network(
                self.source_account.identity_index
            )

    def _on_finished_fetch_source_from_network(self):
        """
        Triggered when async request fetch_from_network is finished

        :return:
        """
        self.sourceErrorLabel.setMovie(None)

        self.application.accounts.update(self.source_account)
        if self.source_account is not None:
            if self.source_account.balance is None:
                self.sourceErrorLabel.setText(self._("This account does not exists"))
                self.sourceErrorLabel.setStyleSheet("color: red;")
            else:
                self.sourceBalanceValueLabel.setText(
                    self.locale().toCurrencyString(
                        self.amount.value(self.source_account.balance),
                        self.amount.symbol(),
                    )
                )

                if self.source_account.identity_index is not None:
                    identity = self.application.identities.get(
                        self.source_account.identity_index
                    )
                    if identity.status not in self.display_identity_status:
                        self.sourceIdentityValueLabel.setText(
                            self.display_identity_status["Unknown"]
                        )
                    else:
                        self.sourceIdentityValueLabel.setText(
                            self.display_identity_status[identity.status]
                        )
                else:
                    self.sourceIdentityValueLabel.setText(self._("None"))

                self.sourceErrorLabel.setText(self._("Account is valid"))
                self.sourceErrorLabel.setStyleSheet("color: green;")
        self.wizardPage2.completeChanged.emit()

        if self.wizardPage2.isComplete():
            self.wizard_page3_init()

    def wizard_page3_init(self):
        """
        Initialize page 3 form

        :return:
        """
        # Mnemonic language selector translated
        mnemonic_language_selector = OrderedDict(
            [
                ("en", self._("English")),
                ("fr", self._("French")),
                ("zh-hans", self._("Chinese simplified")),
                ("zh-hant", self._("Chinese traditional")),
                ("it", self._("Italian")),
                ("ja", self._("Japanese")),
                ("ko", self._("Korean")),
                ("es", self._("Spanish")),
            ]
        )
        for language_code, language_name in mnemonic_language_selector.items():
            self.destinationMnemonicLanguageComboBox.addItem(
                language_name, userData=language_code
            )
        self.destinationMnemonicLanguageComboBox.setCurrentIndex(
            self.destinationMnemonicLanguageComboBox.findData(
                self.application.config.get("language")[:2]
            )
        )

        # fonts
        self.destinationRootNameOrAddressComboBox.setFont(self.monospace_font)
        self.destinationRootAddressValueLabel.setFont(self.monospace_font)
        self.destinationAddressValueLabel.setFont(self.monospace_font)

        # page next button status handling
        self.wizardPage3.isComplete = self.wizard_page3_is_complete

        # init root accounts combo box
        # only V2 root accounts...
        for account in self.application.accounts.get_list(
            filters={
                AccountsRepositoryInterface.COLUMN_ROOT: True,
                AccountsRepositoryInterface.COLUMN_CRYPTO_TYPE: int(
                    KeypairType.SR25519
                ),
            }
        ):
            # only accounts with password (user owns it)
            if self.application.passwords.exists(account.address):
                self.destinationRootNameOrAddressComboBox.addItem(
                    account.name if account.name is not None else account.address,
                    userData=account.address,
                )

        # events
        self.destinationRootNameOrAddressComboBox.currentIndexChanged.connect(
            self._generate_destination_address
        )
        self.destinationMnemonicLineEdit.textChanged.connect(
            self._on_destination_mnemonic_line_edit_changed
        )
        self.destinationShowButton.clicked.connect(
            self.on_destination_show_button_clicked
        )
        self.destinationMnemonicLanguageComboBox.currentIndexChanged.connect(
            self._on_destination_mnemonic_line_edit_changed
        )
        # debounce timer
        self.destination_debounce_timer.timeout.connect(
            self._generate_destination_address
        )

        ##############################
        # ASYNC METHODS
        ##############################
        self.fetch_destination_from_network_async_qworker.finished.connect(
            self._on_finished_fetch_destination_from_network
        )

        self._generate_destination_address()

    def wizard_page3_is_complete(self) -> bool:
        """
        Function to overload V1AccountImportWizardWindow->Page3->IsComplete() method

        :return:
        """
        result = False

        if (
            self.destination_account is not None
            and self.destination_keypair is not None
            and (
                self.source_account.identity_index is None
                or (
                    self.source_account.identity_index is not None
                    and self.destination_account.identity_index is None
                )
            )
        ):
            result = True

        return result

    def _on_destination_mnemonic_line_edit_changed(self):
        """
        Triggered when text is changed in the mnemonic field

        :return:
        """
        if self.destination_debounce_timer.isActive():
            self.destination_debounce_timer.stop()
        self.destination_debounce_timer.start(DEBOUNCE_TIME)

    def on_destination_show_button_clicked(self):
        """
        Triggered when user click on destination show button

        :return:
        """
        if self.destinationMnemonicLineEdit.echoMode() == QLineEdit.Password:
            self.destinationMnemonicLineEdit.setEchoMode(QLineEdit.Normal)
            self.storedPasswordLineEdit.setEchoMode(QLineEdit.Normal)
            self.destinationShowButton.setText(self._("Hide"))
        else:
            self.destinationMnemonicLineEdit.setEchoMode(QLineEdit.Password)
            self.storedPasswordLineEdit.setEchoMode(QLineEdit.Password)
            self.destinationShowButton.setText(self._("Show"))

    def _generate_destination_address(self):
        """
        Generate destination address

        :return:
        """
        # stop debounce_timer to avoid infinite loop
        if self.destination_debounce_timer.isActive():
            self.destination_debounce_timer.stop()

        self.destination_root_account = self.application.accounts.get_by_address(
            self.destinationRootNameOrAddressComboBox.currentData()
        )

        # select derivation: //0 if source account is member, first even number if not
        destination_derivation = None
        if (
            self.source_account is not None
            and self.source_account.identity_index is not None
        ):
            destination_derivation = DERIVATION_PATH_MEMBER

        if self.destination_root_account is not None and destination_derivation is None:
            available_derivation_list = (
                self.application.accounts.get_available_derivation_list(
                    self.destination_root_account
                )
            )
            if available_derivation_list[0] == DERIVATION_PATH_MEMBER:
                destination_derivation = available_derivation_list[1]
            else:
                destination_derivation = available_derivation_list[0]

        self.destinationDerivationValueLabel.setText(destination_derivation)

        # if account name displayed in combobox...
        if (
            self.destinationRootNameOrAddressComboBox.currentText()
            != self.destinationRootNameOrAddressComboBox.currentData()
        ):
            self.destinationRootAddressValueLabel.setText(
                self.destinationRootNameOrAddressComboBox.currentData()
            )
        else:
            self.destinationRootAddressValueLabel.setText("")

        if self.destinationMnemonicLineEdit.text().strip() == "":
            return

        self.destinationErrorLabel.setText("")
        language_code = self.destinationMnemonicLanguageComboBox.currentData()
        self.destination_mnemonic = sanitize_mnemonic_string(
            self.destinationMnemonicLineEdit.text()
        )
        suri = self.destination_mnemonic + destination_derivation
        if not Keypair.validate_mnemonic(self.destination_mnemonic, language_code):
            self.destinationErrorLabel.setText(
                self._("Mnemonic or language not valid!")
            )
            self.destinationErrorLabel.setStyleSheet("color: red;")
            return

        try:
            root_keypair = Keypair.create_from_mnemonic(
                mnemonic=self.destination_mnemonic,
                ss58_format=self.application.currencies.get_current().ss58_format,
                crypto_type=KeypairType.SR25519,
                language_code=language_code,
            )
        except Exception as exception:
            logging.exception(exception)
            self.destinationErrorLabel.setText(
                self._("Mnemonic or language not valid!")
            )
            self.destinationErrorLabel.setStyleSheet("color: red;")
            return

        # if mnemonic address is not account address...
        if root_keypair.ss58_address != self.destination_root_account.address:
            self.destinationErrorLabel.setText(
                self._("Mnemonic address is not the root account address!")
            )
            self.destinationErrorLabel.setStyleSheet("color: red;")
            return

        stored_password = self.application.passwords.get_clear_password(root_keypair)
        self.storedPasswordLineEdit.setText(stored_password)

        try:
            self.destination_keypair = Keypair.create_from_uri(
                suri=suri,
                ss58_format=self.application.currencies.get_current().ss58_format,
                crypto_type=KeypairType.SR25519,
                language_code=language_code,
            )
        except Exception as exception:
            logging.exception(exception)
            self.destinationErrorLabel.setText(
                self._("Mnemonic or language not valid!")
            )
            self.destinationErrorLabel.setStyleSheet("color: red;")
            return

        if self.destination_keypair is None:
            return

        self.destination_account = self.application.accounts.get_by_address(
            self.destination_keypair.ss58_address
        )
        if self.destination_account is None:
            self.destination_account = self.application.accounts.get_instance(
                self.destination_keypair.ss58_address,
                self.destinationNameLineEdit.text().strip(),
            )
            self.destination_account.crypto_type = KeypairType.SR25519
            self.destination_account.root = self.destination_root_account.address
            self.destination_account.path = destination_derivation
        self.destinationAddressValueLabel.setText(self.destination_account.address)

        # fetch if v2 account exists on network
        self.fetch_destination_from_network_async_qworker.start()

    def fetch_destination_from_network(self):
        """
        Fetch destination account data from the network

        :return:
        """
        self.destinationErrorLabel.setMovie(self.loader_movie)

        try:
            balance = self.application.accounts.fetch_balance_from_network(
                self.destination_account.address
            )
        except Exception:
            # keep balance from cache DB if network failure
            balance = self.destination_account.balance

        if balance is None:
            return

        self.destination_account.balance = balance
        self.destination_account.identity_index = (
            self.application.identities.fetch_index_from_network(
                self.destination_account.address
            )
        )
        if self.destination_account.identity_index is not None:
            self.application.identities.fetch_from_network(
                self.destination_account.identity_index
            )

    def _on_finished_fetch_destination_from_network(self):
        """
        Triggered when async request fetch_from_network is finished

        :return:
        """
        self.destinationErrorLabel.setMovie(None)

        if self.destination_account.balance is not None:
            self.destinationBalanceValueLabel.setText(
                self.locale().toCurrencyString(
                    self.amount.value(self.destination_account.balance),
                    self.amount.symbol(),
                )
            )

            if self.destination_account.identity_index is not None:
                self.destinationErrorLabel.setText(
                    self._("Account has already an identity!")
                )
                self.destinationErrorLabel.setStyleSheet("color: red;")
            else:
                self.destinationErrorLabel.setText(self._("Account is valid"))
                self.destinationErrorLabel.setStyleSheet("color: green;")

        self.wizardPage3.completeChanged.emit()

        if self.wizardPage3.isComplete():
            self.wizard_page4_init()

    def wizard_page4_init(self):
        """
        Initialize page 4 form

        :return:
        """
        # fonts
        self.sourceAddressValueImportLabel.setFont(self.monospace_font)
        self.destinationAddressValueImportLabel.setFont(self.monospace_font)

        self.sourceAddressValueImportLabel.setText(self.source_v1_address)
        if self.source_account is not None:
            if self.source_account.balance is not None:
                self.sourceBalanceValueImportLabel.setText(
                    self.locale().toCurrencyString(
                        self.amount.value(self.source_account.balance),
                        self.amount.symbol(),
                    )
                )
        if self.source_account.identity_index is not None:
            identity = self.application.identities.get(
                self.source_account.identity_index
            )
            if identity.status not in self.display_identity_status:
                self.sourceIdentityValueImportLabel.setText(
                    self.display_identity_status["Unknown"]
                )
            else:
                self.sourceIdentityValueImportLabel.setText(
                    self.display_identity_status[identity.status]
                )
        else:
            self.sourceIdentityValueImportLabel.setText(self._("None"))

        self.destinationAddressValueImportLabel.setText(
            self.destination_account.address
        )
        if self.destination_account.balance is not None:
            self.destinationBalanceValueImportLabel.setText(
                self.locale().toCurrencyString(
                    self.amount.value(self.destination_account.balance),
                    self.amount.symbol(),
                )
            )
        self.destinationIdentityValueImportLabel.setText(self._("None"))

        # page next button status handling
        self.wizardPage4.isComplete = self.wizard_page4_is_complete

        # events
        self.importButton.clicked.connect(self.on_import_button_clicked)

        ##############################
        # ASYNC METHODS
        ##############################
        self.import_source_into_destination_on_network_async_qworker.finished.connect(
            self._on_finished_import_source_into_destination_on_network
        )

    def wizard_page4_is_complete(self) -> bool:
        """
        Function to overload V1AccountImportWizardWindow->Page4->IsComplete() method

        :return:
        """
        result = False

        if (
            self.source_account is not None
            and (
                self.source_account.balance == 0 or self.source_account.balance is None
            )
            and self.source_account.identity_index is None
        ):
            result = True

        return result

    def on_import_button_clicked(self):
        """
        Triggered when user click on import button

        :return:
        """
        self.importButton.setDisabled(True)
        self.importErrorLabel.setMovie(self.loader_movie)

        self.import_source_into_destination_on_network_async_qworker.start()

    def import_source_into_destination_on_network(self):
        """
        Send changeOwnerKey for identity if any and tranfer money from V1 source account to V2 destination account

        :return:
        """
        if self.source_keypair is None:
            return

        if self.source_account.identity_index is not None:
            result = self.application.identities.change_owner_key(
                self.source_keypair, self.destination_keypair
            )
            if not result:
                # do not transfer all the money if identity transfer failed,
                # because identity transfer requires fees from sender account
                return

        if self.source_account.balance is not None and self.source_account.balance > 0:
            self.application.transfers.send_all(
                self.source_keypair, self.destination_account.address, False
            )

        try:
            balance = self.application.accounts.fetch_balance_from_network(
                self.source_account.address
            )
        except Exception:
            # keep balance from cache DB if network failure
            balance = self.source_account.balance

        self.source_account.balance = balance

        self.source_account.identity_index = (
            self.application.identities.fetch_index_from_network(
                self.source_account.address
            )
        )

        try:
            balance = self.application.accounts.fetch_balance_from_network(
                self.destination_account.address
            )
        except Exception:
            # keep balance from cache DB if network failure
            balance = self.destination_account.balance

        self.destination_account.balance = balance

        self.destination_account.identity_index = (
            self.application.identities.fetch_index_from_network(
                self.destination_account.address
            )
        )

    def _on_finished_import_source_into_destination_on_network(self):
        """
        Triggered when async request import_source_into_destination_on_network is finished

        :return:
        """
        self.importErrorLabel.setMovie(None)

        if self.source_account is not None:
            if self.source_account.balance is not None:
                self.sourceBalanceValueImportLabel.setText(
                    self.locale().toCurrencyString(
                        self.amount.value(self.source_account.balance),
                        self.amount.symbol(),
                    )
                )
            else:
                # empty account deleted from blockchain
                self.sourceBalanceValueImportLabel.setText("")

        if self.source_account.identity_index is not None:
            identity = self.application.identities.get(
                self.source_account.identity_index
            )
            if identity.status not in self.display_identity_status:
                self.sourceIdentityValueImportLabel.setText(
                    self.display_identity_status["Unknown"]
                )
            else:
                self.sourceIdentityValueImportLabel.setText(
                    self.display_identity_status[identity.status]
                )
        else:
            self.sourceIdentityValueImportLabel.setText(self._("None"))

        if self.destination_account.balance is not None:
            self.destinationBalanceValueImportLabel.setText(
                self.locale().toCurrencyString(
                    self.amount.value(self.destination_account.balance),
                    self.amount.symbol(),
                )
            )
        else:
            self.destinationBalanceValueImportLabel.setText("")

        if self.destination_account.identity_index is not None:
            identity = self.application.identities.get(
                self.destination_account.identity_index
            )
            if identity.status not in self.display_identity_status:
                self.destinationIdentityValueImportLabel.setText(
                    self.display_identity_status["Unknown"]
                )
            else:
                self.destinationIdentityValueImportLabel.setText(
                    self.display_identity_status[identity.status]
                )
        else:
            self.destinationIdentityValueImportLabel.setText(self._("None"))

        self.wizardPage4.completeChanged.emit()

        if self.wizardPage4.isComplete():
            self.importButton.setDisabled(True)
            self.importErrorLabel.setStyleSheet("color: green;")
            self.importErrorLabel.setText(self._("Account imported successfully!"))
            if (
                self.application.accounts.get_by_address(
                    self.destination_account.address
                )
                is None
            ):
                self.application.accounts.add(self.destination_account)
            else:
                self.application.accounts.update(self.destination_account)
        else:
            self.importButton.setDisabled(False)
            self.importErrorLabel.setStyleSheet("color: red;")
            if (
                self.source_account.balance is not None
                and self.source_account.balance > 0
            ):
                self.importErrorLabel.setText(self._("Error importing money!"))
            elif self.destination_account.identity_index is None:
                self.importErrorLabel.setText(self._("Error importing identity!"))


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    V1AccountImportWizardWindow(application_, QMutex()).exec_()
