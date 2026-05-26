"""
Tang 3 - VIEW: Giao dien thong ke
"""
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from controllers.statistics_controller import StatisticsController
from ui.statistics_ui import Ui_StatisticsWidget


class StatisticsView(QWidget, Ui_StatisticsWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = StatisticsController()
        self._connect_signals()
        self.refresh_summary()

    def _connect_signals(self):
        self.revenue_btn.clicked.connect(self.show_monthly_revenue)
        self.popular_btn.clicked.connect(self.show_popular_services)

    def refresh_summary(self):
        summary = self.controller.get_summary()
        self.total_customers_label.setText(
            f"Tổng khách hàng: {summary['customers']}"
        )
        self.total_pets_label.setText(
            f"Tổng thú cưng: {summary['pets']}"
        )
        self.total_appointments_label.setText(
            f"Tổng lịch hẹn: {summary['appointments']}"
        )

    def show_monthly_revenue(self):
        year = self.year_spinbox.value()
        rows = self.controller.get_monthly_revenue(year)
        self.revenue_table.setRowCount(0)
        month_names = ["", "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4",
                       "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8",
                       "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"]
        for row in rows:
            r = self.revenue_table.rowCount()
            self.revenue_table.insertRow(r)
            month_idx = int(row["month"])
            month_name = (
                month_names[month_idx]
                if month_idx < len(month_names)
                else f"Tháng {month_idx}"
            )
            self.revenue_table.setItem(r, 0, QTableWidgetItem(month_name))
            self.revenue_table.setItem(r, 1, QTableWidgetItem(f"{row['total']:,.0f} đ"))
        self.revenue_table.resizeColumnsToContents()

    def show_popular_services(self):
        rows = self.controller.get_popular_services()
        self.services_table.setRowCount(0)
        for row in rows:
            r = self.services_table.rowCount()
            self.services_table.insertRow(r)
            self.services_table.setItem(r, 0, QTableWidgetItem(str(row["name"])))
            self.services_table.setItem(r, 1, QTableWidgetItem(str(row["count"])))
        self.services_table.resizeColumnsToContents()
