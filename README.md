#  Hệ Thống Quản Lý Cửa Hàng Chăm Sóc Thú Cưng

##  Giới thiệu

Đây là ứng dụng quản lý cửa hàng chăm sóc thú cưng được xây dựng bằng Python (PyQt5).
Hệ thống hỗ trợ quản lý khách hàng, thú cưng, dịch vụ, lịch hẹn và hóa đơn.

---

##  Chức năng chính

###  Quản lý khách hàng

* Thêm / sửa / xóa khách hàng
* Tìm kiếm khách hàng
* Làm mới khách hàng
###  Quản lý thú cưng
* Sửa ,xóa tìm kiếm thú cưng
* Thêm thú cưng theo khách hàng
* Quản lý thông tin thú cưng (tên, loại, tuổi...)

###  Quản lý dịch vụ
*Thêm ,sửa ,xóa ,,tìm kiếm làm mới dịch vụ
* Danh sách dịch vụ (tắm, cắt tỉa, khám bệnh...)
* Giá dịch vụ

###  Quản lý lịch hẹn
* Lọc theo ngày tháng
* Chỉnh sửa lịch hẹn
* Đặt lịch cho thú cưng
* Theo dõi trạng thái lịch

###  Quản lý hóa đơn

* Tạo hóa đơn
* Thanh toán
* Xuất hóa đơn

###  Thống kê

* Doanh thu tháng
* Số lượng khách hàng
* Số lượng thú cưng
* Tổng lịch hẹn
* Các dịch vụ
  
---

## Công nghệ sử dụng

* Python
* Vs code
* PyQt5 (GUI)
* SQLite  (Database)
* Qt Designer (thiết kế UI)

---

##  Cấu trúc thư mục

```
project/
│
├── ui/                # File giao diện (.ui)
├── gui/               # File convert từ UI
├── views/             # Xử lý giao diện
├── controllers/       # Xử lý logic
├── models/            # Database
├── main.py            # Chạy chương trình
```

---

## ⚙️ Cài đặt & chạy

### 1. Clone project

```
git clone https://github.com/Huypp11/Nhom9.QLDV-chamsocthucung-.git
```

### 2. Cài thư viện

```
pip install PyQt5
```

### 3. Convert UI

```
pyuic5 ui/customer.ui -o gui/customer_ui.py
```

### 4. Chạy chương trình

```
python main.py
```

---

##  Kiến trúc hệ thống

Ứng dụng được xây dựng theo mô hình 3 lớp:

* **GUI (View):** giao diện người dùng
* **Controller:** xử lý logic
* **Model:** dữ liệu và database

---

##  Hướng phát triển

* Thêm đăng nhập / phân quyền
* Kết nối API
* Xuất báo cáo 
* Deploy thành phần mềm hoàn chỉnh



