"""
Tầng 3 - VIEW: Giao diện quản lý dịch vụ
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QLineEdit, QSpinBox,
                             QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem,
                             QDoubleSpinBox, QComboBox)
from PyQt5.QtCore import Qt
from ui.service_ui import Ui_ServiceWidget
from controllers.service_controller import ServiceController


class ServiceView(QWidget, Ui_ServiceWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = ServiceController()
        self._connect_signals()
        self.load_data()

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.add_service)
        self.edit_btn.clicked.connect(self.edit_service)
        self.delete_btn.clicked.connect(self.delete_service)
        self.refresh_btn.clicked.connect(self.load_data)
        self.search_btn.clicked.connect(self.search_services)
        self.search_input.returnPressed.connect(self.search_services)

    def load_data(self, data=None):
        rows = data if data is not None else self.controller.get_all()
        self._fill_table(rows)

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            values = [
                str(row.get("id", "")),
                str(row.get("name", "")),
                str(row.get("description", "") or ""),
                f"{row.get('price', 0):,.0f}",
                str(row.get("duration", "")),
                str(row.get("species_category", "") or "Tat ca"),
            ]
            for c, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def search_services(self):
        keyword = self.search_input.text().strip()
        self.load_data(self.controller.search(keyword))

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một dịch vụ!")
            return None
        return int(self.table.item(row, 0).text())

    def add_service(self):
        dialog = ServiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên dịch vụ không được để trống!")
                return
            ok, message = self.controller.add(data)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã thêm dịch vụ!")

    def edit_service(self):
        sid = self._get_selected_id()
        if sid is None:
            return
        row = self.table.currentRow()
        current = {
            "name":        self.table.item(row, 1).text(),
            "description": self.table.item(row, 2).text(),
            "price":       self.table.item(row, 3).text().replace(",", ""),
            "duration":    self.table.item(row, 4).text(),
            "species_category": self.table.item(row, 5).text(),
        }
        dialog = ServiceDialog(self, current)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            ok, message = self.controller.update(sid, data)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã cập nhật dịch vụ!")

    def delete_service(self):
        sid = self._get_selected_id()
        if sid is None:
            return
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa dịch vụ này?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.delete(sid)
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã xóa dịch vụ!")


class ServiceDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Dịch Vụ" if data is None else "Chỉnh Sửa Dịch Vụ")
        self.setFixedSize(380, 270)
        layout = QFormLayout(self)

        self.name_input = QLineEdit(data["name"] if data else "")
        self.desc_input = QLineEdit(data["description"] if data else "")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 99_000_000)
        self.price_input.setSingleStep(10000)
        self.price_input.setDecimals(0)
        if data:
            try:
                self.price_input.setValue(float(data["price"]))
            except (ValueError, TypeError):
                pass
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 480)
        self.duration_input.setValue(30)
        if data:
            try:
                self.duration_input.setValue(int(data["duration"]))
            except (ValueError, TypeError):
                pass
        self.species_input = QComboBox()
        self.species_input.addItems(["Tat ca", "Cho", "Meo", "Chim", "Ca", "Khac"])
        if data:
            species = data.get("species_category") or "Tat ca"
            idx = self.species_input.findText(species)
            if idx < 0:
                self.species_input.addItem(species)
                idx = self.species_input.findText(species)
            self.species_input.setCurrentIndex(idx)

        layout.addRow("Tên dịch vụ (*):", self.name_input)
        layout.addRow("Mô tả:",           self.desc_input)
        layout.addRow("Giá (VNĐ):",       self.price_input)
        layout.addRow("Thời gian (phút):", self.duration_input)
        layout.addRow("Loai thu cung:", self.species_input)

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
            "name":        self.name_input.text().strip(),
            "description": self.desc_input.text().strip(),
            "price":       self.price_input.value(),
            "duration":    self.duration_input.value(),
            "species_category": self.species_input.currentText(),
        }
