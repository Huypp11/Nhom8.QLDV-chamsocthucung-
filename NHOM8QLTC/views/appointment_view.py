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
        # Kết nối ô nhập tìm kiếm (Giả sử tên là txt_tim, ấn Enter để lọc ngay)
        try:
            self.txt_tim.returnPressed.connect(self.load_data)
        except AttributeError:
            pass # Bỏ qua nếu bạn lỡ đặt tên ô này khác 'txt_tim' trong Designer

    def load_data(self):
        keyword = ""

        try:
         keyword = self.txt_tim.text().strip()
        except AttributeError:
            pass

    # Chưa nhập tìm kiếm -> hiện tất cả
        if keyword == "":
         rows = self.controller.get_all()

    # Có nhập -> lọc
        else:
         date_from = self.date_from.date().toString("yyyy-MM-dd")
         date_to = self.date_to.date().toString("yyyy-MM-dd")

         rows = self.controller.search(date_from, date_to, keyword)

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
        self.setFixedSize(430, 320)
        layout = QFormLayout(self)

        self._customer_ids = []
        self._customers = []
        self._pet_ids = []
        self._service_ids = []

        self.customer_search_input = QLineEdit()
        self.customer_search_input.setPlaceholderText("Tim theo ten hoac so dien thoai...")
        self.customer_combo = QComboBox()
        self.pet_combo      = QComboBox()
        self.service_combo  = QComboBox()
        self.datetime_edit  = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.note_input = QLineEdit()

        self._load_customers()
        self.customer_search_input.textChanged.connect(self._filter_customers)
        self.customer_combo.currentIndexChanged.connect(self._load_pets)
        layout.addRow("Tim khach:", self.customer_search_input)

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
        self._customers = AppointmentController().get_customers()
        self._fill_customer_combo(self._customers)
        self._load_services()

    def _fill_customer_combo(self, customers):
        current_index = self.customer_combo.currentIndex()
        current_customer_id = (
            self._customer_ids[current_index]
            if 0 <= current_index < len(self._customer_ids)
            else None
        )
        self.customer_combo.blockSignals(True)
        self.customer_combo.clear()
        self._customer_ids = []
        for c in customers:
            phone = c.get("phone") or "Chua co SDT"
            self.customer_combo.addItem(f"{c['name']} - {phone}")
            self._customer_ids.append(c["id"])
        if current_customer_id in self._customer_ids:
            self.customer_combo.setCurrentIndex(self._customer_ids.index(current_customer_id))
        self.customer_combo.blockSignals(False)
        self._load_pets()

    def _filter_customers(self):
        keyword = self.customer_search_input.text().strip().lower()
        if keyword:
            customers = [
                c for c in self._customers
                if keyword in (c.get("name") or "").lower()
                or keyword in (c.get("phone") or "").lower()
            ]
        else:
            customers = self._customers
        self._fill_customer_combo(customers)

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
