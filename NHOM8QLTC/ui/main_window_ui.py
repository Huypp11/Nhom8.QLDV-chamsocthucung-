# -*- coding: utf-8 -*-
# File được tạo từ main_window.ui - KHÔNG CHỈNH SỬA FILE NÀY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 700)
        MainWindow.setWindowTitle("Quản Lý Dịch Vụ Chăm Sóc Thú Cưng")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        # Sidebar
        self.sidebar = QtWidgets.QWidget()
        self.sidebar.setMaximumWidth(180)
        self.sidebar.setMinimumWidth(160)
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)

        self.titleLabel = QtWidgets.QLabel("QUẢN LÝ DỊCH VỤ\nCHĂM SÓC THÚ CƯNG")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(11)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.sidebarLayout.addWidget(self.titleLabel)

        # Sidebar buttons
        self.btn_customer = QtWidgets.QPushButton("👥 Khách Hàng")
        self.btn_customer.setMinimumHeight(40)
        self.btn_pet = QtWidgets.QPushButton("🐾 Thú Cưng")
        self.btn_pet.setMinimumHeight(40)
        self.btn_service = QtWidgets.QPushButton("🛁 Dịch Vụ")
        self.btn_service.setMinimumHeight(40)
        self.btn_product = QtWidgets.QPushButton("📦 Sản Phẩm")
        self.btn_product.setMinimumHeight(40)
        self.btn_appointment = QtWidgets.QPushButton("📅 Lịch Hẹn")
        self.btn_appointment.setMinimumHeight(40)
        self.btn_invoice = QtWidgets.QPushButton("💰 Thanh Toán")
        self.btn_invoice.setMinimumHeight(40)
        self.btn_statistics = QtWidgets.QPushButton("📊 Thống Kê")
        self.btn_statistics.setMinimumHeight(40)

        for btn in [self.btn_customer, self.btn_pet, self.btn_service,
                    self.btn_product, self.btn_appointment, self.btn_invoice, self.btn_statistics]:
            self.sidebarLayout.addWidget(btn)

        self.sidebarLayout.addStretch()
        self.mainLayout.addWidget(self.sidebar)

        # Stacked widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.mainLayout.addWidget(self.stacked_widget, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
