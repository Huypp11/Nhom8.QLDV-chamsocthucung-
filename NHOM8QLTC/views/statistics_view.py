"""
Tang 3 - VIEW: Giao dien thong ke
"""
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from controllers.statistics_controller import StatisticsController
from ui.statistics_ui import Ui_StatisticsWidget


class RevenueChart(QWidget):
    COLORS = [
        "#2563eb", "#16a34a", "#f97316", "#dc2626", "#7c3aed", "#0891b2",
        "#ca8a04", "#db2777", "#4f46e5", "#059669", "#ea580c", "#64748b",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []
        self.setMinimumHeight(240)
        self.setMaximumHeight(300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_data(self, rows):
        self._rows = rows
        self.update()

    def _chart_rows(self):
        rows = [row for row in self._rows if float(row.get("total") or 0) > 0]
        rows.sort(key=lambda row: float(row.get("total") or 0), reverse=True)
        if len(rows) <= 12:
            return rows

        visible = rows[:11]
        other_total = sum(float(row.get("total") or 0) for row in rows[11:])
        visible.append({"period": "Khac", "total": other_total})
        return visible

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor("#ffffff"))

        rows = self._chart_rows()
        total_revenue = sum(float(row.get("total") or 0) for row in rows)
        if not rows or total_revenue <= 0:
            painter.setPen(QColor("#6b7280"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Khong co du lieu")
            return

        side = min(self.width() * 0.45, self.height() - 32)
        pie_rect = QRectF(24, 16, side, side)
        start_angle = 90 * 16
        painter.setPen(Qt.NoPen)

        for idx, row in enumerate(rows):
            value = float(row.get("total") or 0)
            span_angle = int(-360 * 16 * value / total_revenue)
            color = QColor(self.COLORS[idx % len(self.COLORS)])
            painter.setBrush(color)
            painter.drawPie(pie_rect, start_angle, span_angle)
            start_angle += span_angle

        painter.setBrush(QColor("#ffffff"))
        hole = pie_rect.adjusted(side * 0.28, side * 0.28, -side * 0.28, -side * 0.28)
        painter.drawEllipse(hole)

        painter.setPen(QColor("#111827"))
        painter.drawText(hole, Qt.AlignCenter, f"{total_revenue:,.0f}\nVND")

        legend_x = int(pie_rect.right() + 28)
        legend_y = 22
        line_height = 20
        painter.setPen(QColor("#374151"))
        for idx, row in enumerate(rows):
            y = legend_y + idx * line_height
            color = QColor(self.COLORS[idx % len(self.COLORS)])
            painter.fillRect(legend_x, y + 3, 12, 12, color)
            value = float(row.get("total") or 0)
            percent = value * 100 / total_revenue
            label = str(row.get("period") or "")
            painter.drawText(
                legend_x + 18,
                y + 14,
                f"{label}: {percent:.1f}% ({value:,.0f})",
            )


class BarChart(QWidget):
    def __init__(self, label_key, value_key="total", bar_color="#2563eb", parent=None):
        super().__init__(parent)
        self.label_key = label_key
        self.value_key = value_key
        self.bar_color = QColor(bar_color)
        self._rows = []
        self.setMinimumHeight(240)
        self.setMaximumHeight(300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_data(self, rows):
        self._rows = rows
        self.update()

    def _chart_rows(self):
        rows = [
            row for row in self._rows
            if float(row.get(self.value_key) or 0) > 0
        ]
        if len(rows) <= 12:
            return rows

        visible = rows[:11]
        other_total = sum(float(row.get(self.value_key) or 0) for row in rows[11:])
        visible.append({self.label_key: "Khac", self.value_key: other_total})
        return visible

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        rows = self._chart_rows()
        if not rows:
            painter.setPen(QColor("#6b7280"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Khong co du lieu")
            return

        values = [float(row.get(self.value_key) or 0) for row in rows]
        max_value = max(values)
        if max_value <= 0:
            painter.setPen(QColor("#6b7280"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Khong co du lieu")
            return

        left, top, right, bottom = 48, 20, 20, 54
        chart_w = max(1, self.width() - left - right)
        chart_h = max(1, self.height() - top - bottom)
        base_y = top + chart_h

        painter.setPen(QColor("#d1d5db"))
        painter.drawLine(left, top, left, base_y)
        painter.drawLine(left, base_y, left + chart_w, base_y)

        bar_gap = 10
        bar_w = max(12, int((chart_w - bar_gap * (len(rows) + 1)) / len(rows)))
        if bar_w * len(rows) + bar_gap * (len(rows) + 1) > chart_w:
            bar_gap = 4
            bar_w = max(8, int((chart_w - bar_gap * (len(rows) + 1)) / len(rows)))

        painter.setFont(QFont("", 8))
        for idx, row in enumerate(rows):
            value = float(row.get(self.value_key) or 0)
            bar_h = int(chart_h * value / max_value)
            x = left + bar_gap + idx * (bar_w + bar_gap)
            y = base_y - bar_h
            painter.fillRect(x, y, bar_w, bar_h, self.bar_color)

            painter.setPen(QColor("#111827"))
            painter.drawText(
                QRectF(x - 8, max(top, y - 20), bar_w + 16, 18),
                Qt.AlignCenter,
                f"{value:,.0f}",
            )

            label = str(row.get(self.label_key) or "")
            if len(label) > 12:
                label = label[:11] + "..."
            painter.setPen(QColor("#374151"))
            painter.drawText(
                QRectF(x - 16, base_y + 6, bar_w + 32, 36),
                Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap,
                label,
            )


class StatisticsView(QWidget, Ui_StatisticsWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.verticalLayout.setContentsMargins(14, 12, 14, 10)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.titleLabel.setMaximumHeight(40)
        for label in (
            self.total_customers_label,
            self.total_pets_label,
            self.total_appointments_label,
        ):
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            label.setMinimumHeight(30)
            label.setMaximumHeight(36)
        self.summary_container = self._wrap_layout(self.summaryLayout, 46)
        self.controller = StatisticsController()
        self._setup_chart_selector()
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Ngày", "Tuần", "Tháng", "Năm"])
        self.revenueLayout.insertWidget(1, self.period_combo)
        self.period_combo.setMinimumHeight(30)
        self.year_spinbox.setMinimumHeight(30)
        self.revenue_btn.setMinimumHeight(32)
        self.revenue_controls_container = self._wrap_layout(self.revenueLayout, 48)
        self.revenue_chart = RevenueChart()
        self.revenue_table.setMaximumHeight(130)
        self.revenue_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.verticalLayout.insertWidget(
            self.verticalLayout.indexOf(self.revenue_table) + 1,
            self.revenue_chart,
        )
        self.popular_btn.setMinimumHeight(32)
        self.popular_container = self._wrap_layout(self.popularLayout, 48)
        self._setup_customer_statistics()
        self._setup_product_statistics()
        self._connect_signals()
        self.refresh_summary()
        self.show_revenue()
        self.show_customer_statistics()
        self.show_product_statistics()
        self.show_chart_section("revenue")

    def _wrap_layout(self, layout, height):
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        for index in range(self.verticalLayout.count()):
            item = self.verticalLayout.itemAt(index)
            if item.layout() is layout:
                self.verticalLayout.takeAt(index)
                container = QWidget(self)
                container.setLayout(layout)
                container.setMinimumHeight(height)
                container.setMaximumHeight(height)
                container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.verticalLayout.insertWidget(index, container)
                return container
        return None

    def _setup_chart_selector(self):
        self.chart_selector_layout = QHBoxLayout()
        self.chart_selector_label = QLabel("Xem bieu do:")
        self.revenue_chart_btn = QPushButton("Doanh thu")
        self.customer_chart_btn = QPushButton("Khach hang")
        self.product_chart_btn = QPushButton("San pham")

        self.chart_button_group = QButtonGroup(self)
        self.chart_button_group.setExclusive(True)
        for button in (
            self.revenue_chart_btn,
            self.customer_chart_btn,
            self.product_chart_btn,
        ):
            button.setCheckable(True)
            self.chart_button_group.addButton(button)

        self.chart_selector_layout.addWidget(self.chart_selector_label)
        self.chart_selector_layout.addWidget(self.revenue_chart_btn)
        self.chart_selector_layout.addWidget(self.customer_chart_btn)
        self.chart_selector_layout.addWidget(self.product_chart_btn)
        self.chart_selector_layout.addStretch()
        self.verticalLayout.insertLayout(2, self.chart_selector_layout)
        for button in (
            self.revenue_chart_btn,
            self.customer_chart_btn,
            self.product_chart_btn,
        ):
            button.setMinimumHeight(32)
        self.chart_selector_container = self._wrap_layout(self.chart_selector_layout, 48)

    def _setup_customer_statistics(self):
        popular_index = max(0, self.verticalLayout.indexOf(self.services_table) - 1)
        self.customer_stats_layout = QHBoxLayout()
        self.customer_stats_label = QLabel("Khach hang theo:")
        self.customer_period_combo = QComboBox()
        self.customer_period_combo.addItems(["Tuan", "Thang", "Nam"])
        self.customer_stats_btn = QPushButton("Xem")
        self.customer_stats_layout.addWidget(self.customer_stats_label)
        self.customer_stats_layout.addWidget(self.customer_period_combo)
        self.customer_stats_layout.addWidget(self.customer_stats_btn)
        self.customer_stats_layout.addStretch()
        self.verticalLayout.insertLayout(
            popular_index,
            self.customer_stats_layout,
        )
        self.customer_period_combo.setMinimumHeight(30)
        self.customer_stats_btn.setMinimumHeight(32)
        self.customer_controls_container = self._wrap_layout(self.customer_stats_layout, 48)

        self.customer_stats_table = QTableWidget()
        self.customer_stats_table.setColumnCount(2)
        self.customer_stats_table.setHorizontalHeaderLabels(["Thoi gian", "So khach hang"])
        self.customer_stats_table.horizontalHeader().setStretchLastSection(True)
        self.customer_stats_table.setMaximumHeight(120)
        self.customer_stats_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.verticalLayout.insertWidget(
            popular_index + 1,
            self.customer_stats_table,
        )

        self.customer_chart = BarChart("period", "total", "#16a34a")
        self.verticalLayout.insertWidget(
            popular_index + 2,
            self.customer_chart,
        )

    def _setup_product_statistics(self):
        self.product_stats_layout = QHBoxLayout()
        self.product_stats_label = QLabel("San pham ban ra theo:")
        self.product_period_combo = QComboBox()
        self.product_period_combo.addItems(["Ngay", "Tuan", "Thang", "Nam"])
        self.product_stats_btn = QPushButton("Xem")
        self.product_stats_layout.addWidget(self.product_stats_label)
        self.product_stats_layout.addWidget(self.product_period_combo)
        self.product_stats_layout.addWidget(self.product_stats_btn)
        self.product_stats_layout.addStretch()
        self.verticalLayout.addLayout(self.product_stats_layout)
        self.product_period_combo.setMinimumHeight(30)
        self.product_stats_btn.setMinimumHeight(32)
        self.product_controls_container = self._wrap_layout(self.product_stats_layout, 48)

        self.product_stats_table = QTableWidget()
        self.product_stats_table.setColumnCount(2)
        self.product_stats_table.setHorizontalHeaderLabels(["Thoi gian", "So luong ban"])
        self.product_stats_table.horizontalHeader().setStretchLastSection(True)
        self.product_stats_table.setMaximumHeight(120)
        self.product_stats_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.verticalLayout.addWidget(self.product_stats_table)

        self.product_chart = BarChart("period", "total", "#f97316")
        self.verticalLayout.addWidget(self.product_chart)

    def _connect_signals(self):
        self.revenue_btn.clicked.connect(self.show_revenue_section)
        self.popular_btn.clicked.connect(self.show_popular_services)
        self.period_combo.currentIndexChanged.connect(self.show_revenue)
        self.customer_stats_btn.clicked.connect(self.show_customer_section)
        self.customer_period_combo.currentIndexChanged.connect(self.show_customer_statistics)
        self.product_stats_btn.clicked.connect(self.show_product_section)
        self.product_period_combo.currentIndexChanged.connect(self.show_product_statistics)
        self.year_spinbox.valueChanged.connect(self.refresh_active_chart)
        self.revenue_chart_btn.clicked.connect(self.show_revenue_section)
        self.customer_chart_btn.clicked.connect(self.show_customer_section)
        self.product_chart_btn.clicked.connect(self.show_product_section)

    def _set_layout_visible(self, layout, visible):
        for index in range(layout.count()):
            item = layout.itemAt(index)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.setVisible(visible)
            if child_layout is not None:
                self._set_layout_visible(child_layout, visible)

    def show_chart_section(self, section):
        self.active_chart_section = section
        if hasattr(self, "popular_container") and self.popular_container is not None:
            self.popular_container.setVisible(False)
        self._set_layout_visible(self.popularLayout, False)
        self.services_table.setVisible(False)

        self.revenue_controls_container.setVisible(section == "revenue")
        self._set_layout_visible(self.revenueLayout, section == "revenue")
        self.revenue_table.setVisible(section == "revenue")
        self.revenue_chart.setVisible(section == "revenue")

        self.customer_controls_container.setVisible(section == "customer")
        self._set_layout_visible(self.customer_stats_layout, section == "customer")
        self.customer_stats_table.setVisible(section == "customer")
        self.customer_chart.setVisible(section == "customer")

        self.product_controls_container.setVisible(section == "product")
        self._set_layout_visible(self.product_stats_layout, section == "product")
        self.product_stats_table.setVisible(section == "product")
        self.product_chart.setVisible(section == "product")

        self.revenue_chart_btn.setChecked(section == "revenue")
        self.customer_chart_btn.setChecked(section == "customer")
        self.product_chart_btn.setChecked(section == "product")

    def show_revenue_section(self):
        self.show_revenue()
        self.show_chart_section("revenue")

    def show_customer_section(self):
        self.show_customer_statistics()
        self.show_chart_section("customer")

    def show_product_section(self):
        self.show_product_statistics()
        self.show_chart_section("product")

    def refresh_active_chart(self):
        section = getattr(self, "active_chart_section", "revenue")
        if section == "revenue":
            self.show_revenue()
        elif section == "customer":
            self.show_customer_statistics()
        elif section == "product":
            self.show_product_statistics()

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
        self.show_revenue()

    def show_revenue(self):
        year = self.year_spinbox.value()
        period_map = {
            "Ngày": "day",
            "Tuần": "week",
            "Tháng": "month",
            "Năm": "year",
        }
        period = period_map.get(self.period_combo.currentText(), "month")
        rows = self.controller.get_revenue_by_period(period, year)
        self.revenue_table.setRowCount(0)
        self.revenue_table.setHorizontalHeaderLabels(["Thời gian", "Doanh Thu (VND)"])
        for row in rows:
            r = self.revenue_table.rowCount()
            self.revenue_table.insertRow(r)
            self.revenue_table.setItem(r, 0, QTableWidgetItem(str(row["period"])))
            self.revenue_table.setItem(
                r,
                1,
                QTableWidgetItem(f"{row['total']:,.0f} đ"),
            )
        self.revenue_table.resizeColumnsToContents()
        self.revenue_chart.set_data(rows)

    def show_customer_statistics(self):
        period_map = {
            "Tuan": "week",
            "Thang": "month",
            "Nam": "year",
        }
        period = period_map.get(self.customer_period_combo.currentText(), "month")
        rows = self.controller.get_customer_count_by_period(period, self.year_spinbox.value())
        self.customer_stats_table.setRowCount(0)
        for row in rows:
            r = self.customer_stats_table.rowCount()
            self.customer_stats_table.insertRow(r)
            self.customer_stats_table.setItem(r, 0, QTableWidgetItem(str(row["period"])))
            self.customer_stats_table.setItem(r, 1, QTableWidgetItem(str(row["total"])))
        self.customer_stats_table.resizeColumnsToContents()
        self.customer_chart.set_data(rows)

    def show_product_statistics(self):
        period_map = {
            "Ngay": "day",
            "Tuan": "week",
            "Thang": "month",
            "Nam": "year",
        }
        period = period_map.get(self.product_period_combo.currentText(), "month")
        rows = self.controller.get_products_sold_by_period(
            period,
            self.year_spinbox.value(),
        )
        self.product_stats_table.setRowCount(0)
        for row in rows:
            r = self.product_stats_table.rowCount()
            self.product_stats_table.insertRow(r)
            self.product_stats_table.setItem(r, 0, QTableWidgetItem(str(row["period"])))
            self.product_stats_table.setItem(r, 1, QTableWidgetItem(str(row["total"])))
        self.product_stats_table.resizeColumnsToContents()
        self.product_chart.set_data(rows)

    def show_popular_services(self):
        rows = self.controller.get_popular_services()
        self.services_table.setRowCount(0)
        for row in rows:
            r = self.services_table.rowCount()
            self.services_table.insertRow(r)
            self.services_table.setItem(r, 0, QTableWidgetItem(str(row["name"])))
            self.services_table.setItem(r, 1, QTableWidgetItem(str(row["count"])))
        self.services_table.resizeColumnsToContents()
