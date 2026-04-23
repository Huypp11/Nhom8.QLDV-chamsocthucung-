# -*- coding: utf-8 -*-
# File được tạo từ service_ui.ui - KHÔNG CHỈNH SỬA FILE NÀY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ServiceWidget(object):
    def setupUi(self, ServiceWidget):
        ServiceWidget.setObjectName("ServiceWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(ServiceWidget)

        # Tìm kiếm
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLabel = QtWidgets.QLabel("Tìm kiếm dịch vụ:")
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên dịch vụ...")
        self.search_btn = QtWidgets.QPushButton("Tìm kiếm")
        self.searchLayout.addWidget(self.searchLabel)
        self.searchLayout.addWidget(self.search_input)
        self.searchLayout.addWidget(self.search_btn)
        self.verticalLayout.addLayout(self.searchLayout)

        # Nút thao tác
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("➕ Thêm Dịch Vụ")
        self.edit_btn = QtWidgets.QPushButton("✏️ Chỉnh Sửa")
        self.delete_btn = QtWidgets.QPushButton("🗑️ Xóa")
        self.refresh_btn = QtWidgets.QPushButton("🔄 Làm Mới")
        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.refresh_btn]:
            self.buttonLayout.addWidget(btn)
        self.buttonLayout.addStretch()
        self.verticalLayout.addLayout(self.buttonLayout)

        # Bảng
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tên Dịch Vụ", "Mô Tả", "Giá (VNĐ)", "Thời Gian (phút)"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table)
