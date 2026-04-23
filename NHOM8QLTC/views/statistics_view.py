"""
Tầng 3 - VIEW: Giao diện thống kê
"""
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from ui.statistics_ui import Ui_StatisticsWidget
from models.customer_model import CustomerModel
from models.pet_model import PetModel
from models.appointment_model import AppointmentModel
from models.invoice_model import InvoiceModel
from models.service_model import ServiceModel


class StatisticsView(QWidget, Ui_StatisticsWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._connect_signals()
        self.refresh_summary()

    def _connect_signals(self):
        self.revenue_btn.clicked.connect(self.show_monthly_revenue)
        self.popular_btn.clicked.connect(self.show_popular_services)

    def refresh_summary(self):
        self.total_customers_label.setText(
            f"👥 Tổng Khách Hàng: {CustomerModel().count()}")
        self.total_pets_label.setText(
            f"🐾 Tổng Thú Cưng: {PetModel().count()}")
        self.total_appointments_label.setText(
            f"📅 Tổng Lịch Hẹn: {AppointmentModel().count()}")

    def show_monthly_revenue(self):
        year = self.year_spinbox.value()
        rows = InvoiceModel().get_monthly_revenue(year)
        self.revenue_table.setRowCount(0)
        month_names = ["", "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4",
                        "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8",
                        "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"]
        for row in rows:
            r = self.revenue_table.rowCount()
            self.revenue_table.insertRow(r)
            month_idx = int(row["month"])
            month_name = month_names[month_idx] if month_idx < len(month_names) else f"Tháng {month_idx}"
            self.revenue_table.setItem(r, 0, QTableWidgetItem(month_name))
            self.revenue_table.setItem(r, 1, QTableWidgetItem(f"{row['total']:,.0f} đ"))
        self.revenue_table.resizeColumnsToContents()

    def show_popular_services(self):
        rows = ServiceModel().get_popular()
        self.services_table.setRowCount(0)
        for row in rows:
            r = self.services_table.rowCount()
            self.services_table.insertRow(r)
            self.services_table.setItem(r, 0, QTableWidgetItem(str(row["name"])))
            self.services_table.setItem(r, 1, QTableWidgetItem(str(row["count"])))
        self.services_table.resizeColumnsToContents()
