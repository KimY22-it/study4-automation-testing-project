from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class TestsPage(BasePage):
    
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Nhập từ khoá bạn muốn tìm kiếm: tên sách, dạng câu hỏi ...']")
    
    SEARCH_BUTTON = (By.XPATH, "//button[text()='Tìm kiếm']")
    
    RESULTS = (By.XPATH, "//div[@class='col-6 col-md-3']")
    
    NO_RESULT_TEXT = (By.XPATH, "//*[contains(text(), 'Không tìm thấy') or contains(text(), 'không có kết quả')]")
    
    INVALID_KEYWORD_MESSAGE = (By.XPATH, "//*[contains(text(), 'không hợp lệ') or contains(text(), 'không được phép')]")

    FILTER_SUBJECTS = (By.XPATH, "//li[@class='nav-item w-auto'] //a[contains(@class, 'nav-link')]")

    MINI_TEST_FILTER = (By.XPATH, "//a[contains(text(),'Đề rút gọn')]")

    PAGINATION_BUTTON = (By.XPATH, "//a[@class='page-link']")

    def load(self):
        self.open_url("https://study4.com/tests/")
    
    def search(self, keyword):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_results_loaded(self.RESULTS)

    def get_results(self):
        return self.find_elements(self.RESULTS)

    def check_keyword_in_results(self, keyword):
        results = self.get_results()
        for result in results:
            if keyword.upper() not in result.text.upper():
                return False
        return True
    
    def filter(self, subject):
        subjects = self.find_elements(self.FILTER_SUBJECTS)
        for subj in subjects:
            if subj.text.strip().upper() == subject.upper():
                self.click_by_element(subj)  
                self.wait_for_results_loaded(self.RESULTS)           
                break

    def check_filter_results(self, subject):
        results = self.get_results()
        if len(results) == 0:
            return False
        for r in results:
            if subject.upper() not in r.text.upper():
                return False
        return True

    def is_no_result_displayed(self):
        return len(self.driver.find_elements(*self.NO_RESULT_TEXT)) > 0

    def is_invalid_keyword_displayed(self):
        return len(self.driver.find_elements(*self.INVALID_KEYWORD_MESSAGE)) > 0

    def is_page_not_crashed(self):
        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()

        error_keywords = [
            "internal server error",
            "server error",
            "application error",
            "exception",
            "traceback",
            "something went wrong",
            "bad request"
            "Error code 520"
        ]

        return not any(keyword in page_text for keyword in error_keywords)
    
    def filter_mini_tests(self):
        self.click(self.MINI_TEST_FILTER)
        self.wait_for_results_loaded(self.RESULTS)


    def go_to_page(self, page_number):
        buttons = self.find_elements(self.PAGINATION_BUTTON)
        for btn in buttons:
            try:
                if btn.text.strip() == str(page_number):
                    self.click_by_element(btn)
                    self.wait_for_results_loaded(self.RESULTS)
                    return True
            except Exception:
                continue
        return False
    
    def click_detail_button(self, test_name):
        self.search(test_name)
        result = self.get_results()[0]
        self.click_by_element(result)