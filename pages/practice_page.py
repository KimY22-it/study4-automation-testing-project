
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys

class PracticePage(BasePage):
    
    PRACTICE_PARTS = (By.XPATH, "//div[@class='form-check']")
    PART_NAME_IN_PRACTICE_PART = (By.XPATH, "//label[@class='form-check-label']")
    SET_PRACTICE_TIME = (By.XPATH, "//select[@name='time_limit']")
    PRACTICE_BUTTON = (By.XPATH, "//button[contains(text(), 'LUYỆN TẬP')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'NỘP BÀI')]")
    INPUT_ANSWER_1 = (By.ID, "question-37299")
    WARNING_BANNER = (By.XPATH, "//div[contains(text(), 'Bạn cần trả lời câu hỏi trong đề thi mới có thể nộp bài')]")
    TIMER = (By.ID, "timeleft")
    EXIT_BUTTON = (By.XPATH, "//a[contains(text(), 'Thoát')]")
    PRACTICE_FULL_TEST_BUTTON = (By.XPATH, "//a[normalize-space()='Làm full test']")
    START_TEST_BUTTON = (By.XPATH, "//a[contains(text(),'BẮT ĐẦU THI')]")
    PART_BUTTONS_IN_EXAM_PAGE = (By.XPATH, "//li[@role='presentation']/a")

    CONTINUE_BUTTON = (By.XPATH, "//a[contains(text(),'TIẾP THEO')]")
    QUESTION_NUMBER_LIST = (By.XPATH, "//div[@class='test-questions-list']")

    INPUT_ANSWERS = (By.XPATH, "//input[@data-type='question-answer']")
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
        submit_btn = self.find_element(self.SUBMIT_BUTTON)
        if submit_btn.is_enabled():
            submit_btn.click()

    def type_a_answer(self, answer):
        self.type_text(self.INPUT_ANSWER_1, answer)
        element = self.find_element(self.INPUT_ANSWER_1)
        element.send_keys(Keys.ENTER)

    def get_text_in_answer_input(self):
        return self.find_element(self.INPUT_ANSWER_1).get_attribute("value")

    def check_visible_part_name(self, part_name):
        part_buttons = self.find_elements(self.PART_BUTTONS_IN_EXAM_PAGE)
        for part_button in part_buttons:
            if part_name in part_button.text:
                return True
        return False

    def click_part_button(self, part_name):
        part_buttons = self.find_elements(self.PART_BUTTONS_IN_EXAM_PAGE)
        for part_button in part_buttons:
            if part_name in part_button.text:
                self.click_by_element(part_button)
                break
    
    def check_active_part_button(self, part_name):
        part_buttons = self.find_elements(self.PART_BUTTONS_IN_EXAM_PAGE)
        for part_button in part_buttons:
            button_text = part_button.text.strip()
            button_class = part_button.get_attribute("class")
            print(f"Button text: '{button_text}' | Class: {button_class} | Target: '{part_name}'")
            if part_name == button_text:
                print(f"Match found! Checking if 'active' in class: {button_class}")
                if "active" in button_class:
                    return True
                else:
                    return False
        return False  # Return False if no matching button found

    def get_text_in_part_button(self):
        part_buttons = self.find_elements(self.PART_BUTTONS_IN_EXAM_PAGE)
        text = []
        for part_button in part_buttons:
            text.append(part_button.text)
        return text

    def get_part_names_in_practice_part(self):
        part_names = self.find_elements(self.PART_NAME_IN_PRACTICE_PART)
        name = ""
        for part_name in part_names:
            name += part_name.text + "\n"
        return name.strip()

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
    
    def click_continue_button(self):
        return self.click(self.CONTINUE_BUTTON)
    
    def get_done_question_number(self, number):
        question_container = self.find_element(self.QUESTION_NUMBER_LIST)
        question_elements = question_container.find_elements(By.XPATH, ".//*")
        for question in question_elements:
            text = question.text.strip()
            if text == str(number):
                return "done" in question.get_attribute("class")
        # Fallback: if the container text includes the number but no separate child was found,
        # return the container's status if it carries the done class.
        if str(number) in question_container.text.split():
            return "done" in question_container.get_attribute("class")
        return False
    
    def click_question_number(self, number):
        question_container = self.find_element(self.QUESTION_NUMBER_LIST)
        question_elements = question_container.find_elements(By.XPATH, ".//*")
        for question in question_elements:
            text = question.text.strip()
            if text == str(number):
                self.click_by_element(question)
                break

    def is_answer_input_visible(self, question_number):
        """Check if the input field for a specific question number is focused/active"""
        try:
            # Find input field inside the question-wrapper that contains the specific question number
            input_field = self.driver.find_element(By.XPATH, f"//strong[text()='{question_number}']/ancestor::div[@class='question-wrapper']//input")
            return input_field.is_displayed()
        except:
            return False

