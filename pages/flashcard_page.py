from selenium.common import StaleElementReferenceException
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
import re

class FlashcardPage(BasePage):

    FLASHCARD_CARDS = (By.XPATH, "//div[@class='col-6 col-md-3']")
    WORD_CARDS = (By.XPATH, "//div[@class='termlist-item contentblock']")
    DEFINE_LINE_IN_WORD_CARD = (By.XPATH, "//div[@class='prewrap mb-2']")
    WORD_TYPE_LINE = (By.CSS_SELECTOR, "body > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > div:nth-child(2) > h2:nth-child(1) > span:nth-child(1)")
    PRONUNCIATION_LINE = (By.CSS_SELECTOR, "body > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > div:nth-child(2) > h2:nth-child(1) > span:nth-child(2)")
    EXAMPLE_LINE = (By.XPATH, "//ul[@class='termlist-item-examples']")
    NOTE_LINE = (By.XPATH, "//div[@class='prewrap']")
    PICTURE_AREA = (By.XPATH, "//div[@class='termlist-item-images']//img[@class='lazyel entered loaded']")

    CHOOSE_PICTURE = (By.XPATH, "//input[@id='id_image']")
    EDIT_BUTTON = (By.XPATH, "//a[@class='font-1 ml-1']")
    EDIT_FORM = (By.XPATH, "//div[@id='form-modal-content']")         
    DEFINE_INPUT = (By.ID, "field-definition")          
    SHOW_OPTION = (By.ID, "headingOne")  
    NEWWORD_INPUT = (By.XPATH, "//input[@id='id_name']")               
    CLOSE_FORM_BUTTON = (By.XPATH, "//div[@id='form-modal']//button[@aria-label='Close']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Lưu')]")
    LABEL_INPUT = (By.XPATH, "//div[@id='form-modal-content']//label")
    REQUIRED_ERROR = (By.XPATH, "//*[contains(text(), 'bắt buộc') or contains(text(), 'không được để trống') or contains(text(), 'required')]")
    PRACTICE_BUTTON = (By.XPATH, "//a[contains(text(),'Luyện tập flashcards')]")
    AREA_PRACTICE = (By.XPATH, "//div[contains(@class,'flashcard') and not(contains(@class,'flashcard-action'))]")
    AREA_LEVEL = (By.XPATH, "//div[contains(@class, 'flashcard-action-controls')]")
    FLASHCARD_ACTION = (By.XPATH, "//div[contains(@class, 'flashcard-action ')]")
    EASY_BUTTON = (By.XPATH, "//div[@class='flashcard-action action-easy text-success']")
    HARD_BUTTON = (By.XPATH, "//div[@class='flashcard-action action-difficult text-danger']")
    KNOWN_BUTTON = (By.XPATH, "//div[@class='flashcard-action action-ignore text-gray']")

    REVIEW_CARD = (By.XPATH, "//div[@class='flashcard-review']")
    DEFINE_IN_REVIEW_CARD = (By.XPATH, "//div[@class='prewrap mb-2']")
    DEFINE_IN_REVIEW_CARD_CHOOSE = (By.XPATH, "//h2[@class='font-2']")
    ANSWER_INPUT = (By.XPATH, "//input[@placeholder='Điền từ vào ô trống ...']")

    OPTIONS_IN_REVIEW_CARD = (By.XPATH, "//div[@class='flashcard-review-option']")
    KNOWN_IN_REVIEW_CARD = (By.XPATH, "//div[@class='float-right']")

    SHOW_ANSWER_BUTTON = (By.XPATH, "//span[@class='link flashcard-review-showanswer']")
    CONTINUE_BUTTON = (By.XPATH, "//span[@class='float-right link flashcard-review-skip']")

    def load(self):
        self.driver.get("https://study4.com/flashcards/")

    def check_visible_flashcard_cards(self):
        return self.is_visible(self.FLASHCARD_CARDS)
    
    def choose_flashcard(self, card_name):
        flashcard_cards = self.find_elements(self.FLASHCARD_CARDS)
        for card in flashcard_cards:
            if card_name in card.text:
                self.click_by_element(card)
                break

    def check_visible_word_cards(self):
        return self.is_visible(self.WORD_CARDS)
    
    def click_edit_button(self, word):
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                self.click_by_element(w.find_element(*self.EDIT_BUTTON))
                break
    
    def click_show_options(self):

        self.click(self.SHOW_OPTION)
        return True
    
    def get_text_newword_input(self):
        return self.find_element(self.NEWWORD_INPUT).get_attribute("value")
    
    def click_close_form_button(self):
        return self.click(self.CLOSE_FORM_BUTTON)

    def click_save_form_button(self):
        return self.click(self.SAVE_BUTTON)
    
    def check_visible_save_button(self):
        return self.is_visible(self.SAVE_BUTTON)
    

    def check_visible_edit_form(self):
        return self.is_visible(self.EDIT_FORM)
    
    def click_practice_button(self):
        """Click nút luyện tập và chờ browser navigate sang trang practice mới."""
        current_url = self.driver.current_url
        self.click(self.PRACTICE_BUTTON)
        # Chờ URL thay đổi (navigate sang trang practice)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.url_changes(current_url)
            )
        except TimeoutException:
            pass  # URL không đổi — trang practice có thể load ngay trong page
        # Chờ thêm để JS render xong iframe flashcard
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//iframe[contains(@class, 'flashcard-iframe')]")
                )
            )
        except TimeoutException:
            pass
    
    def type_define_input(self, text):
        self.type_text(self.DEFINE_INPUT, text)

    def type_text_field_by_text_label(self, label_text, text):
        labels = self.find_elements(self.LABEL_INPUT)
        for label in labels:
            if label_text in label.text.strip():
                id_input = label.get_attribute("for")
                typed = False

                # Cách 1: dùng thuộc tính 'for' → tìm bằng By.ID
                if id_input:
                    try:
                        self.type_text((By.ID, id_input), text)
                        typed = True
                    except Exception:
                        pass  

                # Cách 2: tìm input/textarea trong cùng thẻ cha với label
                if not typed:
                    parent = self.driver.execute_script(
                        "return arguments[0].parentElement", label
                    )
                    try:
                        input_elem = parent.find_element(
                            By.XPATH, ".//input | .//textarea"
                        )
                        input_elem.clear()
                        input_elem.send_keys(text)
                        typed = True
                    except Exception:
                        pass

                # Cách 3: tìm input/textarea trong thẻ cha của cha (grandparent)
                if not typed:
                    grandparent = self.driver.execute_script(
                        "return arguments[0].parentElement.parentElement", label
                    )
                    input_elem = grandparent.find_element(
                        By.XPATH, ".//input | .//textarea"
                    )
                    input_elem.clear()
                    input_elem.send_keys(text)

                break

    def upload_image_to_image_field(self, image_path):
        input_image = self.find_element(self.CHOOSE_PICTURE)
        input_image.send_keys(image_path)

    def get_text_of_define_in_wordcard(self, word):
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.find_element(*self.DEFINE_LINE_IN_WORD_CARD).text
        return None

    def get_word_type(self, word):
        """Lấy toàn bộ text của word card chứa từ đã cho để kiểm tra định nghĩa"""
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.find_element(*self.WORD_TYPE_LINE).text
        return None

    def get_word_pronunciation(self, word):
        """Lấy toàn bộ text của word card chứa từ đã cho để kiểm tra định nghĩa"""
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.find_element(*self.PRONUNCIATION_LINE).text
        return None

    def get_word_example(self, word):
        """Lấy toàn bộ text của word card chứa từ đã cho để kiểm tra định nghĩa"""
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.find_element(*self.EXAMPLE_LINE).text
        return None

    def get_word_note(self, word):
        """Lấy toàn bộ text của word card chứa từ đã cho để kiểm tra định nghĩa"""
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.find_element(*self.NOTE_LINE).text
        return None

    def get_word_picture(self, word):
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.find_element(*self.PICTURE_AREA).get_attribute("src")
        return None
    def get_word_definition(self, word):
        """Lấy toàn bộ text của word card chứa từ đã cho để kiểm tra định nghĩa"""
        words = self.find_elements(self.WORD_CARDS)
        for w in words:
            if word in w.text:
                return w.text
        return None


    def is_required_error_displayed(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located(self.REQUIRED_ERROR)
            )
            return error.is_displayed()
        except TimeoutException:
            return False
    
    def switch_to_flashcard_iframe(self):
        self.driver.switch_to.default_content()
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'flashcard-iframe')]")))
            self.driver.switch_to.frame(iframe)
        except TimeoutException:
            pass

    def flip_card(self):
        self.switch_to_flashcard_iframe()
        # Click vào chính thẻ (AREA_PRACTICE) để lật mặt thẻ
        self.click(self.AREA_PRACTICE)
        import time
        time.sleep(1) # Chờ thẻ lật xong (animation)

    def check_visible_area_practice(self):
        self.switch_to_flashcard_iframe()
        return self.is_visible(self.AREA_PRACTICE)

    def check_visible_area_level(self):
        self.switch_to_flashcard_iframe()
        return self.is_visible(self.AREA_LEVEL)
        
    def check_enable_click_action_buttons(self):
        self.switch_to_flashcard_iframe()

        actions = self.find_elements(self.FLASHCARD_ACTION)

        if len(actions) < 3:
            return False

        try:
            for action in actions[:3]:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    action
                )

                self.wait.until(EC.element_to_be_clickable(action))

            return True

        except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException):
            return False
            
    def get_text_in_practice_card(self):
        self.switch_to_flashcard_iframe()
        return self.get_text(self.AREA_PRACTICE)
    
    def click_easy_button(self):
        self.switch_to_flashcard_iframe()
        element = self.find_element(self.EASY_BUTTON)
        element.click()

    def click_hard_button(self):
        self.switch_to_flashcard_iframe()
        element = self.find_element(self.HARD_BUTTON)
        element.click()

    def click_known_button(self):
        self.switch_to_flashcard_iframe()
        element = self.find_element(self.KNOWN_BUTTON)
        element.click()

        
    def check_visible_review_card(self):
        self.switch_to_flashcard_iframe()
        return self.is_visible(self.REVIEW_CARD)

    def get_text_in_review_card(self):
        self.switch_to_flashcard_iframe()
        return self.get_text(self.REVIEW_CARD)
    
    def check_answer_input(self):
        self.switch_to_flashcard_iframe()
        return self.is_visible(self.ANSWER_INPUT)
    
    def type_answer_input(self, text):
        self.switch_to_flashcard_iframe()
        self.type_text(self.ANSWER_INPUT, text)

    def clear_answer_input(self):
        self.switch_to_flashcard_iframe()
        self.clear_text(self.ANSWER_INPUT)

    def press_enter(self):
        self.switch_to_flashcard_iframe()
        element = self.find_element(self.ANSWER_INPUT)
        element.send_keys(Keys.ENTER)

    def get_define_in_review_card(self):
        self.switch_to_flashcard_iframe()

        try:
            text = self.get_text(self.DEFINE_IN_REVIEW_CARD)
            if text:
                return text
        except TimeoutException:
            pass

        try:
            text = self.get_text(self.DEFINE_IN_REVIEW_CARD_CHOOSE)
            if text:
                return text
        except TimeoutException:
            pass

        return ""

    def click_known_in_review_card(self):
        self.switch_to_flashcard_iframe()
        self.click(self.KNOWN_IN_REVIEW_CARD)

    def click_show_answer(self):
        self.switch_to_flashcard_iframe()
        self.click(self.SHOW_ANSWER_BUTTON)

    def get_text_in_answer_input(self):
        self.switch_to_flashcard_iframe()
        return self.find_element(self.ANSWER_INPUT).get_attribute("value")

    def check_visiable_options_in_review_card(self):
        self.switch_to_flashcard_iframe()
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located(self.OPTIONS_IN_REVIEW_CARD))
            return len(elements) > 0
        except TimeoutException:
            return False
    
    def choose_options_in_review_card(self, answer):
        self.switch_to_flashcard_iframe()
        options = self.find_elements(self.OPTIONS_IN_REVIEW_CARD)
        for option in options:
            if answer.strip().lower() in option.text.strip().lower():
                option.click()
                break
        
    def choose_incorrect_options_in_review_card(self, answer):
        self.switch_to_flashcard_iframe()
        options = self.find_elements(self.OPTIONS_IN_REVIEW_CARD)
        for option in options:
            if answer.strip().lower() not in option.text.strip().lower():
                option.click()
                break

    def click_continue_button(self):
        self.switch_to_flashcard_iframe()
        self.click(self.CONTINUE_BUTTON)

    def normalize_review_text(self, text):
        # Xóa các số thứ tự 1,2,3,4 đứng riêng
        text = re.sub(r'\b[1-4]\b', '', text)

        # Chuẩn hóa khoảng trắng, xuống dòng
        text = re.sub(r'\s+', ' ', text).strip()

        return text