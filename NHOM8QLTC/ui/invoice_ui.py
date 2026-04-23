# -*- coding: utf-8 -*-
# File được tạo từ invoice_ui.ui - KHÔNG CHỈNH SỬA FILE NÀY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InvoiceWidget(object):
    def setupUi(self, InvoiceWidget):
        InvoiceWidget.setObjectName("InvoiceWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(InvoiceWidget)

        # Lọc khách hàng
        self.filterLayout = QtWidgets.QHBoxLayout()
        self.customerLabel = QtWidgets.QLabel("Khách hàng:")
        self.customer_combo = QtWidgets.QComboBox()
        self.customer_combo.setMinimumWidth(200)
        self.filter_btn = QtWidgets.QPushButton("Lọc")
        self.filterLayout.addWidget(self.customerLabel)
        self.filterLayout.addWidget(self.customer_combo)
        self.filterLayout.addWidget(self.filter_btn)
        self.filterLayout.addStretch()
        self.verticalLayout.addLayout(self.filterLayout)

        # Nút thao tác
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("➕ Tạo Hóa Đơn")
        self.view_btn = QtWidgets.QPushButton("👁️ Xem Chi Tiết")
        self.export_btn = QtWidgets.QPushButton("📥 Xuất Hóa Đơn")
        for btn in [self.add_btn, self.view_btn, self.export_btn]:
            self.buttonLayout.addWidget(btn)
        self.buttonLayout.addStretch()
        self.verticalLayout.addLayout(self.buttonLayout)

        # Bảng
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID Hóa Đơn", "ID Lịch Hẹn", "Khách Hàng", "Tổng Tiền", "Phương Thức", "Ngày"
        ])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table)
