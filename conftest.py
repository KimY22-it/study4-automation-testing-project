import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from screenshot_utility import take_screenshot

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.set_capability("unhandledPromptBehavior", "ignore")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(r"--user-data-dir=D:\selenium_profile")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver: 
            take_screenshot(driver, f"FAILED_{item.name}")
