# -*- coding: utf-8 -*-
# File được tạo từ appointment_ui.ui - KHÔNG CHỈNH SỬA FILE NÀY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppointmentWidget(object):
    def setupUi(self, AppointmentWidget):
        AppointmentWidget.setObjectName("AppointmentWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(AppointmentWidget)

        # Lọc ngày
        self.filterLayout = QtWidgets.QHBoxLayout()
        self.dateLabel = QtWidgets.QLabel("Từ ngày:")
        self.date_from = QtWidgets.QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QtCore.QDate.currentDate())
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.dateToLabel = QtWidgets.QLabel("Đến ngày:")
        self.date_to = QtWidgets.QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QtCore.QDate.currentDate())
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.filter_btn = QtWidgets.QPushButton("Lọc")
        self.filterLayout.addWidget(self.dateLabel)
        self.filterLayout.addWidget(self.date_from)
        self.filterLayout.addWidget(self.dateToLabel)
        self.filterLayout.addWidget(self.date_to)
        self.filterLayout.addWidget(self.filter_btn)
        self.filterLayout.addStretch()
        self.verticalLayout.addLayout(self.filterLayout)

        # Nút thao tác
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("➕ Đặt Lịch Hẹn")
        self.edit_btn = QtWidgets.QPushButton("✏️ Chỉnh Sửa")
        self.complete_btn = QtWidgets.QPushButton("✓ Hoàn Thành")
        self.cancel_btn = QtWidgets.QPushButton("✗ Hủy")
        for btn in [self.add_btn, self.edit_btn, self.complete_btn, self.cancel_btn]:
            self.buttonLayout.addWidget(btn)
        self.buttonLayout.addStretch()
        self.verticalLayout.addLayout(self.buttonLayout)

        # Bảng
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Khách Hàng", "Thú Cưng", "Dịch Vụ", "Ngày Giờ", "Trạng Thái", "Ghi Chú"
        ])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table)
