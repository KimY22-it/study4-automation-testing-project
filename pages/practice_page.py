
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PracticePage(BasePage):
    
    PRACTICE_PARTS = (By.XPATH, "//div[@class='form-check']")
    SET_PRACTICE_TIME = (By.XPATH, "//select[@name='time_limit']")
    PRACTICE_BUTTON = (By.XPATH, "//button[contains(text(), 'LUYỆN TẬP')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'NỘP BÀI')]")
    INPUT_ANSWER = (By.ID, "question-37299")
    WARNING_BANNER = (By.XPATH, "//div[contains(text(), 'Bạn cần trả lời câu hỏi trong đề thi mới có thể nộp bài')]")
    TIMER = (By.ID, "timeleft")
    EXIT_BUTTON = (By.XPATH, "//a[contains(text(), 'Thoát')]")
    PRACTICE_FULL_TEST_BUTTON = (By.XPATH, "//a[normalize-space()='Làm full test']")
    START_TEST_BUTTON = (By.XPATH, "//a[contains(text(),'BẮT ĐẦU THI')]")
    
    def check_visible_practice_button(self):
        return self.is_visible(self.PRACTICE_BUTTON)

    def click_practice_part(self, part_name):
        practice_parts = self.find_elements(self.PRACTICE_PARTS)
        for practice_part in practice_parts:
            if part_name in practice_part.text:
                checkbox = practice_part.find_element(By.XPATH, ".//input[@type='checkbox']")
                self.click_by_element(checkbox)
                break

    def click_practice_button(self):
        return self.click(self.PRACTICE_BUTTON)
    
    def check_visible_submit_button(self):
        return self.is_visible(self.SUBMIT_BUTTON)

    def click_submit_button(self):
        return self.click(self.SUBMIT_BUTTON)

    def type_a_answer(self, answer):
        self.type_text(self.INPUT_ANSWER, answer)

    def choose_time_limit(self, time_limit):
        self.select_by_visible_text(self.SET_PRACTICE_TIME, time_limit)
    
    def get_time_limit(self):
        return self.find_element(self.SET_PRACTICE_TIME).get_attribute("value")

    def get_timer(self):
        return self.get_text(self.TIMER)
    
    def get_url(self):
        return self.driver.current_url

    def is_warning_banner_displayed(self):
        return self.is_visible(self.WARNING_BANNER)

    def click_exit_button(self):
        return self.click(self.EXIT_BUTTON)

    def choose_all_parts(self):
        practice_parts = self.find_elements(self.PRACTICE_PARTS)
        for practice_part in practice_parts:
            checkbox = practice_part.find_element(By.XPATH, ".//input[@type='checkbox']")
            self.click_by_element(checkbox)

    def click_practice_full_test_button(self):
        return self.click(self.PRACTICE_FULL_TEST_BUTTON)
    
    def click_start_test_button(self):
        return self.click(self.START_TEST_BUTTON)
    
    def check_visible_start_test_button(self):
        return self.is_visible(self.START_TEST_BUTTON)