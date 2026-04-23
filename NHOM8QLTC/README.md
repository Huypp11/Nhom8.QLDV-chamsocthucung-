# 🐾 Quản Lý Cửa Hàng Chăm Sóc Thú Cưng

## Cấu trúc dự án (Mô hình 3 tầng)

```
NHOM8QLTC/
│
├── main.py                        ← Chạy ứng dụng tại đây
│
├── database/                      ← TẦNG 1: Kết nối & khởi tạo DB
│   ├── db_manager.py
│   └── pet_shop.db                (tự tạo khi chạy lần đầu)
│
├── models/                        ← TẦNG 2: Truy vấn SQL (CRUD)
│   ├── customer_model.py
│   ├── pet_model.py
│   ├── service_model.py
│   ├── appointment_model.py
│   └── invoice_model.py
│
├── views/                         ← TẦNG 3: Logic giao diện
│   ├── customer_view.py
│   ├── pet_view.py
│   ├── service_view.py
│   ├── appointment_view.py
│   ├── invoice_view.py
│   └── statistics_view.py
│
└── ui/                            ← File convert từ .ui (KHÔNG SỬA)
    ├── main_window_ui.py
    ├── customer_ui.py
    ├── pet_ui.py
    ├── service_ui.py
    ├── appointment_ui.py
    ├── invoice_ui.py
    └── statistics_ui.py
```

## Cài đặt & Chạy

```bash
# 1. Cài thư viện
pip install PyQt5

# 2. Chạy ứng dụng
python main.py
```

## Luồng dữ liệu (3 tầng)

```
[Người dùng click nút]
        ↓
  views/xxx_view.py        ← Tầng 3: Xử lý sự kiện UI
        ↓
  models/xxx_model.py      ← Tầng 2: Truy vấn SQL
        ↓
  database/db_manager.py   ← Tầng 1: Kết nối SQLite
        ↓
     pet_shop.db           ← Lưu trữ dữ liệu
```
