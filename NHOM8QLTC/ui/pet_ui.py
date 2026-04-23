# -*- coding: utf-8 -*-
# File được tạo từ pet_ui.ui - KHÔNG CHỈNH SỬA FILE NÀY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PetWidget(object):
    def setupUi(self, PetWidget):
        PetWidget.setObjectName("PetWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(PetWidget)

        # Lọc khách hàng
        self.filterLayout = QtWidgets.QHBoxLayout()
        self.filterLabel = QtWidgets.QLabel("Khách hàng:")
        self.customer_combo = QtWidgets.QComboBox()
        self.customer_combo.setMinimumWidth(200)
        self.filterLayout.addWidget(self.filterLabel)
        self.filterLayout.addWidget(self.customer_combo)
        self.filterLayout.addStretch()
        self.verticalLayout.addLayout(self.filterLayout)

        # Nút thao tác
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("➕ Thêm Thú Cưng")
        self.edit_btn = QtWidgets.QPushButton("✏️ Chỉnh Sửa")
        self.delete_btn = QtWidgets.QPushButton("🗑️ Xóa")
        for btn in [self.add_btn, self.edit_btn, self.delete_btn]:
            self.buttonLayout.addWidget(btn)
        self.buttonLayout.addStretch()
        self.verticalLayout.addLayout(self.buttonLayout)

        # Bảng
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Tên", "Loài", "Tuổi", "Giống", "Ngày Tạo"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table)
