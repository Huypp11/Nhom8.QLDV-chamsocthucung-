"""
Tầng 3 - VIEW: Giao diện quản lý khách hàng
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QLineEdit,
                             QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import Qt
from ui.customer_ui import Ui_CustomerWidget
from controllers.customer_controller import CustomerController


class CustomerView(QWidget, Ui_CustomerWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = CustomerController()
        self.refresh_btn.setText("Làm mới")
        self._connect_signals()
        self.load_data()

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.add_customer)
        self.edit_btn.clicked.connect(self.edit_customer)
        self.delete_btn.clicked.connect(self.delete_customer)
        self.refresh_btn.clicked.connect(self.refresh_customers)
        self.search_btn.clicked.connect(self.search_customers)
        self.search_input.returnPressed.connect(self.search_customers)

    def load_data(self, data=None):
        rows = data if data is not None else self.controller.get_all()
        self._fill_table(rows)

    def refresh_customers(self):
        self.search_input.clear()
        self.load_data()
        self.table.clearSelection()

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, key in enumerate(["id", "name", "phone", "email", "address"]):
                item = QTableWidgetItem(str(row.get(key, "") or ""))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def search_customers(self):
        keyword = self.search_input.text().strip()
        if keyword:
            self.load_data(self.controller.search(keyword))
        else:
            self.load_data()

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một khách hàng!")
            return None
        return int(self.table.item(row, 0).text())

    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên không được để trống!")
                return
            ok, message = self.controller.add(data)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã thêm khách hàng!")

    def edit_customer(self):
        cid = self._get_selected_id()
        if cid is None:
            return
        customer = self.controller.get_by_id(cid)
        dialog = CustomerDialog(self, customer)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên không được để trống!")
                return
            ok, message = self.controller.update(cid, data)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã cập nhật khách hàng!")

    def delete_customer(self):
        cid = self._get_selected_id()
        if cid is None:
            return
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa khách hàng này?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.delete(cid)
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã xóa khách hàng!")


class CustomerDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Khách Hàng" if data is None else "Chỉnh Sửa Khách Hàng")
        self.setFixedSize(380, 240)
        layout = QFormLayout(self)

        self.name_input    = QLineEdit(data["name"]    if data else "")
        self.phone_input   = QLineEdit(data["phone"]   if data else "")
        self.email_input   = QLineEdit(data["email"]   if data else "")
        self.address_input = QLineEdit(data["address"] if data else "")

        layout.addRow("Tên (*):",          self.name_input)
        layout.addRow("Số điện thoại:",    self.phone_input)
        layout.addRow("Email:",            self.email_input)
        layout.addRow("Địa chỉ:",         self.address_input)

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
            "name":    self.name_input.text().strip(),
            "phone":   self.phone_input.text().strip(),
            "email":   self.email_input.text().strip(),
            "address": self.address_input.text().strip(),
        }
