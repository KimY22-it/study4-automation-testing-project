# open_profile_login.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

# dùng profile mới
options.add_argument(r"--user-data-dir=D:\selenium_profile_new")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.maximize_window()
driver.get("https://study4.com/")

input("Đăng nhập xong thì nhấn Enter để đóng Chrome...")


driver.quit()