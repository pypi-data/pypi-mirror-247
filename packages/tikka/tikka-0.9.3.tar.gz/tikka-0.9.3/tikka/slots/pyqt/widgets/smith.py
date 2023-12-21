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
from typing import List, Optional

from PyQt5.QtCore import QLocale, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QTableWidgetItem,
    QWidget,
)

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import ConnectionsEvent, CurrencyEvent
from tikka.domains.entities.node import Node
from tikka.domains.entities.smith import SmithCertification, SmithMembership
from tikka.slots.pyqt.entities.constants import (
    ICON_LOADER,
    SMITH_SELECTED_ACCOUNT_ADDRESS,
)
from tikka.slots.pyqt.resources.gui.widgets.smith_rc import Ui_SmithWidget
from tikka.slots.pyqt.windows.account_unlock import AccountUnlockWindow


class SmithWidget(QWidget, Ui_SmithWidget):
    """
    SmithWidget class
    """

    DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST = 6000

    AUTHORITY_STATUS_NO = 0
    AUTHORITY_STATUS_INCOMING = 1
    AUTHORITY_STATUS_ONLINE = 2
    AUTHORITY_STATUS_OUTGOING = 3

    def __init__(
        self, application: Application, parent: Optional[QWidget] = None
    ) -> None:
        """
        Init SmithWidget instance

        :param application: Application instance
        :param parent: MainWindow instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.account: Optional[Account] = None
        self.membership: Optional[SmithMembership] = None
        self.pending_membership: bool = False
        self.authority_status: int = 0
        self.certs_by_receiver: Optional[List[SmithCertification]] = None
        self.current_node = self.application.nodes.get(
            self.application.nodes.get_current_url()
        )

        # animated loading icon
        self.loader_movie = QMovie(ICON_LOADER)
        self.loader_movie.start()
        self.loaderIconLabel.setMovie(self.loader_movie)
        loader_icon_size_policy = self.loaderIconLabel.sizePolicy()
        loader_icon_size_policy.setRetainSizeWhenHidden(True)
        self.loaderIconLabel.setSizePolicy(loader_icon_size_policy)
        self.loaderIconLabel.hide()

        # setup certifier table widget
        self.certifiersTableWidget.setColumnCount(3)
        self.certifiersTableWidget.setHorizontalHeaderLabels(
            [self._("Identity"), self._("Account"), self._("Expire on")]
        )

        ##############################
        # ASYNC METHODS
        ##############################
        self.fetch_membership_from_network_timer = QTimer()
        self.fetch_membership_from_network_timer.timeout.connect(
            self.fetch_membership_from_network_timer_function
        )
        self.fetch_authority_status_from_network_timer = QTimer()
        self.fetch_authority_status_from_network_timer.timeout.connect(
            self.fetch_authority_status_from_network_timer_function
        )
        self.rotate_keys_timer = QTimer()
        self.rotate_keys_timer.timeout.connect(self.rotate_keys_timer_function)
        self.publish_keys_timer = QTimer()
        self.publish_keys_timer.timeout.connect(self.publish_keys_timer_function)
        self.request_membership_timer = QTimer()
        self.request_membership_timer.timeout.connect(
            self.request_membership_timer_function
        )
        self.claim_membership_timer = QTimer()
        self.claim_membership_timer.timeout.connect(
            self.claim_membership_timer_function
        )
        self.revoke_membership_timer = QTimer()
        self.revoke_membership_timer.timeout.connect(
            self.revoke_membership_timer_function
        )
        self.go_online_timer = QTimer()
        self.go_online_timer.timeout.connect(self.go_online_timer_function)
        self.go_offline_timer = QTimer()
        self.go_offline_timer.timeout.connect(self.go_offline_timer_function)

        # events
        self.accountComboBox.activated.connect(self.on_account_combobox_index_changed)
        self.refreshSmithButton.clicked.connect(self._on_refresh_smith_button_clicked)
        self.rotateKeysButton.clicked.connect(self.rotate_keys_timer.start)
        self.publishKeysButton.clicked.connect(self.publish_keys_timer.start)
        self.requestMembershipButton.clicked.connect(
            self.request_membership_timer.start
        )
        self.revokeSmithMembershipButton.clicked.connect(
            self.revoke_membership_timer.start
        )
        self.claimMembershipButton.clicked.connect(self.claim_membership_timer.start)
        self.goOnlineButton.clicked.connect(self.go_online_timer.start)
        self.goOfflineButton.clicked.connect(self.go_offline_timer.start)

        # subscribe to application events
        self.application.event_dispatcher.add_event_listener(
            CurrencyEvent.EVENT_TYPE_CHANGED, self._on_currency_event
        )
        self.application.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_CONNECTED, self.on_connections_event
        )
        self.application.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_DISCONNECTED, self.on_connections_event
        )

        # populate form
        self.init_account_combo_box()
        if self.account is not None:
            self.fetch_membership_from_network_timer.start()
            self.fetch_authority_status_from_network_timer.start()
        else:
            self._update_ui()

    def init_account_combo_box(self) -> None:
        """
        Init combobox with validated identity accounts (with wallets)

        :return:
        """
        self.accountComboBox.clear()
        self.accountComboBox.addItem("-", userData=None)

        accounts = self.application.accounts.get_list()
        for account in accounts:
            if (
                account.identity_index is not None
                and self.application.identities.is_validated(account.identity_index)
                and self.application.wallets.exists(account.address)
            ):
                self.accountComboBox.addItem(
                    account.name if account.name is not None else account.address,
                    userData=account.address,
                )

        preference_account_address_selected = self.application.preferences.get(
            SMITH_SELECTED_ACCOUNT_ADDRESS
        )
        if preference_account_address_selected is not None:
            preference_account_selected = self.application.accounts.get_by_address(
                preference_account_address_selected
            )
            if preference_account_selected is not None:
                self.accountComboBox.setCurrentIndex(
                    accounts.index(preference_account_selected)
                )
                self.account = preference_account_selected

    def on_account_combobox_index_changed(self):
        """
        Triggered when account selection is changed

        :return:
        """
        address = self.accountComboBox.currentData()
        if address is not None:
            self.account = self.application.accounts.get_by_address(address)
        else:
            self.account = None
            self.membership = None
            self.pending_membership = False
            self.certs_by_receiver = None

        self._update_ui()

        if self.account is not None:
            self.loaderIconLabel.show()
            # Disable button
            self.refreshSmithButton.setEnabled(False)
            self.fetch_membership_from_network_timer.start()
            self.fetch_authority_status_from_network_timer.start()

    def rotate_keys_timer_function(self):
        """
        Triggered when user click on rotate keys button

        :return:
        """
        self.rotateKeysButton.setDisabled(True)
        result = self.application.authorities.rotate_keys(self.current_node)
        if result is not None:
            self.sessionKeysTextBrowser.setText(result)
            self.errorLabel.setText("")
        else:
            self.errorLabel.setText(self._("Unable to get session keys"))

        self.rotateKeysButton.setEnabled(True)
        self.rotate_keys_timer.stop()

    def request_membership_timer_function(self):
        """
        Triggered when user click on request membership button

        :return:
        """
        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.requestMembershipButton.setDisabled(True)
        result = self.application.smiths.request_membership(
            self.application.wallets.get_keypair(self.account.address),
            self.current_node.session_keys,
        )
        if not result:
            self.errorLabel.setText(self._("Unable to request membership"))

        self.requestMembershipButton.setEnabled(True)
        self.fetch_membership_from_network_timer.start(
            self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
        )

        self.request_membership_timer.stop()

    def revoke_membership_timer_function(self):
        """
        Triggered when user click on revoke membership button

        :return:
        """
        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.revokeSmithMembershipButton.setDisabled(True)
        result = self.application.smiths.revoke_membership(
            self.application.wallets.get_keypair(self.account.address),
        )
        if not result:
            self.errorLabel.setText(self._("Unable to revoke smith membership"))

        self.revokeSmithMembershipButton.setEnabled(True)
        self.fetch_membership_from_network_timer.start(
            self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
        )

        self.revoke_membership_timer.stop()

    def claim_membership_timer_function(self):
        """
        Triggered when user click on claim membership button

        :return:
        """
        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.claimMembershipButton.setDisabled(True)
        result = self.application.smiths.claim_membership(
            self.application.wallets.get_keypair(self.account.address)
        )
        if not result:
            self.errorLabel.setText(self._("Unable to claim membership"))

        self.claimMembershipButton.setEnabled(True)
        self.fetch_membership_from_network_timer.start(
            self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
        )

        self.claim_membership_timer.stop()

    def publish_keys_timer_function(self):
        """
        Triggered when user click on publish keys button

        :return:
        """
        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.publishKeysButton.setDisabled(True)
        result = self.application.authorities.publish_session_keys(
            self.application.wallets.get_keypair(self.account.address),
            self.current_node.session_keys,
        )
        if not result:
            self.errorLabel.setText(self._("Unable to publish session keys"))

        self.publishKeysButton.setEnabled(True)
        self.publish_keys_timer.stop()

    def go_online_timer_function(self):
        """
        Triggered when user click on go online button

        :return:
        """
        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.goOnlineButton.setDisabled(True)
        result = self.application.authorities.go_online(
            self.application.wallets.get_keypair(self.account.address)
        )
        if not result:
            self.errorLabel.setText(self._("Unable to claim membership"))

        self.goOnlineButton.setEnabled(True)
        self.fetch_membership_from_network_timer.start(
            self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
        )

        self.go_online_timer.stop()

    def go_offline_timer_function(self):
        """
        Triggered when user click on go offline button

        :return:
        """
        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.goOfflineButton.setDisabled(True)
        result = self.application.authorities.go_offline(
            self.application.wallets.get_keypair(self.account.address)
        )
        if not result:
            self.errorLabel.setText(self._("Unable to claim membership"))

        self.goOfflineButton.setEnabled(True)
        self.fetch_membership_from_network_timer.start(
            self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
        )

        self.go_offline_timer.stop()

    def _on_refresh_smith_button_clicked(self, _):
        """ """
        self.loader_movie.start()
        self.loaderIconLabel.show()
        self.fetch_membership_from_network_timer.start()
        self.fetch_authority_status_from_network_timer.start()

    def fetch_membership_from_network_timer_function(self):
        """
        Update smith membership infos from current url connection

        :return:
        """
        if self.account is None or self.account.identity_index is None:
            return

        # Start the thread
        # get membership status
        self.membership = self.application.smiths.fetch_membership_from_network(
            self.account.identity_index
        )
        if self.membership is None:
            # get pending status
            self.pending_membership = (
                self.application.smiths.fetch_pending_membership_from_network(
                    self.account.identity_index
                )
            )

        if self.pending_membership is True or self.membership is not None:
            # get certification list
            self.certs_by_receiver = (
                self.application.smiths.fetch_certs_by_receiver_from_network(
                    self.account.address, self.account.identity_index
                )
            )

        self.refreshSmithButton.setEnabled(True)
        self.loaderIconLabel.hide()

        self._update_ui()

        self.fetch_membership_from_network_timer.stop()

    def fetch_authority_status_from_network_timer_function(self):
        """
        Update authority status for account identity from current url connection

        :return:
        """
        if self.account is None or self.account.identity_index is None:
            return

        # Start the thread
        self.authority_status = self.AUTHORITY_STATUS_NO

        is_online = self.application.authorities.fetch_is_online_from_network(
            self.account.identity_index
        )
        if is_online is True:
            self.authority_status = self.AUTHORITY_STATUS_ONLINE
        else:
            is_incoming = self.application.authorities.fetch_is_incoming_from_network(
                self.account.identity_index
            )
            if is_incoming is True:
                self.authority_status = self.AUTHORITY_STATUS_INCOMING
            else:
                is_outgoing = (
                    self.application.authorities.fetch_is_outgoing_from_network(
                        self.account.identity_index
                    )
                )
                if is_outgoing is True:
                    self.authority_status = self.AUTHORITY_STATUS_OUTGOING

        self.loaderIconLabel.hide()

        self._update_ui()

        self.fetch_authority_status_from_network_timer.stop()

    def _update_ui(self):
        """
        Update node infos in UI

        :return:
        """
        self.errorLabel.setText("")
        self.urlValueLabel.setText(self.current_node.url)

        if self.current_node.session_keys is not None:
            self.sessionKeysTextBrowser.setText(self.current_node.session_keys)
        else:
            self.sessionKeysTextBrowser.setText("")

        if not self.application.connections.is_connected():
            self.rotateKeysButton.setDisabled(True)
            self.refreshSmithButton.setDisabled(True)
            self.publishKeysButton.setDisabled(True)
            self.requestMembershipButton.setDisabled(True)
            self.claimMembershipButton.setDisabled(True)
            self.revokeSmithMembershipButton.setDisabled(True)
            self.goOnlineButton.setDisabled(True)
            self.goOfflineButton.setDisabled(True)
            self.errorLabel.setText(self._("No network connection"))
            return

        # rotate keys only available on localhost via an ssh tunnel or other method...
        self.rotateKeysButton.setEnabled(
            "localhost" in self.application.nodes.get_current_url()
        )

        # disable all buttons
        self.refreshSmithButton.setDisabled(True)
        self.publishKeysButton.setDisabled(True)
        self.requestMembershipButton.setDisabled(True)
        self.claimMembershipButton.setDisabled(True)
        self.revokeSmithMembershipButton.setDisabled(True)
        self.goOnlineButton.setDisabled(True)
        self.goOfflineButton.setDisabled(True)

        if self.account is not None:
            self.refreshSmithButton.setEnabled(True)
            if self.current_node.session_keys is not None:
                if self.membership is not None:
                    self.publishKeysButton.setEnabled(True)
            if self.membership is None and self.pending_membership is False:
                self.requestMembershipButton.setEnabled(True)
            if self.membership is None and self.pending_membership is True:
                self.claimMembershipButton.setEnabled(True)
            if self.membership is not None:
                self.revokeSmithMembershipButton.setEnabled(True)
                self.goOnlineButton.setEnabled(
                    self.authority_status == self.AUTHORITY_STATUS_NO
                )
                self.goOfflineButton.setEnabled(
                    self.authority_status == self.AUTHORITY_STATUS_ONLINE
                )

        if self.membership is not None:
            # display membership expiration block number
            # QLocale.toString(app_utils.get_default_locale(), d, 'dd MMM')
            datetime_from_block = self.application.block_time.get_datetime_from_block(
                self.membership.expire_on
            )
            if datetime_from_block is not None:
                expire_on_localized_datetime_string = self.locale().toString(
                    datetime_from_block,
                    QLocale.dateFormat(self.locale(), QLocale.ShortFormat),
                )
                self.membershipValueLabel.setText(
                    self._("expire on {datetime}").format(
                        datetime=expire_on_localized_datetime_string
                    )
                )
            else:
                self.membershipValueLabel.setText(
                    self._("expire on block #{block}").format(
                        block=self.membership.expire_on
                    )
                )
            self.membershipValueLabel.setToolTip(
                self._("block #{block}").format(block=self.membership.expire_on)
            )
        elif self.pending_membership is True:
            self.membershipValueLabel.setText(self._("Pending..."))
        else:
            self.membershipValueLabel.setText(self._("No"))

        if self.authority_status == self.AUTHORITY_STATUS_NO:
            self.authorityValueLabel.setText(self._("No"))
        elif self.authority_status == self.AUTHORITY_STATUS_INCOMING:
            self.authorityValueLabel.setText(self._("Incoming..."))
        elif self.authority_status == self.AUTHORITY_STATUS_ONLINE:
            self.authorityValueLabel.setText(self._("Online"))
        elif self.authority_status == self.AUTHORITY_STATUS_OUTGOING:
            self.authorityValueLabel.setText(self._("Outgoing..."))

        # clear certification table
        self.certifiersTableWidget.clearContents()

        if self.certs_by_receiver is not None:
            self.certifiersTableWidget.setRowCount(len(self.certs_by_receiver))
            for row_index, smith_certification in enumerate(self.certs_by_receiver):
                identity_item = QTableWidgetItem(
                    str(smith_certification.issuer_identity_index)
                )
                address_item = QTableWidgetItem(str(smith_certification.issuer_address))

                datetime_from_block = (
                    self.application.block_time.get_datetime_from_block(
                        smith_certification.expire_on_block
                    )
                )
                if datetime_from_block is not None:
                    expire_on_localized_datetime_string = self.locale().toString(
                        datetime_from_block,
                        QLocale.dateFormat(self.locale(), QLocale.ShortFormat),
                    )
                    expire_on_item = QTableWidgetItem(
                        expire_on_localized_datetime_string
                    )
                    expire_on_item.setToolTip(
                        self._("block #{block}").format(
                            block=smith_certification.expire_on_block
                        )
                    )
                else:
                    expire_on_item = QTableWidgetItem(
                        f"#{smith_certification.expire_on_block}"
                    )

                self.certifiersTableWidget.setItem(row_index, 0, identity_item)
                self.certifiersTableWidget.setItem(row_index, 1, address_item)
                self.certifiersTableWidget.setItem(row_index, 2, expire_on_item)

            self.certifiersTableWidget.resizeColumnsToContents()
            self.certifiersTableWidget.horizontalHeader().stretchLastSection()

    def _on_currency_event(self, _):
        """
        When a currency event is triggered

        :param _: CurrencyEvent instance
        :return:
        """
        self.init_account_combo_box()
        if self.account is not None:
            self.fetch_membership_from_network_timer.start()
        else:
            self._update_ui()

    def on_connections_event(self, _):
        """
        Triggered when the network connection if connected/disconnected

        :param _: ConnectionsEvent instance
        :return:
        """

        self.current_node = self.application.nodes.get(
            self.application.nodes.get_current_url()
        )
        self.init_account_combo_box()
        self._update_ui()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)

    main_window = QMainWindow()
    main_window.show()
    validator_node = Node(url="ws://localhost:9944")
    if application_.nodes.get(validator_node.url) is None:
        application_.nodes.add(validator_node)
    application_.nodes.set_current_url(validator_node.url)
    main_window.setCentralWidget(SmithWidget(application_, main_window))

    sys.exit(qapp.exec_())
