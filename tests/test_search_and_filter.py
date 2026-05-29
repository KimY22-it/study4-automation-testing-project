import pytest

from pages.base_page import BasePage
from pages.tests_page import TestsPage 

@pytest.fixture
def tests_page(driver):
    tests_page = TestsPage(driver)
    tests_page.load()
    return tests_page

# TC_SEARCH_01: Verify that the tests page loads successfully
def test_open_tests_page(tests_page):
    assert tests_page.is_visible(tests_page.SEARCH_INPUT)

# TC_SEARCH_04: Verify that searching with a valid keyword returns relevant results

@pytest.mark.parametrize("key", ["TOEIC", "New Economy"])
def test_search_with_valid_keyword(tests_page, key):    
    tests_page.search(key)
    for result in tests_page.get_results():
        assert key.upper() in result.text.upper()

@pytest.mark.parametrize("invalid_key", ["abcxyz123"])
def test_search_with_invalid_keyword(tests_page, invalid_key):
    tests_page.search(invalid_key)
    assert tests_page.is_no_result_displayed() or len(tests_page.get_results()) == 0

@pytest.mark.parametrize("invalid_key", ["!@#$%^&*()"])
def test_search_with_special_characters(tests_page, invalid_key):
    tests_page.search(invalid_key)
    assert tests_page.is_page_not_crashed()
    assert tests_page.is_invalid_keyword_displayed() or tests_page.is_no_result_displayed() or len(tests_page.get_results()) == 0

def test_search_with_empty_keyword(tests_page):
    tests_page.search("")
    assert len(tests_page.get_results()) > 0

@pytest.mark.parametrize("subject", ["IELTS Academic"])
def test_filter_by_subject(tests_page, subject):
    tests_page.filter(subject)
    assert tests_page.check_filter_results(subject)

def test_filter_mini_tests(tests_page):
    tests_page.filter_mini_tests()
    assert 'tests/mini' in tests_page.driver.current_url

@pytest.mark.parametrize(("subject", "keyword"), [("TOEIC", "New Economy")])
def test_search_and_filter_combination(tests_page, subject, keyword):
    tests_page.filter(subject)
    tests_page.search(keyword)
    for result in tests_page.get_results():
        assert keyword.upper() in result.text.upper()
        assert subject.upper() in result.text.upper()

@pytest.mark.parametrize("page_number", [2])
def test_pagination(tests_page, page_number):
    initial_results = tests_page.get_results()
    initial_texts = [r.text for r in initial_results]
    
    if tests_page.go_to_page(page_number):
        next_page_results = tests_page.get_results()
        next_texts = [r.text for r in next_page_results]
        assert initial_texts != next_texts
    else:
        pytest.skip("Not enough results for pagination test")

@pytest.mark.parametrize("test_name", ["IELTS Simulation Listening test 1"])
def test_check_access_detail_test(driver, test_name):
    tests_page = TestsPage(driver)
    tests_page.click_detail_button(test_name)

    assert test_name in driver.title