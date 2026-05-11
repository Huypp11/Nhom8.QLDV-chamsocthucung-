"""
main.py - Khởi động ứng dụng Quản Lý Cửa Hàng Chăm Sóc Thú Cưng
Mô hình 3 tầng: Database → Model → View
"""
import sys
import os

# Thêm thư mục gốc vào path để import đúng
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont

from database.db_manager import init_db
from ui.main_window_ui import Ui_MainWindow
from views.customer_view import CustomerView
from views.pet_view import PetView
from views.service_view import ServiceView
from views.product_view import ProductView          # <-- MỚI
from views.appointment_view import AppointmentView
from views.invoice_view import InvoiceView
from views.statistics_view import StatisticsView


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Khởi tạo các trang
        self.customer_view    = CustomerView()
        self.pet_view         = PetView()
        self.service_view     = ServiceView()
        self.product_view     = ProductView()        # <-- MỚI
        self.appointment_view = AppointmentView()
        self.invoice_view     = InvoiceView()
        self.statistics_view  = StatisticsView()

        # Thêm vào stacked widget
        for view in [self.customer_view, self.pet_view, self.service_view,
                     self.product_view,                                     # <-- MỚI
                     self.appointment_view, self.invoice_view, self.statistics_view]:
            self.stacked_widget.addWidget(view)

        # Kết nối sidebar buttons
        self.btn_customer.clicked.connect(self._show_customer)
        self.btn_pet.clicked.connect(self._show_pet)
        self.btn_service.clicked.connect(self._show_service)
        self.btn_product.clicked.connect(self._show_product)   # <-- MỚI (xem ghi chú bên dưới)
        self.btn_appointment.clicked.connect(self._show_appointment)
        self.btn_invoice.clicked.connect(self._show_invoice)
        self.btn_statistics.clicked.connect(self._show_statistics)

        # Mở trang Khách Hàng mặc định
        self._show_customer()

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

    def _show_product(self):                                     # <-- MỚI
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
        self.statistics_view.refresh_summary()
        self.stacked_widget.setCurrentWidget(self.statistics_view)
        self.statusbar.showMessage("Thống kê")


if __name__ == "__main__":
    # Khởi tạo database
    init_db()

    app = QApplication(sys.argv)

    # Font mặc định
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())