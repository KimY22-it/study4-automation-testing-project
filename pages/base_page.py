
from selenium.webdriver.support.select import Select
from selenium.common import StaleElementReferenceException
from selenium.common import ElementClickInterceptedException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 2)
    
    def open_url(self, url):
        self.driver.get(url)
    
    def find_element(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator: tuple):
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def click(self, locator: tuple, timeout=None, js_fallback=True):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self._scroll_to_element(element)
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return 
            except ElementClickInterceptedException:
                if js_fallback:
                    self._js_click(element)
                    return
                raise
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.5)
    def click_by_element(self, element, js_fallback=True):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self._scroll_to_element(element)
                self.wait.until(EC.visibility_of(element))
                element.click()
                return
            except ElementClickInterceptedException:
                if js_fallback:
                    self._js_click(element)
                    return
                raise
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.5)
    
    def select_by_visible_text(self, locator: tuple, text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        select = Select(element)
        select.select_by_visible_text(text)
    
    def _scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        time.sleep(0.3)
    def _js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
    
    # def click(self, locator: tuple):
    #     element = self.wait.until(EC.element_to_be_clickable(locator))

    #     self.driver.execute_script(
    #         "arguments[0].scrollIntoView({block: 'center'});",
    #         element
    #     )

    #     element = self.wait.until(EC.element_to_be_clickable(locator))
    #     element.click()

    # def click_by_element(self, element):
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    #     self.driver.execute_script("arguments[0].click();", element)
  
    def type_text(self, locator: tuple, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find_element(locator).text.strip()

    def clear_text(self, locator: tuple):
        element = self.find_element(locator)
        element.clear()
    
    def is_visible(self, locator: tuple) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_for_results_loaded(self, locator: tuple):
        try:
            elements = self.find_elements(locator)
            if len(elements) > 0:
                self.wait.until(EC.visibility_of_any_elements_located(locator))
        except TimeoutException:
            pass

            