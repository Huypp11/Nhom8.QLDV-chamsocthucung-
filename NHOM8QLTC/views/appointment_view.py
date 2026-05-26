"""
Tầng 3 - VIEW: Giao diện quản lý lịch hẹn
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QLineEdit, QComboBox,
                             QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem,
                             QDateTimeEdit)
from PyQt5.QtCore import Qt, QDateTime
from ui.appointment_ui import Ui_AppointmentWidget
from controllers.appointment_controller import AppointmentController


class AppointmentView(QWidget, Ui_AppointmentWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = AppointmentController()
        self._connect_signals()
        self.load_data()

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.add_appointment)
        self.edit_btn.clicked.connect(self.edit_appointment)
        self.complete_btn.clicked.connect(self.complete_appointment)
        self.cancel_btn.clicked.connect(self.cancel_appointment)
        self.filter_btn.clicked.connect(self.load_data)

    def load_data(self):
        date_from = self.date_from.date().toString("yyyy-MM-dd")
        date_to   = self.date_to.date().toString("yyyy-MM-dd")
        rows = self.controller.get_by_date_range(date_from, date_to)
        self._fill_table(rows)

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, key in enumerate(["id", "customer_name", "pet_name",
                                      "service_name", "datetime", "status", "note"]):
                item = QTableWidgetItem(str(row.get(key, "") or ""))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một lịch hẹn!")
            return None
        return int(self.table.item(row, 0).text())

    def add_appointment(self):
        dialog = AppointmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not all([data["customer_id"], data["pet_id"], data["service_id"]]):
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ thông tin!")
                return
            ok, message = self.controller.add(data)
            if not ok:
                QMessageBox.warning(self, "Loi", message)
                return
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã đặt lịch hẹn!")

    def edit_appointment(self):
        aid = self._get_selected_id()
        if aid is None:
            return
        QMessageBox.information(self, "Thông báo", f"Chỉnh sửa lịch hẹn ID: {aid}")

    def complete_appointment(self):
        aid = self._get_selected_id()
        if aid is None:
            return
        self.controller.complete(aid)
        self.load_data()
        QMessageBox.information(self, "Thành công", "Đã đánh dấu hoàn thành!")

    def cancel_appointment(self):
        aid = self._get_selected_id()
        if aid is None:
            return
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn hủy lịch hẹn này?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.cancel(aid)
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã hủy lịch hẹn!")


class AppointmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đặt Lịch Hẹn")
        self.setFixedSize(400, 280)
        layout = QFormLayout(self)

        self._customer_ids = []
        self._pet_ids = []
        self._service_ids = []

        self.customer_combo = QComboBox()
        self.pet_combo      = QComboBox()
        self.service_combo  = QComboBox()
        self.datetime_edit  = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.note_input = QLineEdit()

        self._load_customers()
        self.customer_combo.currentIndexChanged.connect(self._load_pets)

        layout.addRow("Khách hàng:", self.customer_combo)
        layout.addRow("Thú cưng:",   self.pet_combo)
        layout.addRow("Dịch vụ:",    self.service_combo)
        layout.addRow("Ngày giờ:",   self.datetime_edit)
        layout.addRow("Ghi chú:",    self.note_input)

        btn_layout = QHBoxLayout()
        save_btn   = QPushButton("💾 Lưu")
        cancel_btn = QPushButton("Hủy")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow("", btn_layout)

    def _load_customers(self):
        customers = AppointmentController().get_customers()
        self.customer_combo.clear()
        self._customer_ids = []
        for c in customers:
            self.customer_combo.addItem(c["name"])
            self._customer_ids.append(c["id"])
        self._load_pets()
        self._load_services()

    def _load_pets(self):
        idx = self.customer_combo.currentIndex()
        self.pet_combo.clear()
        self._pet_ids = []
        if idx < 0 or idx >= len(self._customer_ids):
            return
        pets = AppointmentController().get_pets_by_customer(self._customer_ids[idx])
        for p in pets:
            self.pet_combo.addItem(p["name"])
            self._pet_ids.append(p["id"])

    def _load_services(self):
        services = AppointmentController().get_services()
        self.service_combo.clear()
        self._service_ids = []
        for s in services:
            self.service_combo.addItem(s["name"])
            self._service_ids.append(s["id"])

    def get_data(self):
        ci = self.customer_combo.currentIndex()
        pi = self.pet_combo.currentIndex()
        si = self.service_combo.currentIndex()
        return {
            "customer_id": self._customer_ids[ci] if ci >= 0 and ci < len(self._customer_ids) else None,
            "pet_id":      self._pet_ids[pi]      if pi >= 0 and pi < len(self._pet_ids)      else None,
            "service_id":  self._service_ids[si]  if si >= 0 and si < len(self._service_ids)  else None,
            "datetime":    self.datetime_edit.dateTime().toString("yyyy-MM-dd HH:mm"),
            "note":        self.note_input.text().strip(),
        }
