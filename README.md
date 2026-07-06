# Todo List Management

Ứng dụng quản lý công việc cá nhân được xây dựng theo cấu trúc backend/frontend tách riêng, tham khảo cách tổ chức project Smartwatch-Ai-Pro-Website và cách xử lý backend từ Library-Management.

Project sử dụng Flask API cho backend, ReactJS cho frontend và MySQL/Aiven MySQL để lưu tài khoản người dùng cùng danh sách công việc. Giao diện không dùng Bootstrap 5, không dùng react-bootstrap; toàn bộ style nằm trong CSS riêng của frontend.

## Tính năng

* Đăng ký tài khoản.
* Đăng nhập, đăng xuất bằng Flask-Login Session.
* Mỗi người dùng chỉ xem và quản lý danh sách công việc của mình.
* Hiển thị danh sách công việc.
* Thêm công việc mới.
* Chỉnh sửa công việc.
* Xóa công việc.
* Đánh dấu hoàn thành/chưa hoàn thành.
* Tìm kiếm theo tiêu đề hoặc mô tả.
* Lọc theo trạng thái: tất cả, chưa xong, hoàn thành.
* Sắp xếp theo mới nhất, cũ nhất, A-Z, trạng thái.
* Phân trang danh sách.
* Validate dữ liệu ở frontend và backend.
* Responsive với CSS custom.

## Công nghệ

### Backend

* Python 3.10+
* Flask
* Flask-CORS
* Flask-Login
* Flask-SQLAlchemy
* PyMySQL
* MySQL/Aiven MySQL
* Gunicorn

### Frontend

* ReactJS
* Axios
* CSS Custom

## Cấu trúc thư mục

```text
.
+-- backend/
|   +-- app.py
|   +-- __init__.py
|   +-- init_db.py
|   +-- models.py
|   +-- dao/
|   |   +-- __init__.py
|   |   +-- todo_dao.py
|   |   +-- users.py
|   +-- routes/
|   |   +-- __init__.py
|   |   +-- login_logout.py
|   |   +-- register.py
|   |   +-- todo_routes.py
|   +-- utils/
|   |   +-- __init__.py
|   |   +-- validator.py
|   +-- requirements.txt
+-- frontend/
|   +-- public/
|   +-- src/
|   |   +-- components/
|   |   +-- configs/
|   |   +-- screens/
|   |   +-- services/
|   |   +-- utils/
|   |   +-- App.js
|   |   +-- index.css
|   |   +-- index.js
|   +-- package.json
|   +-- package-lock.json
+-- docs/
+-- tests/
+-- .env.example
+-- .gitignore
+-- Procfile
+-- README.md
```

## Cài đặt backend

Tạo môi trường ảo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script, chạy trong terminal hiện tại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Cài dependency backend:

```powershell
python -m pip install -r backend\requirements.txt
```

Tạo file `.env` ở thư mục gốc theo `.env.example` và điền thông tin Aiven MySQL:

```env
SECRET_KEY=change-this-secret-key
AIVEN_DB_HOST=your-aiven-mysql-host.aivencloud.com
AIVEN_DB_PORT=12345
AIVEN_DB_USER=avnadmin
AIVEN_DB_PASSWORD=your-aiven-password
AIVEN_DB_NAME=todo_list_management
AIVEN_DB_SSL_CA=
```

Khởi tạo bảng và dữ liệu mẫu trên database:

```powershell
python backend\init_db.py
```

Chạy backend:

```powershell
python -m backend.app
```

Backend mặc định chạy tại:

```text
http://localhost:5000/api
```

## Cài đặt frontend

Mở terminal mới và chuyển vào thư mục frontend:

```powershell
cd frontend
npm install
```

Nếu cần đổi API URL, tạo file `frontend/.env`:

```env
REACT_APP_API_BASE_URL=http://localhost:5000/api
```

Chạy frontend:

```powershell
npm start
```

Frontend mặc định chạy tại:

```text
http://localhost:3000
```

## Tài khoản mẫu

Sau khi chạy:

```powershell
python backend\init_db.py
```

Hệ thống sẽ tạo tài khoản demo nếu chưa tồn tại:

```text
Username: demo
Password: demo123
```

## API chính

### Auth

```http
POST /api/register
POST /api/login
POST /api/logout
GET  /api/profile
```

### Todo

```http
GET    /api/health
GET    /api/todos
GET    /api/todos/:id
POST   /api/todos
PUT    /api/todos/:id
PATCH  /api/todos/:id/toggle
DELETE /api/todos/:id
```

Các API Todo yêu cầu người dùng đã đăng nhập. Frontend gửi request kèm cookie session thông qua Axios với `withCredentials: true`.

## Chạy build frontend

```powershell
cd frontend
npm run build
```

## Chạy test backend

```powershell
pytest
```

Lưu ý: Nếu backend đã bắt buộc đăng nhập cho API Todo, test cần tạo session đăng nhập hoặc mock user trước khi gọi các endpoint Todo.

## Đối chiếu yêu cầu đề bài

Đã hoàn thành:

* Hiển thị danh sách công việc.
* Thêm, sửa, xóa công việc.
* Đánh dấu hoàn thành/chưa hoàn thành.
* Tìm kiếm và lọc theo trạng thái.
* Đăng ký, đăng nhập và lưu Todo theo từng người dùng.
* Lưu dữ liệu bằng MySQL/Aiven MySQL.
* Xử lý dữ liệu không hợp lệ.
* Tổ chức mã nguồn rõ ràng theo mô hình backend/frontend.
* README hướng dẫn chạy dự án.
* Có phân trang, sắp xếp và responsive.

## Deploy

Frontend đã deploy tại:

```text
https://todo-list-management.pages.dev/
```