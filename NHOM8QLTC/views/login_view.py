"""
Tầng 3 - VIEW: Màn hình đăng nhập và đăng ký
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models.user_model import UserModel


class LoginDialog(QDialog):
    """
    Màn hình đăng nhập và đăng ký — hiện ra trước MainWindow.
    Sau khi login thành công, self.current_user chứa thông tin user.
    """

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.model = UserModel()
        self._setup_ui()

    # ----------------------------------------------------------------- UI --
    def _setup_ui(self):
        self.setWindowTitle("Đăng Nhập / Đăng Ký")
        self.setFixedSize(560, 600)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ── Header ──────────────────────────────────────────────────────────
        header = QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet("background-color: #2c7be5;")
        header_layout = QVBoxLayout(header)

        title = QLabel("🐾 PET SHOP")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white;")

        subtitle = QLabel("Quản Lý Dịch Vụ Chăm Sóc Thú Cưng")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255,255,255,0.88); font-size: 14px;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header)

        # ── Tab Widget ───────────────────────────────────────────────────────
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab {
                background: #f0f0f0;
                padding: 12px 34px;
                font-size: 14px;
                border: none;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2c7be5;
                color: #2c7be5;
                font-weight: bold;
            }
        """)

        # TAB 1: ĐĂNG NHẬP
        login_frame = QFrame()
        login_frame.setStyleSheet("background: white;")
        login_layout = QVBoxLayout(login_frame)
        login_layout.setContentsMargins(70, 36, 70, 36)
        login_layout.setSpacing(16)

        login_layout.addWidget(self._label("Tên đăng nhập"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tên đăng nhập...")
        self.username_input.setFixedHeight(44)
        self._style_input(self.username_input)
        login_layout.addWidget(self.username_input)

        login_layout.addWidget(self._label("Mật khẩu"))
        pwd_row = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu...")
        self.password_input.setFixedHeight(44)
        self.password_input.setEchoMode(QLineEdit.Password)
        self._style_input(self.password_input)

        self.show_pwd_btn = QPushButton("👁")
        self.show_pwd_btn.setFixedSize(44, 44)
        self.show_pwd_btn.setCheckable(True)
        self.show_pwd_btn.setStyleSheet(
            "QPushButton { border: 1px solid #ced4da; border-radius: 4px; background: #f8f9fa; }"
            "QPushButton:checked { background: #e2e8f0; }"
        )
        self.show_pwd_btn.toggled.connect(self._toggle_password)

        pwd_row.addWidget(self.password_input)
        pwd_row.addWidget(self.show_pwd_btn)
        login_layout.addLayout(pwd_row)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53e3e; font-size: 11px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(self.error_label)

        self.login_btn = QPushButton("Đăng Nhập")
        self.login_btn.setFixedHeight(46)
        self.login_btn.setStyleSheet(self._button_style())
        self.login_btn.clicked.connect(self._do_login)
        login_layout.addWidget(self.login_btn)
        login_layout.addStretch()

        # TAB 2: ĐĂNG KÝ
        register_frame = QFrame()
        register_frame.setStyleSheet("background: white;")
        register_layout = QVBoxLayout(register_frame)
        register_layout.setContentsMargins(70, 28, 70, 28)
        register_layout.setSpacing(12)

        register_layout.addWidget(self._label("Họ tên"))
        self.reg_fullname = QLineEdit()
        self.reg_fullname.setPlaceholderText("Nhập họ và tên...")
        self.reg_fullname.setFixedHeight(42)
        self._style_input(self.reg_fullname)
        register_layout.addWidget(self.reg_fullname)

        register_layout.addWidget(self._label("Tên đăng nhập"))
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Chọn tên đăng nhập...")
        self.reg_username.setFixedHeight(42)
        self._style_input(self.reg_username)
        register_layout.addWidget(self.reg_username)

        register_layout.addWidget(self._label("Mật khẩu"))
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Nhập mật khẩu...")
        self.reg_password.setFixedHeight(42)
        self.reg_password.setEchoMode(QLineEdit.Password)
        self._style_input(self.reg_password)
        register_layout.addWidget(self.reg_password)

        register_layout.addWidget(self._label("Xác nhận mật khẩu"))
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setPlaceholderText("Xác nhận mật khẩu...")
        self.reg_confirm.setFixedHeight(42)
        self.reg_confirm.setEchoMode(QLineEdit.Password)
        self._style_input(self.reg_confirm)
        register_layout.addWidget(self.reg_confirm)

        self.reg_error_label = QLabel("")
        self.reg_error_label.setStyleSheet("color: #e53e3e; font-size: 11px;")
        self.reg_error_label.setAlignment(Qt.AlignCenter)
        register_layout.addWidget(self.reg_error_label)

        self.register_btn = QPushButton("Đăng Ký")
        self.register_btn.setFixedHeight(46)
        self.register_btn.setStyleSheet(self._button_style())
        self.register_btn.clicked.connect(self._do_register)
        register_layout.addWidget(self.register_btn)
        register_layout.addStretch()

        tabs.addTab(login_frame, "Đăng Nhập")
        tabs.addTab(register_frame, "Đăng Ký")

        main_layout.addWidget(tabs)

        # Enter để đăng nhập
        self.username_input.returnPressed.connect(self._do_login)
        self.password_input.returnPressed.connect(self._do_login)

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #4a5568;")
        return lbl

    def _style_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QLineEdit:focus { border-color: #2c7be5; }
        """)

    def _button_style(self):
        return """
            QPushButton {
                background-color: #2c7be5;
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1a68d1; }
            QPushButton:pressed { background-color: #1558b0; }
        """

    def _toggle_password(self, checked):
        self.password_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password)

    def closeEvent(self, event):
        self.reject()
        event.accept()

    # -------------------------------------------------------------- Logic --
    def _do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.error_label.setText("⚠ Vui lòng nhập đầy đủ thông tin!")
            return

        user = self.model.login(username, password)
        if user:
            self.current_user = user
            self.accept()
        else:
            self.error_label.setText("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
            self.password_input.clear()
            self.password_input.setFocus()

    def _do_register(self):
        fullname = self.reg_fullname.text().strip()
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()

        # Kiểm tra dữ liệu
        if not fullname or not username or not password or not confirm:
            self.reg_error_label.setText("⚠ Vui lòng nhập đầy đủ thông tin!")
            return

        if password != confirm:
            self.reg_error_label.setText("❌ Mật khẩu không khớp!")
            return

        if len(password) < 6:
            self.reg_error_label.setText("❌ Mật khẩu phải ít nhất 6 ký tự!")
            return

        # Thêm tài khoản mới
        success = self.model.add(username, password, fullname, "nhanvien")
        if success:
            QMessageBox.information(self, "Thành Công", 
                f" Đăng ký thành công!\n\nBạn có thể đăng nhập ngay bây giờ.")
            # Xóa form
            self.reg_fullname.clear()
            self.reg_username.clear()
            self.reg_password.clear()
            self.reg_confirm.clear()
            self.reg_error_label.setText("")
        else:
            self.reg_error_label.setText("❌ Tên đăng nhập đã tồn tại!")
