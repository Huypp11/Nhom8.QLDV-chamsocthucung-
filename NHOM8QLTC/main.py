"""
main.py - Khoi dong ung dung Quan Ly Cua Hang Cham Soc Thu Cung
Mo hinh 3 tang: Database -> Model -> View
"""
import os
import sys

# Them thu muc goc vao path de import dung khi chay truc tiep main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from database.db_manager import init_db
from ui.main_window_ui import Ui_MainWindow
from views.appointment_view import AppointmentView
from views.customer_view import CustomerView
from views.invoice_view import InvoiceView
from views.login_view import LoginDialog
from views.pet_view import PetView
from views.product_view import ProductView
from views.service_view import ServiceView
from views.statistics_view import StatisticsView
from views.user_view import UserView


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.logout_requested = False
        self.setupUi(self)

        # Khoi tao cac trang
        self.customer_view = CustomerView()
        self.pet_view = PetView()
        self.service_view = ServiceView()
        self.product_view = ProductView()
        self.appointment_view = AppointmentView()
        self.invoice_view = InvoiceView()
        self.statistics_view = StatisticsView()
        self.user_view = UserView()

        # Them vao stacked widget
        for view in [
            self.customer_view,
            self.pet_view,
            self.service_view,
            self.product_view,
            self.appointment_view,
            self.invoice_view,
            self.statistics_view,
            self.user_view,
        ]:
            self.stacked_widget.addWidget(view)

        # Ket noi sidebar buttons
        self.btn_customer.clicked.connect(self._show_customer)
        self.btn_pet.clicked.connect(self._show_pet)
        self.btn_service.clicked.connect(self._show_service)
        self.btn_product.clicked.connect(self._show_product)
        self.btn_appointment.clicked.connect(self._show_appointment)
        self.btn_invoice.clicked.connect(self._show_invoice)
        self.btn_statistics.clicked.connect(self._show_statistics)
        self.btn_user.clicked.connect(self._show_user)
        self.btn_logout.clicked.connect(self._logout)

        self._apply_permissions()
        self._show_customer()

    def _apply_permissions(self):
        role = self.current_user.get("role", "nhanvien")
        full_name = self.current_user.get(
            "full_name", self.current_user.get("username", "")
        )
        role_name = "Admin" if role == "admin" else "Nhân viên"

        self.userLabel.setText(f"{full_name}\n{role_name}")
        self.btn_user.setVisible(role == "admin")
        self.btn_statistics.setVisible(role == "admin")

        if role != "admin":
            self.stacked_widget.removeWidget(self.user_view)
            self.stacked_widget.removeWidget(self.statistics_view)

    def _show_customer(self):
        self.stacked_widget.setCurrentWidget(self.customer_view)
        self.statusbar.showMessage("Quản lý khách hàng")

    def _show_pet(self):
        self.pet_view.load_customers()
        self.stacked_widget.setCurrentWidget(self.pet_view)
        self.statusbar.showMessage("Quản lý thú cưng")

    def _show_service(self):
        self.stacked_widget.setCurrentWidget(self.service_view)
        self.statusbar.showMessage("Quản lý dịch vụ")

    def _show_product(self):
        self.product_view.load_data()
        self.stacked_widget.setCurrentWidget(self.product_view)
        self.statusbar.showMessage("Quản lý sản phẩm")

    def _show_appointment(self):
        self.stacked_widget.setCurrentWidget(self.appointment_view)
        self.statusbar.showMessage("Quản lý lịch hẹn")

    def _show_invoice(self):
        self.invoice_view._load_customers()
        self.invoice_view.load_data()
        self.stacked_widget.setCurrentWidget(self.invoice_view)
        self.statusbar.showMessage("Quản lý thanh toán")

    def _show_statistics(self):
        if self.current_user.get("role") != "admin":
            self.statusbar.showMessage("Ban khong co quyen xem thong ke")
            return
        self.statistics_view.refresh_summary()
        self.stacked_widget.setCurrentWidget(self.statistics_view)
        self.statusbar.showMessage("Thống kê")

    def _show_user(self):
        if self.current_user.get("role") != "admin":
            self.statusbar.showMessage("Bạn không có quyền quản lý tài khoản")
            return
        self.user_view.load_data()
        self.stacked_widget.setCurrentWidget(self.user_view)
        self.statusbar.showMessage("Quản lý tài khoản")

    def _logout(self):
        self.logout_requested = True
        self.close()


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    while True:
        login_dialog = LoginDialog()
        if login_dialog.exec_() != QDialog.Accepted:
            sys.exit(0)

        window = MainWindow(login_dialog.current_user)
        window.show()
        app.exec_()

        if not window.logout_requested:
            break
