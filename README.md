
# 📝 Lab 2: Fullstack Note Application with Firebase

Dự án này là một ứng dụng ghi chú đơn giản được xây dựng nhằm mục tiêu thực hành tách biệt Frontend và Backend, tích hợp xác thực người dùng và lưu trữ dữ liệu đám mây qua Firebase

## 👤 Thông tin sinh viên
*   **Họ và tên:** Phạm Anh Khoa
*   **MSSV:** 24120074
*   **Lớp:** 24CTT5
*   **Trường:** Đại học Khoa học Tự nhiên - ĐHQG TP.HCM

---

## 🛠 Công nghệ sử dụng
*   **Backend:** FastAPI (Python)
*   **Frontend:** Streamlit
*   **Database & Auth:** Firebase Studio (Authentication & Firestore/Realtime DB)
*   **Version Control:** GitHub

---

## 📂 Cấu trúc thư mục
Dự án được tổ chức tách biệt giữa Frontend và Backend theo đúng yêu cầu
```text
lab2-note-app/
├── backend/            # Chứa logic xử lý API và kết nối Firebase
│   └── main.py         # File chạy chính của Backend (FastAPI)
├── frontend/           # Chứa giao diện người dùng
│   └── app.py          # File chạy chính của Frontend (Streamlit)
├── .gitignore          # Loại bỏ các file rác và Private Key (.vs, venv, firebase_key.json)
├── requirements.txt    # Danh sách các thư viện cần thiết
└── README.md           # Tài liệu hướng dẫn dự án
```

---

## 🚀 Hướng dẫn cài đặt và khởi chạy

### 1. Cài đặt môi trường
Mở Terminal tại thư mục gốc của dự án và cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 2. Chạy Backend (FastAPI)
Di chuyển vào thư mục backend và khởi chạy server
```bash
uvicorn backend.main:app --reload
```
*Hệ thống sẽ chạy tại địa chỉ: `[http://127.0.0.1:8000](http://127.0.0.1:8000)`*

### 3. Chạy Frontend (Streamlit)
Mở một Terminal mới và khởi chạy giao diện
```bash
streamlit run frontend/app.py
```
*Giao diện sẽ hiển thị tại: `http://localhost:8501`*

---

## 🔐 Bảo mật dữ liệu
*   Dự án sử dụng **Firebase Authentication** để quản lý đăng nhập/đăng xuất
*   File cấu hình dịch vụ `firebase_key.json` đã được đưa vào `.gitignore` để đảm bảo không bị lộ Private Key trên Repository công khai

---

## 🎥 Video Demo
Dưới đây là đường dẫn video giới thiệu và hướng dẫn sử dụng ứng dụng
👉 **[Xem Video Demo tại đây](Dán_Link_Của_Khoa_Vào_Đây)**

