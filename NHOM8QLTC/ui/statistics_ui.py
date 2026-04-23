# -*- coding: utf-8 -*-
# File được tạo từ statistics_ui.ui - KHÔNG CHỈNH SỬA FILE NÀY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StatisticsWidget(object):
    def setupUi(self, StatisticsWidget):
        StatisticsWidget.setObjectName("StatisticsWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(StatisticsWidget)

        # Tiêu đề
        self.titleLabel = QtWidgets.QLabel("Thống Kê")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.titleLabel.setFont(font)
        self.verticalLayout.addWidget(self.titleLabel)

        # Tổng quan
        self.summaryLayout = QtWidgets.QHBoxLayout()
        self.total_customers_label = QtWidgets.QLabel("👥 Tổng Khách Hàng: 0")
        self.total_customers_label.setAlignment(QtCore.Qt.AlignCenter)
        self.total_pets_label = QtWidgets.QLabel("🐾 Tổng Thú Cưng: 0")
        self.total_pets_label.setAlignment(QtCore.Qt.AlignCenter)
        self.total_appointments_label = QtWidgets.QLabel("📅 Tổng Lịch Hẹn: 0")
        self.total_appointments_label.setAlignment(QtCore.Qt.AlignCenter)
        for lbl in [self.total_customers_label, self.total_pets_label, self.total_appointments_label]:
            self.summaryLayout.addWidget(lbl)
        self.verticalLayout.addLayout(self.summaryLayout)

        # Doanh thu theo năm
        self.revenueLayout = QtWidgets.QHBoxLayout()
        self.revenueLabel = QtWidgets.QLabel("Doanh Thu Năm:")
        self.year_spinbox = QtWidgets.QSpinBox()
        self.year_spinbox.setMinimum(2000)
        self.year_spinbox.setMaximum(2100)
        self.year_spinbox.setValue(2026)
        self.revenue_btn = QtWidgets.QPushButton("Xem")
        self.revenueLayout.addWidget(self.revenueLabel)
        self.revenueLayout.addWidget(self.year_spinbox)
        self.revenueLayout.addWidget(self.revenue_btn)
        self.revenueLayout.addStretch()
        self.verticalLayout.addLayout(self.revenueLayout)

        # Bảng doanh thu
        self.revenue_table = QtWidgets.QTableWidget()
        self.revenue_table.setColumnCount(2)
        self.revenue_table.setHorizontalHeaderLabels(["Tháng", "Doanh Thu (VNĐ)"])
        self.revenue_table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.revenue_table)

        # Dịch vụ phổ biến
        self.popularLayout = QtWidgets.QHBoxLayout()
        self.popularLabel = QtWidgets.QLabel("Dịch Vụ Phổ Biến:")
        self.popular_btn = QtWidgets.QPushButton("Xem")
        self.popularLayout.addWidget(self.popularLabel)
        self.popularLayout.addWidget(self.popular_btn)
        self.popularLayout.addStretch()
        self.verticalLayout.addLayout(self.popularLayout)

        # Bảng dịch vụ
        self.services_table = QtWidgets.QTableWidget()
        self.services_table.setColumnCount(2)
        self.services_table.setHorizontalHeaderLabels(["Dịch Vụ", "Số Lượng"])
        self.services_table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.services_table)
