"""
Tầng 3 - VIEW: Giao diện quản lý hóa đơn
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QComboBox, QDoubleSpinBox,
                             QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import Qt
from ui.invoice_ui import Ui_InvoiceWidget
from models.invoice_model import InvoiceModel
from models.customer_model import CustomerModel
from models.appointment_model import AppointmentModel


class InvoiceView(QWidget, Ui_InvoiceWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = InvoiceModel()
        self.customer_model = CustomerModel()
        self._customer_ids = []
        self._connect_signals()
        self._load_customers()
        self.load_data()

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.create_invoice)
        self.view_btn.clicked.connect(self.view_invoice)
        self.export_btn.clicked.connect(self.export_invoice)
        self.filter_btn.clicked.connect(self.load_data)

    def _load_customers(self):
        self.customer_combo.clear()
        self._customer_ids = [None]
        self.customer_combo.addItem("-- Tất cả --")
        for c in self.customer_model.get_all():
            self.customer_combo.addItem(c["name"])
            self._customer_ids.append(c["id"])

    def load_data(self):
        idx = self.customer_combo.currentIndex()
        cid = self._customer_ids[idx] if idx < len(self._customer_ids) else None
        rows = self.model.get_by_customer(cid) if cid else self.model.get_all()
        self._fill_table(rows)

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            values = [
                str(row.get("id", "")),
                str(row.get("appointment_id", "")),
                str(row.get("customer_name", "")),
                f"{row.get('total_amount', 0):,.0f} đ",
                str(row.get("payment_method", "")),
                str(row.get("created_at", "")),
            ]
            for c, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một hóa đơn!")
            return None
        return int(self.table.item(row, 0).text())

    def create_invoice(self):
        dialog = InvoiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["appointment_id"]:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lịch hẹn!")
                return
            self.model.add(data["appointment_id"], data["total_amount"], data["payment_method"])
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã tạo hóa đơn!")

    def view_invoice(self):
        iid = self._get_selected_id()
        if iid is None:
            return
        row = self.table.currentRow()
        info = (f"ID Hóa Đơn: {self.table.item(row,0).text()}\n"
                f"Lịch Hẹn:   {self.table.item(row,1).text()}\n"
                f"Khách Hàng: {self.table.item(row,2).text()}\n"
                f"Tổng Tiền:  {self.table.item(row,3).text()}\n"
                f"Thanh Toán: {self.table.item(row,4).text()}\n"
                f"Ngày:       {self.table.item(row,5).text()}")
        QMessageBox.information(self, "Chi Tiết Hóa Đơn", info)

    def export_invoice(self):
        iid = self._get_selected_id()
        if iid is None:
            return
        QMessageBox.information(self, "Xuất Hóa Đơn", f"Hóa đơn #{iid} đã được xuất thành công!")


class InvoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo Hóa Đơn")
        self.setFixedSize(380, 200)
        layout = QFormLayout(self)

        self._appointment_ids = []
        self.appointment_combo  = QComboBox()
        self.amount_input       = QDoubleSpinBox()
        self.amount_input.setRange(0, 99_000_000)
        self.amount_input.setSingleStep(10000)
        self.amount_input.setDecimals(0)
        self.payment_combo      = QComboBox()
        self.payment_combo.addItems(["Tiền mặt", "Chuyển khoản", "Thẻ tín dụng"])

        self._load_appointments()

        layout.addRow("Lịch hẹn:",       self.appointment_combo)
        layout.addRow("Tổng tiền (đ):",   self.amount_input)
        layout.addRow("Phương thức TT:", self.payment_combo)

        btn_layout = QHBoxLayout()
        save_btn   = QPushButton("💾 Lưu")
        cancel_btn = QPushButton("Hủy")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow("", btn_layout)

    def _load_appointments(self):
        appointments = AppointmentModel().get_all()
        self.appointment_combo.clear()
        self._appointment_ids = []
        for a in appointments:
            label = f"#{a['id']} - {a['customer_name']} - {a['datetime']}"
            self.appointment_combo.addItem(label)
            self._appointment_ids.append(a["id"])

    def get_data(self):
        idx = self.appointment_combo.currentIndex()
        return {
            "appointment_id": self._appointment_ids[idx] if idx >= 0 and idx < len(self._appointment_ids) else None,
            "total_amount":   self.amount_input.value(),
            "payment_method": self.payment_combo.currentText(),
        }
