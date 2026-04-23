"""
Tầng 3 - VIEW: Giao diện quản lý thú cưng
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QLineEdit, QSpinBox,
                             QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import Qt
from ui.pet_ui import Ui_PetWidget
from models.pet_model import PetModel
from models.customer_model import CustomerModel


class PetView(QWidget, Ui_PetWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = PetModel()
        self.customer_model = CustomerModel()
        self._customer_ids = []
        self._connect_signals()
        self.load_customers()

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.add_pet)
        self.edit_btn.clicked.connect(self.edit_pet)
        self.delete_btn.clicked.connect(self.delete_pet)
        self.customer_combo.currentIndexChanged.connect(self.load_pets)

    def load_customers(self):
        self.customer_combo.clear()
        self._customer_ids = []
        self.customer_combo.addItem("-- Tất cả --")
        self._customer_ids.append(None)
        customers = self.customer_model.get_all()
        for c in customers:
            self.customer_combo.addItem(c["name"])
            self._customer_ids.append(c["id"])

    def load_pets(self):
        idx = self.customer_combo.currentIndex()
        cid = self._customer_ids[idx] if idx < len(self._customer_ids) else None
        if cid:
            rows = self.model.get_by_customer(cid)
        else:
            rows = self.model.get_all()
        self._fill_table(rows)

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, key in enumerate(["id", "name", "species", "age", "breed", "created_at"]):
                item = QTableWidgetItem(str(row.get(key, "") or ""))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một thú cưng!")
            return None
        return int(self.table.item(row, 0).text())

    def _get_selected_customer_id(self):
        idx = self.customer_combo.currentIndex()
        cid = self._customer_ids[idx] if idx < len(self._customer_ids) else None
        if not cid:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn khách hàng trước!")
        return cid

    def add_pet(self):
        cid = self._get_selected_customer_id()
        if not cid:
            return
        dialog = PetDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên thú cưng không được để trống!")
                return
            self.model.add(cid, data["name"], data["species"], data["breed"], data["age"])
            self.load_pets()
            QMessageBox.information(self, "Thành công", "Đã thêm thú cưng!")

    def edit_pet(self):
        pid = self._get_selected_id()
        if pid is None:
            return
        row = self.table.currentRow()
        current = {
            "name":    self.table.item(row, 1).text(),
            "species": self.table.item(row, 2).text(),
            "age":     self.table.item(row, 3).text(),
            "breed":   self.table.item(row, 4).text(),
        }
        dialog = PetDialog(self, current)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.model.update(pid, data["name"], data["species"], data["breed"], data["age"])
            self.load_pets()
            QMessageBox.information(self, "Thành công", "Đã cập nhật thú cưng!")

    def delete_pet(self):
        pid = self._get_selected_id()
        if pid is None:
            return
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa thú cưng này?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.model.delete(pid)
            self.load_pets()
            QMessageBox.information(self, "Thành công", "Đã xóa thú cưng!")


class PetDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Thú Cưng" if data is None else "Chỉnh Sửa Thú Cưng")
        self.setFixedSize(360, 220)
        layout = QFormLayout(self)

        self.name_input    = QLineEdit(data["name"]    if data else "")
        self.species_input = QLineEdit(data["species"] if data else "")
        self.breed_input   = QLineEdit(data["breed"]   if data else "")
        self.age_input     = QSpinBox()
        self.age_input.setRange(0, 30)
        if data:
            try:
                self.age_input.setValue(int(data["age"]))
            except (ValueError, TypeError):
                pass

        layout.addRow("Tên (*):", self.name_input)
        layout.addRow("Loài:",    self.species_input)
        layout.addRow("Giống:",   self.breed_input)
        layout.addRow("Tuổi:",    self.age_input)

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
            "species": self.species_input.text().strip(),
            "breed":   self.breed_input.text().strip(),
            "age":     self.age_input.value(),
        }
