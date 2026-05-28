# Study4 Automation Testing Project

## 1. Giới thiệu

Website kiểm thử: https://study4.com/

Đây là project kiểm thử tự động website **Study4.com** bằng Selenium WebDriver, Python và Pytest.

Mục tiêu của project là kiểm thử một số chức năng chính trên website Study4, bao gồm:

- Tìm kiếm, lọc đề thi online
- Luyện tập đề thi online
- Sửa từ và luyện tập flashcard

---

## 2. Công nghệ sử dụng

- Python
- Selenium WebDriver
- Pytest
- WebDriver Manager
- Google Chrome
- Git/GitHub

---

## 3. Cấu trúc thư mục dự kiến

---

## 4. Các chức năng kiểm thử

### 4.1. Tìm kiếm, lọc đề thi online

Chức năng này kiểm tra việc người dùng truy cập trang thư viện đề thi, tìm kiếm đề thi theo từ khóa và lọc đề thi theo danh mục.

---

### 4.2. Luyện tập đề thi online

Chức năng này kiểm tra việc người dùng đã đăng nhập có thể chọn đề thi, chọn phần luyện tập, bắt đầu làm bài, trả lời câu hỏi và nộp bài.

---

### 4.3. Sửa từ và luyện tập flashcard

Chức năng này kiểm tra việc người dùng chỉnh sửa từ trong flashcard và luyện tập flashcard.

---

## 5. Cài đặt project

### Bước 1: Clone project

```bash
git clone <repository-url>
```

### Bước 2: Di chuyển vào thư mục project

```bash
cd study4-automation-testing
```

### Bước 3: Cài đặt thư viện cần thiết

```bash
pip install -r requirements.txt
```

Hoặc có thể cài thủ công:

```bash
pip install selenium pytest webdriver-manager
```

---

## 6. Cách chạy test

Chạy toàn bộ test case:

```bash
pytest
```

Chạy một file test cụ thể:

```bash
pytest testcases/test_search_and_filter.py
```

Chạy test và hiển thị chi tiết hơn:

```bash
pytest -v -s
```

Chạy test và tạo report HTML:

```bash
pytest --html=reports/report.html --self-contained-html
```

---

## 7. Cấu hình Chrome Profile

Project sử dụng Chrome profile riêng để duy trì trạng thái đăng nhập Study4 khi kiểm thử các chức năng yêu cầu tài khoản.

Trong `conftest.py`:

```python
options.add_argument(r"--user-data-dir=D:\selenium_profile")
```

Trước khi chạy các test case cần đăng nhập, người dùng cần đăng nhập Study4 thủ công trong profile này một lần. Sau đó Selenium có thể sử dụng lại trạng thái đăng nhập cho các lần chạy test sau.

---

## 9. Ghi chú

- Nếu Chrome báo lỗi profile đang được sử dụng, cần đóng toàn bộ cửa sổ Chrome hoặc đổi sang thư mục profile khác.
- Các locator trên website có thể thay đổi theo thời gian, vì vậy cần cập nhật script nếu giao diện website thay đổi.

---
