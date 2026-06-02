from selenium.common import StaleElementReferenceException
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FlashcardPage(BasePage):

    FLASHCARD_CARDS = (By.XPATH, "//div[@class='col-6 col-md-3']")
    WORD_CARDS = (By.XPATH, "//div[@class='termlist-item contentblock']")
    EDIT_BUTTON = (By.XPATH, "//a[@class='font-1 ml-1']")
    EDIT_FORM = (By.XPATH, "//div[@id='form-modal-content']")         
    DEFINE_INPUT = (By.ID, "field-definition")          
    SHOW_OPTION = (By.ID, "headingOne")                 
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
        return self.click(self.SHOW_OPTION)
                
    
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
        import time
        time.sleep(1) # Đợi modal render xong tránh StaleElement
        if label_text not in "Định nghĩa":
            self.click_show_options()
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
        self.click(self.EASY_BUTTON)

    def click_hard_button(self):
        self.switch_to_flashcard_iframe()
        self.click(self.HARD_BUTTON)

    def click_known_button(self):
        self.switch_to_flashcard_iframe()
        self.click(self.KNOWN_BUTTON)

        

