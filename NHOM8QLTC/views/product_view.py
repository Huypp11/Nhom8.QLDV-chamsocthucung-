"""
Tầng 3 - VIEW: Giao diện quản lý sản phẩm
"""
from PyQt5.QtWidgets import (QWidget, QDialog, QFormLayout, QComboBox, QLineEdit,
                             QDoubleSpinBox, QSpinBox, QPushButton, QHBoxLayout,
                             QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
                             QMessageBox, QAbstractItemView, QHeaderView)
from PyQt5.QtCore import Qt
from models.product_model import ProductModel

CATEGORIES = ["Sữa tắm", "Thức ăn", "Phụ kiện", "Đồ chơi", "Khác"]


class ProductView(QWidget):
    def __init__(self):
        super().__init__()
        self.model = ProductModel()
        self._setup_ui()
        self._connect_signals()
        self.load_data()

    # ------------------------------------------------------------------ UI --
    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # --- Tiêu đề ---
        title = QLabel("QUẢN LÝ SẢN PHẨM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:16px; font-weight:bold; padding:8px;")
        layout.addWidget(title)

        # --- Thanh tìm kiếm ---
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Tìm kiếm sản phẩm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên sản phẩm...")
        self.search_input.setMinimumWidth(300)
        self.search_btn = QPushButton("Tìm kiếm")
        self.reset_btn  = QPushButton("Làm Mới")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.reset_btn)
        search_layout.addStretch()
        layout.addLayout(search_layout)

        # --- Nút thao tác ---
        btn_layout = QHBoxLayout()
        self.add_btn  = QPushButton("➕ Thêm Sản Phẩm")
        self.edit_btn = QPushButton("✏️ Chỉnh Sửa")
        self.del_btn  = QPushButton("🗑️ Xóa")
        for btn in [self.add_btn, self.edit_btn, self.del_btn]:
            btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # --- Bảng ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên Sản Phẩm", "Mô Tả", "Giá (VNĐ)", "Danh Mục", "Tồn Kho"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

    def _connect_signals(self):
        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn.clicked.connect(self.edit_product)
        self.del_btn.clicked.connect(self.delete_product)
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(self.load_data)
        self.search_input.returnPressed.connect(self.search)

    # --------------------------------------------------------------- Data --
    def load_data(self):
        self.search_input.clear()
        self._fill_table(self.model.get_all())

    def search(self):
        kw = self.search_input.text().strip()
        self._fill_table(self.model.search(kw) if kw else self.model.get_all())

    def _fill_table(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            values = [
                str(row.get("id", "")),
                str(row.get("name", "")),
                str(row.get("description", "")),
                f"{row.get('price', 0):,.0f}",
                str(row.get("category", "")),
                str(row.get("stock", 0)),
            ]
            for c, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn một sản phẩm!")
            return None
        return int(self.table.item(row, 0).text())

    # ------------------------------------------------------------ Actions --
    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            d = dialog.get_data()
            if not d["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên sản phẩm không được để trống!")
                return
            self.model.add(d["name"], d["description"], d["price"], d["category"], d["stock"])
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã thêm sản phẩm!")

    def edit_product(self):
        pid = self._get_selected_id()
        if pid is None:
            return
        product = self.model.get_by_id(pid)
        if not product:
            return
        dialog = ProductDialog(self, product)
        if dialog.exec_() == QDialog.Accepted:
            d = dialog.get_data()
            self.model.update(pid, d["name"], d["description"], d["price"], d["category"], d["stock"])
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã cập nhật sản phẩm!")

    def delete_product(self):
        pid = self._get_selected_id()
        if pid is None:
            return
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa sản phẩm này?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.model.delete(pid)
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã xóa sản phẩm!")


# ------------------------------------------------------------------ Dialog --
class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Sản Phẩm" if product is None else "Chỉnh Sửa Sản Phẩm")
        self.setFixedSize(400, 280)
        layout = QFormLayout(self)

        self.name_input  = QLineEdit()
        self.desc_input  = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 99_000_000)
        self.price_input.setSingleStep(1000)
        self.price_input.setDecimals(0)
        self.cat_combo   = QComboBox()
        self.cat_combo.addItems(CATEGORIES)
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 99999)

        if product:
            self.name_input.setText(product.get("name", ""))
            self.desc_input.setText(product.get("description", ""))
            self.price_input.setValue(product.get("price", 0))
            idx = self.cat_combo.findText(product.get("category", ""))
            if idx >= 0:
                self.cat_combo.setCurrentIndex(idx)
            self.stock_input.setValue(product.get("stock", 0))

        layout.addRow("Tên sản phẩm *:", self.name_input)
        layout.addRow("Mô tả:",          self.desc_input)
        layout.addRow("Giá (VNĐ):",      self.price_input)
        layout.addRow("Danh mục:",        self.cat_combo)
        layout.addRow("Tồn kho:",         self.stock_input)

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
            "category":    self.cat_combo.currentText(),
            "stock":       self.stock_input.value(),
        }