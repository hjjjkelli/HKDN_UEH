#  Final Year Assignment

## Objective
Dự án này sử dụng Selenium và BeautifulSoup để thu thập dữ liệu từ Google Reviews, bao gồm tên người đánh giá, nội dung đánh giá, số sao, và thời gian đăng đánh giá.

### Cách chạy chương trình CrawlData
```Requirements
Python 3.x
Selenium
BeautifulSoup
pandas
```
Cài đặt **chromedriver.exe** phù hợp với bản đang sử dụng. Có thể sử dụng egdedrive tương ứng. ***(https://googlechromelabs.github.io/chrome-for-testing/)***

Sau đó bỏ file **chromedriver.exe** vào thư mục lưu trữ Project và thay đường dẫn tuyệt đối của driver vào thư mục CrawlData.py
```Requirements
driver_path = r"<YOUR_PAHT>\chromedriver.exe"
```
Sau đó khởi chạy CrawlData.py là sẽ hoàn tất việc setup và thu thập đánh giá tại đường link được thiết lập sẵn. (Đường link có thể thay đổi trong cài đặt của đoạn Code)

## Future Work
**Mở rộng dữ liệu thu thập**: Cải thiện khả năng thu thập dữ liệu từ nhiều nguồn khác nhau.

**Nâng cao phân tích cảm xúc**: Khám phá các mô hình và phương pháp khác để cải thiện độ chính xác trong phân tích cảm xúc.

**Tối ưu hóa mã nguồn**: Cải thiện hiệu suất và tính khả thi của mã nguồn để hỗ trợ quy mô lớn hơn.

## Conclusion
Dự án này không chỉ giúp thu thập và phân tích dữ liệu từ Google Reviews mà còn tạo ra một nền tảng để thực hiện các nghiên cứu sâu hơn về hành vi của khách hàng và xu hướng trong đánh giá sản phẩm.
