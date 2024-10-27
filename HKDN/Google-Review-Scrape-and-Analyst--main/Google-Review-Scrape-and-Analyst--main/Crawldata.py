import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Đường dẫn đến tệp ChromeDriver
chromedriver_path = r"C:\Users\nyhoh\Downloads\HKDN\Google-Review-Scrape-and-Analyst--main\Google-Review-Scrape-and-Analyst--main\chromedriver.exe"

# Khởi tạo Service và Options cho ChromeDriver
chrome_service = Service(executable_path=chromedriver_path)
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # Ẩn các log từ Chrome

# Khởi tạo driver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def get_element_text(review, class_name, default='N/A'):
    """Lấy văn bản từ phần tử với class_name."""
    element = review.find(class_=class_name)
    return element.text if element else default

def get_review_content(review):
    """Lấy nội dung đánh giá từ phần tử."""
    content_elements = review.find_all('span', class_='wiI7pd')
    return ' '.join(element.get_text(separator=' ', strip=True).replace('\n', ' ') for element in content_elements) if content_elements else 'N/A'

def extract_review_data(review_set):
    """Trích xuất dữ liệu đánh giá từ tập hợp các đánh giá."""
    review_data = []
    for review in review_set:
        reviewer_name = get_element_text(review, 'd4r55')
        local_guide_status = get_element_text(review, 'RfnDt')
        review_content = get_review_content(review)
        review_date = get_element_text(review, 'rsqaWe')
        star_rating = get_element_text(review.find('span', class_='kvMYJc'), 'aria-label', 'N/A')
        likes_count = get_element_text(review, 'pkWtMe', '0')

        review_data.append({
            'Reviewer': reviewer_name,  # Tên người đánh giá
            'Content': review_content,  # Nội dung đánh giá
            'Date': review_date,  # Ngày đánh giá
            'Stars': star_rating,  # Số sao đánh giá
            'Local Guide': local_guide_status,  # Tình trạng Hướng dẫn viên địa phương
            'Likes': likes_count  # Số lượng thích
        })
    
    return pd.DataFrame(review_data)

def load_reviews(driver, url_list):
    """Tải đánh giá từ danh sách URL."""
    for review_url in url_list:
        logging.info(f"Đang tải đánh giá từ: {review_url}")
        driver.get(review_url)

        # Chờ đến khi trang được tải hoàn toàn
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]')))

        # Nhấp vào nút "Bài đánh giá" để lấy các đánh giá
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div/div/button[2]/div[2]'))
            )
            load_more_button.click()
            logging.info("Đã nhấp vào nút 'Bài đánh giá'.")
        except Exception as e:
            logging.warning(f"Không thể tìm hoặc nhấp vào nút 'Bài đánh giá': {e}")

        # Cuộn xuống để tải thêm đánh giá nếu cần
        scrollable_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]'))
        )

        # Mở rộng các đánh giá dài
        try:
            while True:
                more_buttons = driver.find_elements(By.CLASS_NAME, 'w8nwRe')
                if not more_buttons:
                    logging.info("Không còn nút 'Thêm' nào để nhấp.")
                    break
                
                for button in more_buttons:
                    try:
                        driver.execute_script("arguments[0].click();", button)
                        logging.info("Đã nhấp vào nút 'Thêm' để mở rộng đánh giá.")
                        time.sleep(1)  # Chờ sau khi nhấp vào nút
                    except Exception as e:
                        logging.warning(f"Không thể nhấp vào nút: {e}")
        except Exception as e:
            logging.error(f"Lỗi khi mở rộng đánh giá: {e}")
            
        previous_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_element)
        while True:
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_element)
                WebDriverWait(driver, 5).until(lambda d: d.execute_script("return arguments[0].scrollHeight;", scrollable_element) > previous_height)

                current_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_element)

                if current_height == previous_height:
                    logging.info("Đã đến cuối các đánh giá.")
                    break

                previous_height = current_height
            except TimeoutException:
                logging.warning("Đã xảy ra timeout trong khi chờ thay đổi chiều cao cuộn. Dừng cuộn.")
                break

def save_to_csv(dataframe, filename='datareview.csv'):
    """Lưu DataFrame vào tệp CSV."""
    if os.path.isfile(filename):
        previous_data = pd.read_csv(filename)
        combined_data = pd.concat([previous_data, dataframe], ignore_index=True)
    else:
        combined_data = dataframe
    combined_data.to_csv(filename, index=False)
    logging.info(f"Dữ liệu đã được lưu vào {filename}")

# Thực thi chính
if __name__ == "__main__":
    # Danh sách URL để thu thập dữ liệu
    url_list = [
        'https://www.google.com/maps/place/B%E1%BA%A3o+Hi%E1%BB%83m+Manulife/@10.7814739,106.6906709,15.49z/data=!4m10!1m2!2m1!1smanulife!3m6!1s0x317528d318cfb18b:0xba954bd27cb9e831!8m2!3d10.7811083!4d106.6970667!15sCghtYW51bGlmZSIDiAEBWgoiCG1hbnVsaWZlkgERaW5zdXJhbmNlX2NvbXBhbnngAQA!16s%2Fg%2F11c38t5mw5?hl=vi&entry=ttu&g_ep=EgoyMDI0MDkyNS4wIKXMDSoASAFQAw%3D%3D'
    ]

    load_reviews(driver, url_list)

    # Trích xuất đánh giá và lưu vào tệp CSV
    soup_response = BeautifulSoup(driver.page_source, 'html.parser')
    review_items = soup_response.find_all('div', class_='jftiEf')
    reviews_df = extract_review_data(review_items)
    
    save_to_csv(reviews_df)
    driver.quit()
