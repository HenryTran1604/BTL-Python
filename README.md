# Bài tập lớn python nhóm 16: Ứng dụng desktop Python scraping
## I. Chức năng:
### - Lấy dữ liệu sản phẩm từ shopee, hiển thị, sắp xếp và lưu vào file csv
### - Download ảnh từ 1 link cho trước
## II.Yêu cầu tài nguyên:
1. Các thư viện sau:
    - BeautifulSoup
    - Selenium
    - tkinter
    - PIL
    - requests
    - tqdm
    - lxml
2. Ứng dụng Chromedriver
- Đối với cài đặt các thư viện trên: Các bạn vào cmd và copy paste đoạn code sau
```
    pip install BeautifulSoup4
    pip install Selenium
    pip install tkinter
    pip install Pillow
    pip install tqdm
    pip install requests
    pip install lxml
```
- Đối với Chromedriver: Các bạn vào link [Chromedriver](https://chromedriver.chromium.org/downloads) và chọn phiên bản tương thích với trình duyệt Chrome trên máy<br>Sau khi cài đặt, các bạn copy đường dẫn và thay thế vào biến `PATH` trong file `shopeeFunctions.py` và `imageFunctions.py`
## III. Chạy ứng dụng
Sau khi làm theo hướng dẫn trên, các bạn run file main.py