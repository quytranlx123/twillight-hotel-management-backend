🔄 Tài liệu đang trong quá trình cập nhật (14/6/2025)

# TwllightHotelManagement 🏨

Ứng dụng web quản lý khách sạn được xây dựng bằng **Django**, hỗ trợ các chức năng như quản lý phòng, đặt phòng, người dùng và hóa đơn.

---

## 📚 Mục lục

- [🚀 Giới thiệu](#-giới-thiệu)
- [🧩 Tính năng](#-tính-năng)
- [⚙️ Công nghệ](#-công-nghệ)
- [📁 Cấu trúc dự án](#-cấu-trúc-dự-án)
- [🛠️ Cài đặt & chạy](#️-cài-đặt--chạy)
- [📖 Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [🔐 Xác thực & phân quyền](#-xác-thực--phân-quyền)
- [📝 TODO / Định hướng mở rộng](#-todo--định-hướng-mở-rộng)
- [📜 License](#-license)
- [👤 Tác giả](#-tác-giả)

---

## 🚀 Giới thiệu

**TwllightHotelManagement** là hệ thống web đơn giản mô phỏng quy trình quản lý khách sạn. Ứng dụng hỗ trợ quản lý các thực thể như: phòng, khách hàng, hóa đơn, tài khoản người dùng, v.v… Dự án được xây dựng cá nhân nhằm luyện tập Django theo hướng fullstack.

---

## 🧩 Tính năng

- Quản lý phòng (CRUD)
- Quản lý loại phòng
- Đặt phòng và tạo hóa đơn
- Đăng nhập/đăng xuất, phân quyền user/admin
- Giao diện quản trị đơn giản bằng Django Admin và các template tùy chỉnh
- Sử dụng JWT cho các API bảo mật (nếu có)

---

## ⚙️ Công nghệ

| Thành phần     | Công nghệ sử dụng           |
|----------------|-----------------------------|
| Backend        | Python, Django               |
| Frontend       | Django Template / Bootstrap |
| CSDL           | SQLite (hoặc MySQL)         |
| API bảo mật    | Django REST Framework + JWT|
| IDE            | VS Code                     |
| Công cụ khác   | Postman (test API), Git     |

---

## 📁 Cấu trúc dự án

```
TwllightHotelManagement/
├── hotel_app/              # Ứng dụng chính
│   ├── models.py           # Các lớp dữ liệu: Room, Booking, User
│   ├── views.py            # Xử lý request
│   ├── forms.py            # Form cho các thực thể
│   ├── urls.py             # Điều hướng URL nội bộ
│   └── templates/          # Giao diện HTML
├── hotel_management/       # Cấu hình dự án Django
│   ├── settings.py
│   └── urls.py
├── manage.py               # File quản lý dự án Django
├── requirements.txt        # Danh sách thư viện
└── README.md               # Tài liệu hướng dẫn
```

---

## 🛠️ Cài đặt & chạy

### 1. Clone dự án

```bash
git clone https://github.com/quytranlx123/TwllightHotelManagement.git
cd TwllightHotelManagement
```

### 2. Tạo và kích hoạt môi trường ảo

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Tạo database và migrate

```bash
python manage.py migrate
```

### 5. Tạo tài khoản quản trị

```bash
python manage.py createsuperuser
```

### 6. Chạy server

```bash
python manage.py runserver
```

---

## 📖 Hướng dẫn sử dụng

- Truy cập giao diện chính tại:  
  `http://127.0.0.1:8000/`

- Giao diện quản trị Django:  
  `http://127.0.0.1:8000/admin/`

---

## 🔐 Xác thực & phân quyền

- Người dùng có thể đăng ký, đăng nhập (nếu đã tích hợp).
- Admin có thể tạo/sửa/xóa các thực thể như phòng, hóa đơn, loại phòng.
- Hỗ trợ bảo mật JWT nếu sử dụng REST API.

---

## 📝 TODO / Định hướng mở rộng

- [ ] Tích hợp REST API cho mobile app
- [ ] Giao diện quản lý hiện đại bằng React
- [ ] Tìm kiếm phòng theo ngày/tháng
- [ ] Gửi email xác nhận đặt phòng
- [ ] Giao diện responsive

---

## 📜 License

Hiện tại chưa có giấy phép mã nguồn mở. Có thể cân nhắc sử dụng:

- [MIT License](https://opensource.org/licenses/MIT)
- [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)

---

## 👤 Tác giả

- **Tên:** Trần Ngọc Quí  
- **GitHub:** [@quytranlx123](https://github.com/quytranlx123)  
- **Email:** *[tuỳ chọn nếu bạn muốn để]*

---

📌 *Cảm ơn bạn đã quan tâm đến dự án!*
