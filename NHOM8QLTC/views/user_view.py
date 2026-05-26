"""
Tầng 3 - VIEW: Giao diện quản lý tài khoản (chỉ Admin)
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QComboBox, QLineEdit,
                             QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QAbstractItemView, QGroupBox)
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController


class UserView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = UserController()
        self._setup_ui()
        self._connect_signals()
        self.load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("QUẢN LÝ TÀI KHOẢN")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:16px; font-weight:bold; padding:8px;")
        layout.addWidget(title)

        note = QLabel("⚠ Chỉ Admin mới có quyền quản lý tài khoản")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("color: #e53e3e; font-size: 11px; padding: 4px;")
        layout.addWidget(note)

        btn_layout = QHBoxLayout()
        self.add_btn  = QPushButton("➕ Thêm Tài Khoản")
        self.edit_btn = QPushButton("✏️ Đổi Mật Khẩu")
        self.del_btn  = QPushButton("🗑️ Xóa")
        for btn in [self.add_btn, self.edit_btn, self.del_btn]:
            btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên đăng nhập", "Họ tên", "Vai trò", "Ngày tạo"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.add_user)
        self.edit_btn.clicked.connect(self.change_password)
        self.del_btn.clicked.connect(self.delete_user)

    def load_data(self):
        self._fill_table(self.controller.get_all())

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            role_display = "👑 Admin" if row["role"] == "admin" else "👤 Nhân viên"
            values = [str(row["id"]), row["username"], row["full_name"],
                      role_display, str(row["created_at"])]
            for c, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một tài khoản!")
            return None
        return int(self.table.item(row, 0).text())

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            d = dialog.get_data()
            if not d["username"] or not d["password"] or not d["full_name"]:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            if self.controller.username_exists(d["username"]):
                QMessageBox.warning(self, "Lỗi", f"Tên đăng nhập '{d['username']}' đã tồn tại!")
                return
            ok, message = self.controller.add(d)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã tạo tài khoản!")

    def change_password(self):
        uid = self._get_selected_id()
        if uid is None:
            return
        dialog = ChangePasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_pwd = dialog.get_password()
            if not new_pwd:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu không được để trống!")
                return
            ok, message = self.controller.update_password(uid, new_pwd)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            QMessageBox.information(self, "Thành công", "Đã đổi mật khẩu!")

    def delete_user(self):
        uid = self._get_selected_id()
        if uid is None:
            return
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa tài khoản này?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            ok, message = self.controller.delete(uid)
            if ok:
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã xóa tài khoản!")
            else:
                QMessageBox.warning(self, "Không thể xóa",
                                    "Không thể xóa admin cuối cùng trong hệ thống!")


# ─────────────────────────────── Dialogs ─────────────────────────────────────

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Tài Khoản")
        self.setFixedSize(360, 240)
        layout = QFormLayout(self)

        self.username_input  = QLineEdit()
        self.fullname_input  = QLineEdit()
        self.password_input  = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_combo      = QComboBox()
        self.role_combo.addItems(["nhanvien", "admin"])

        layout.addRow("Tên đăng nhập *:", self.username_input)
        layout.addRow("Họ tên *:",        self.fullname_input)
        layout.addRow("Mật khẩu *:",      self.password_input)
        layout.addRow("Vai trò:",          self.role_combo)

        btn_layout = QHBoxLayout()
        save_btn   = QPushButton("💾 Lưu")
        cancel_btn = QPushButton("Hủy")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow("", btn_layout)

    def get_data(self):
        return {
            "username":  self.username_input.text().strip(),
            "full_name": self.fullname_input.text().strip(),
            "password":  self.password_input.text(),
            "role":      self.role_combo.currentText(),
        }


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đổi Mật Khẩu")
        self.setFixedSize(320, 140)
        layout = QFormLayout(self)

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd2_input = QLineEdit()
        self.pwd2_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Mật khẩu mới *:",    self.pwd_input)
        layout.addRow("Xác nhận mật khẩu:", self.pwd2_input)

        btn_layout = QHBoxLayout()
        save_btn   = QPushButton("💾 Lưu")
        cancel_btn = QPushButton("Hủy")
        save_btn.clicked.connect(self._validate)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow("", btn_layout)

    def _validate(self):
        if self.pwd_input.text() != self.pwd2_input.text():
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        self.accept()

    def get_password(self):
        return self.pwd_input.text()
