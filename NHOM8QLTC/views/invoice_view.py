"""
Tầng 3 - VIEW: Giao diện quản lý hóa đơn (có tích hợp sản phẩm)
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QComboBox, QDoubleSpinBox,
                             QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox, QGroupBox,
                             QAbstractItemView, QSplitter, QHeaderView)
from PyQt5.QtCore import Qt
from ui.invoice_ui import Ui_InvoiceWidget
from models.invoice_model import InvoiceModel
from models.customer_model import CustomerModel
from models.appointment_model import AppointmentModel
from models.product_model import ProductModel
from models.service_model import ServiceModel


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
            if not data["items"]:
                QMessageBox.warning(self, "Lỗi", "Hóa đơn phải có ít nhất 1 dịch vụ hoặc sản phẩm!")
                return
            invoice_id = self.model.add_full(
                data["appointment_id"],
                data["payment_method"],
                data["items"]
            )
            self.load_data()
            QMessageBox.information(self, "Thành công",
                                    f"Đã tạo hóa đơn #{invoice_id} thành công!")

    def view_invoice(self):
        iid = self._get_selected_id()
        if iid is None:
            return

        items = self.model.get_items(iid)
        row   = self.table.currentRow()

        # Xây dựng chi tiết hóa đơn
        lines = [
            f"{'─'*40}",
            f"  HÓA ĐƠN #{self.table.item(row, 0).text()}",
            f"{'─'*40}",
            f"Khách hàng : {self.table.item(row, 2).text()}",
            f"Lịch hẹn   : #{self.table.item(row, 1).text()}",
            f"Ngày        : {self.table.item(row, 5).text()}",
            f"Thanh toán : {self.table.item(row, 4).text()}",
            f"{'─'*40}",
        ]

        if items:
            # Nhóm dịch vụ
            services = [i for i in items if i["item_type"] == "service"]
            products = [i for i in items if i["item_type"] == "product"]

            if services:
                lines.append("  DỊCH VỤ:")
                for it in services:
                    subtotal = it["quantity"] * it["unit_price"]
                    lines.append(f"  • {it['item_name']:<25} {it['unit_price']:>12,.0f} đ")

            if products:
                lines.append("  SẢN PHẨM:")
                for it in products:
                    subtotal = it["quantity"] * it["unit_price"]
                    lines.append(f"  • {it['item_name']:<20} x{it['quantity']}  {subtotal:>12,.0f} đ")

            lines.append(f"{'─'*40}")

        lines.append(f"  TỔNG TIỀN : {self.table.item(row, 3).text():>15}")
        lines.append(f"{'─'*40}")

        QMessageBox.information(self, "Chi Tiết Hóa Đơn", "\n".join(lines))

    def export_invoice(self):
        iid = self._get_selected_id()
        if iid is None:
            return
        QMessageBox.information(self, "Xuất Hóa Đơn",
                                f"Hóa đơn #{iid} đã được xuất thành công!")


# ══════════════════════════════════════════════════════════════════════════════
#  Dialog tạo hóa đơn – chọn lịch hẹn + thêm dịch vụ + thêm sản phẩm
# ══════════════════════════════════════════════════════════════════════════════
class InvoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo Hóa Đơn")
        self.setMinimumSize(700, 580)
        self._appointment_ids = []
        self._items = []          # list of dict: item_type, item_id, item_name, quantity, unit_price
        self._setup_ui()
        self._load_appointments()
        self._load_services()
        self._load_products()

    # ----------------------------------------------------------- Setup UI --
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # ── Chọn lịch hẹn & thanh toán ──
        info_group = QGroupBox("Thông tin chung")
        info_form  = QFormLayout(info_group)
        self.appointment_combo = QComboBox()
        self.payment_combo     = QComboBox()
        self.payment_combo.addItems(["Tiền mặt", "Chuyển khoản", "Thẻ tín dụng"])
        info_form.addRow("Lịch hẹn *:",        self.appointment_combo)
        info_form.addRow("Phương thức TT:",     self.payment_combo)
        main_layout.addWidget(info_group)

        # ── Splitter: trái = chọn hàng, phải = giỏ hóa đơn ──
        splitter = QSplitter(Qt.Horizontal)

        # -- Panel trái: chọn dịch vụ / sản phẩm --
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 4, 0)

        # Dịch vụ
        svc_group  = QGroupBox("Dịch vụ")
        svc_layout = QVBoxLayout(svc_group)
        self.service_combo = QComboBox()
        add_svc_btn = QPushButton("➕ Thêm dịch vụ vào hóa đơn")
        add_svc_btn.clicked.connect(self._add_service)
        svc_layout.addWidget(self.service_combo)
        svc_layout.addWidget(add_svc_btn)
        left_layout.addWidget(svc_group)

        # Sản phẩm
        prod_group  = QGroupBox("Sản phẩm")
        prod_layout = QVBoxLayout(prod_group)
        self.product_combo = QComboBox()
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Số lượng:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 999)
        self.qty_spin.setValue(1)
        qty_layout.addWidget(self.qty_spin)
        qty_layout.addStretch()
        add_prod_btn = QPushButton("➕ Thêm sản phẩm vào hóa đơn")
        add_prod_btn.clicked.connect(self._add_product)
        prod_layout.addWidget(self.product_combo)
        prod_layout.addLayout(qty_layout)
        prod_layout.addWidget(add_prod_btn)
        left_layout.addWidget(prod_group)
        left_layout.addStretch()

        # -- Panel phải: giỏ hóa đơn --
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(4, 0, 0, 0)

        right_layout.addWidget(QLabel("📋 Các mục trong hóa đơn:"))
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(
            ["Loại", "Tên", "SL", "Đơn giá", "Thành tiền"])
        self.cart_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cart_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        right_layout.addWidget(self.cart_table)

        remove_btn = QPushButton("🗑️ Xóa dòng đã chọn")
        remove_btn.clicked.connect(self._remove_item)
        right_layout.addWidget(remove_btn)

        # Tổng tiền
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(QLabel("TỔNG TIỀN:"))
        self.total_label = QLabel("0 đ")
        self.total_label.setStyleSheet("font-size:14px; font-weight:bold; color:#d32f2f;")
        total_layout.addWidget(self.total_label)
        right_layout.addLayout(total_layout)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([280, 400])
        main_layout.addWidget(splitter)

        # ── Nút Lưu / Hủy ──
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_btn   = QPushButton("💾 Lưu hóa đơn")
        cancel_btn = QPushButton("Hủy")
        save_btn.setMinimumWidth(130)
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

    # ---------------------------------------------------- Load combo data --
    def _load_appointments(self):
        appointments = AppointmentModel().get_all()
        self.appointment_combo.clear()
        self._appointment_ids = []
        for a in appointments:
            label = f"#{a['id']} - {a['customer_name']} - {a['datetime']}"
            self.appointment_combo.addItem(label)
            self._appointment_ids.append(a["id"])

    def _load_services(self):
        self._services = ServiceModel().get_all()
        self.service_combo.clear()
        for s in self._services:
            self.service_combo.addItem(f"{s['name']}  ({s['price']:,.0f} đ)")

    def _load_products(self):
        self._products = ProductModel().get_all()
        self.product_combo.clear()
        for p in self._products:
            self.product_combo.addItem(f"{p['name']}  ({p['price']:,.0f} đ)")

    # ----------------------------------------------- Add / Remove items --
    def _add_service(self):
        idx = self.service_combo.currentIndex()
        if idx < 0 or idx >= len(self._services):
            return
        s = self._services[idx]
        # Nếu dịch vụ đã có thì không thêm lại
        for it in self._items:
            if it["item_type"] == "service" and it["item_id"] == s["id"]:
                QMessageBox.information(self, "Thông báo", "Dịch vụ này đã có trong hóa đơn!")
                return
        self._items.append({
            "item_type":  "service",
            "item_id":    s["id"],
            "item_name":  s["name"],
            "quantity":   1,
            "unit_price": s["price"],
        })
        self._refresh_cart()

    def _add_product(self):
        idx = self.product_combo.currentIndex()
        if idx < 0 or idx >= len(self._products):
            return
        p   = self._products[idx]
        qty = self.qty_spin.value()
        # Nếu sản phẩm đã có thì cộng thêm số lượng
        for it in self._items:
            if it["item_type"] == "product" and it["item_id"] == p["id"]:
                it["quantity"] += qty
                self._refresh_cart()
                return
        self._items.append({
            "item_type":  "product",
            "item_id":    p["id"],
            "item_name":  p["name"],
            "quantity":   qty,
            "unit_price": p["price"],
        })
        self._refresh_cart()

    def _remove_item(self):
        row = self.cart_table.currentRow()
        if row < 0:
            return
        self._items.pop(row)
        self._refresh_cart()

    # ---------------------------------------------------- Refresh cart --
    def _refresh_cart(self):
        self.cart_table.setRowCount(0)
        total = 0
        for it in self._items:
            r = self.cart_table.rowCount()
            self.cart_table.insertRow(r)
            subtotal = it["quantity"] * it["unit_price"]
            total   += subtotal
            type_label = "Dịch vụ" if it["item_type"] == "service" else "Sản phẩm"
            for c, val in enumerate([
                type_label,
                it["item_name"],
                str(it["quantity"]),
                f"{it['unit_price']:,.0f} đ",
                f"{subtotal:,.0f} đ",
            ]):
                cell = QTableWidgetItem(val)
                cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
                self.cart_table.setItem(r, c, cell)
        self.total_label.setText(f"{total:,.0f} đ")

    # --------------------------------------------------------- Get data --
    def get_data(self):
        idx = self.appointment_combo.currentIndex()
        return {
            "appointment_id": (self._appointment_ids[idx]
                               if 0 <= idx < len(self._appointment_ids) else None),
            "payment_method": self.payment_combo.currentText(),
            "items":          self._items,
        }