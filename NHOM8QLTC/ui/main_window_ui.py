# -*- coding: utf-8 -*-
# File duoc tao tu main_window.ui - KHONG CHINH SUA FILE NAY

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 700)
        MainWindow.setWindowTitle("Quản Lý Dịch Vụ Chăm Sóc Thú Cưng")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Sidebar
        self.sidebar = QtWidgets.QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMaximumWidth(180)
        self.sidebar.setMinimumWidth(160)
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(12, 14, 12, 14)
        self.sidebarLayout.setSpacing(8)

        self.titleLabel = QtWidgets.QLabel("QUẢN LÝ DỊCH VỤ\nCHĂM SÓC THÚ CƯNG")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(11)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.sidebarLayout.addWidget(self.titleLabel)

        # Sidebar buttons
        self.btn_customer = QtWidgets.QPushButton("Khách Hàng")
        self.btn_customer.setMinimumHeight(40)
        self.btn_pet = QtWidgets.QPushButton("Thú Cưng")
        self.btn_pet.setMinimumHeight(40)
        self.btn_service = QtWidgets.QPushButton("Dịch Vụ")
        self.btn_service.setMinimumHeight(40)
        self.btn_product = QtWidgets.QPushButton("Sản Phẩm")
        self.btn_product.setMinimumHeight(40)
        self.btn_appointment = QtWidgets.QPushButton("Lịch Hẹn")
        self.btn_appointment.setMinimumHeight(40)
        self.btn_invoice = QtWidgets.QPushButton("Thanh Toán")
        self.btn_invoice.setMinimumHeight(40)
        self.btn_statistics = QtWidgets.QPushButton("Thống Kê")
        self.btn_statistics.setMinimumHeight(40)
        self.btn_user = QtWidgets.QPushButton("Tài Khoản")
        self.btn_user.setMinimumHeight(40)
        self.btn_logout = QtWidgets.QPushButton("Đăng Xuất")
        self.btn_logout.setObjectName("logoutButton")
        self.btn_logout.setMinimumHeight(40)

        for btn in [
            self.btn_customer,
            self.btn_pet,
            self.btn_service,
            self.btn_product,
            self.btn_appointment,
            self.btn_invoice,
            self.btn_statistics,
            self.btn_user,
        ]:
            self.sidebarLayout.addWidget(btn)

        self.sidebarLayout.addStretch()
        self.userLabel = QtWidgets.QLabel("")
        self.userLabel.setObjectName("userLabel")
        self.userLabel.setWordWrap(True)
        self.userLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebarLayout.addWidget(self.userLabel)
        self.sidebarLayout.addWidget(self.btn_logout)
        self.mainLayout.addWidget(self.sidebar)

        # Stacked widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.mainLayout.addWidget(self.stacked_widget, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setStyleSheet("""
            QMainWindow {
                background: #f4f7fb;
            }
            QWidget#centralwidget {
                background: #f4f7fb;
            }
            QWidget#sidebar {
                background: #243447;
                border-right: 1px solid #1b2838;
            }
            QLabel#titleLabel {
                color: #ffffff;
                padding: 10px 6px 16px 6px;
            }
            QWidget#sidebar QPushButton {
                background: #eef3f8;
                color: #1f2937;
                border: none;
                border-radius: 6px;
                padding: 8px 10px;
                text-align: left;
                font-weight: 600;
            }
            QWidget#sidebar QPushButton:hover {
                background: #dbe7f3;
            }
            QWidget#sidebar QPushButton:pressed {
                background: #c8d8ea;
            }
            QWidget#sidebar QPushButton#logoutButton {
                background: #ef4444;
                color: white;
                text-align: center;
            }
            QWidget#sidebar QPushButton#logoutButton:hover {
                background: #dc2626;
            }
            QLabel#userLabel {
                color: #dbeafe;
                background: #1d2a3a;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QStackedWidget {
                background: white;
                border-left: 1px solid #e5e7eb;
            }
            QStatusBar {
                background: #ffffff;
                color: #374151;
                border-top: 1px solid #e5e7eb;
            }
        """)
