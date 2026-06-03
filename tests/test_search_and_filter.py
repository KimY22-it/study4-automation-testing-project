import pytest

from pages.tests_page import TestsPage 

@pytest.fixture
def page(driver):
    page = TestsPage(driver)
    page.load()
    return page

def test_TC_SEARCH_01_open_page(page):
    assert page.is_visible(page.SEARCH_INPUT)

@pytest.mark.parametrize("keyword", ["TOEIC"])
def test_TC_SEARCH_02_search_with_certificate_keyword(page, keyword):    
    page.search(keyword)
    assert page.check_keyword_in_results(keyword) 

@pytest.mark.parametrize("keyword", ["New Economy"])
def test_TC_SEARCH_03_search_with_thematic_keyword(page, keyword):    
    page.search(keyword)
    assert page.check_keyword_in_results(keyword) 

@pytest.mark.parametrize("invalid_key", ["abcxyz123"])
def test_TC_SEARCH_04_search_with_invalid_keyword(page, invalid_key):
    page.search(invalid_key)
    assert page.is_page_not_crashed(), "Trang bị lỗi khi nhập từ khóa không tồn tại"
    assert page.is_no_result_displayed() or len(page.get_results()) == 0

@pytest.mark.parametrize("invalid_key", ["<hfs"])
def test_TC_SEARCH_05_search_with_special_characters(page, invalid_key):
    page.search(invalid_key)
    assert page.is_page_not_crashed(), "Trang bị lỗi khi nhập từ khóa với các ký tự đặc biệt"
    assert page.is_invalid_keyword_displayed() or page.is_no_result_displayed() or len(page.get_results()) == 0

@pytest.mark.parametrize("keyword", ["Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với  với từ khóa dài Tìm kiêm Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài  kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa dài Tìm kiếm Tìm kiếm với từ khóa dài Tìm kiếm với từ khóa "])
def test_TC_SEARCH_06_search_with_a_very_long_keyword(page, keyword):
    page.search(keyword)
    assert page.is_page_not_crashed()
    if len(page.get_results()) > 0:
        assert page.check_keyword_in_results(keyword) 
    else:
        assert page.is_no_result_displayed() or page.is_invalid_keyword_displayed()

def test_TC_SEARCH_07_search_with_empty_keyword(page):
    page.search("")
    assert len(page.get_results()) > 0

@pytest.mark.parametrize("sql_key", ["' OR '1'='1 "])
def test_TC_SEARCH_08_search_with_sql_injection(page, sql_key):
    page.search(sql_key)
    assert page.is_page_not_crashed(), "Trang bị lỗi khi nhập SQL Injection"
    
@pytest.mark.parametrize("subject", ["IELTS Academic"])
def test_TC_FILTER_01_filter_by_subject(page, subject):
    page.filter(subject)
    assert page.check_filter_results(subject)

def test_TC_FILTER_02_filter_mini_tests(page):
    page.filter_mini_tests()
    assert 'tests/mini' in page.driver.current_url

@pytest.mark.parametrize(("subject", "keyword"), [("TOEIC", "New Economy")])
def test_TC_SEARCH_AND_FILTER_01_search_and_filter_combination(page, subject, keyword):
    page.filter(subject)
    page.search(keyword)
    assert page.check_keyword_in_results(keyword)
    assert page.check_filter_results(subject) 

@pytest.mark.parametrize("page_number", [2])
def test_TC_PAGING_01_pagination(page, page_number):
    initial_results = page.get_results()
    initial_texts = [r.text for r in initial_results]
    
    if page.go_to_page(page_number):
        next_page_results = page.get_results()
        next_texts = [r.text for r in next_page_results]
        assert initial_texts != next_texts
    else:
        pytest.skip("Not enough results for pagination test")
