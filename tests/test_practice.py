from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pytest
import re

from pages.practice_page import PracticePage
from pages.tests_page import TestsPage

TEST_NAME = "IELTS Simulation Listening test 1"

# @pytest.fixture(scope="module")
@pytest.fixture
def practice_page(driver):
    tests_page = TestsPage(driver)
    tests_page.load()
    tests_page.click_detail_button(TEST_NAME)
    practice_page = PracticePage(driver)
    return practice_page


def test_TC_PRACTICE_01_access_detail_test(practice_page):
    assert practice_page.check_visible_practice_button()

@pytest.mark.parametrize("part_name", ["Recording 1"])
def test_TC_PRACTICE_02_practice_a_part_of_test(practice_page, part_name):
    practice_page.click_practice_part(part_name)
    practice_page.click_practice_button()
    assert practice_page.check_visible_submit_button()
    assert practice_page.check_visible_part_name(part_name)

@pytest.mark.parametrize(("part_name1, part_name2"), [("Recording 1", "Recording 2")])
def test_TC_PRACTICE_03_practice_multiple_parts(practice_page, part_name1, part_name2):
    practice_page.click_practice_part(part_name1)
    practice_page.click_practice_part(part_name2)
    practice_page.click_practice_button()
    assert practice_page.check_visible_submit_button()
    assert practice_page.check_visible_part_name(part_name1) and practice_page.check_visible_part_name(part_name2)

def test_TC_PRACTICE_04_click_practice_button_without_choose_part(practice_page):
    old_url = practice_page.driver.current_url
    practice_page.click_practice_button()
    new_url = practice_page.driver.current_url
    assert old_url == new_url

# @pytest.mark.parametrize("part_name", ["Recording 1"])
# def test_TC_PRACTICE_05_submit_test_without_choose_answers(practice_page, part_name):
#     practice_page.click_practice_part(part_name)
#     practice_page.click_practice_button()
#     practice_page.click_submit_button()
#     new_url = practice_page.driver.current_url
#     assert "results" not in new_url
#     assert practice_page.is_warning_banner_displayed()

# @pytest.mark.parametrize("part_name", ["Recording 1"])
# def test_TC_PRACTICE_06_submit_test_with_a_part_answers(practice_page, part_name):
#     practice_page.click_practice_part(part_name)
#     practice_page.click_practice_button()
#     old_url = practice_page.driver.current_url
#     practice_page.type_a_answer("answer")
#     time.sleep(3)
#     practice_page.click_submit_button()
#     new_url = practice_page.driver.current_url
#     assert "results" not in new_url
#     assert old_url == new_url

# @pytest.mark.parametrize("part_name", ["Recording 1"])
# @pytest.mark.parametrize("time_limit", ["5 phút"])
# def test_TC_PRACTICE_07_timer_display_correct_time(practice_page, part_name, time_limit):
#     practice_page.click_practice_part(part_name)
#     practice_page.choose_time_limit(time_limit)
#     practice_page.click_practice_button()
#     time.sleep(1)
#     timer_text = practice_page.get_timer()
#     minutes_int = int(re.search(r'\d+', time_limit).group())
#     expected_start = f"0{minutes_int}:" if minutes_int < 10 else f"{minutes_int}:"
#     expected_start_minus_1 = f"0{minutes_int-1}:" if (minutes_int - 1) < 10 else f"{minutes_int-1}:"
#     assert timer_text.startswith(expected_start) or timer_text.startswith(expected_start_minus_1)

@pytest.mark.parametrize("part_name", ["Recording 1"])
@pytest.mark.parametrize("time_limit", ["5 phút"])
def test_TC_PRACTICE_05_auto_submit_test_when_limit_time_run_out(practice_page, part_name, time_limit):
    practice_page.click_practice_part(part_name)
    practice_page.choose_time_limit(time_limit)
    practice_page.click_practice_button()
    minutes_int = int(re.search(r'\d+', time_limit).group())
    WebDriverWait(practice_page.driver, minutes_int*60+20).until(
        EC.url_contains("results")
    )
    current_url = practice_page.driver.current_url
    assert "results" in current_url.lower(), \
        f"Hết thời gian nhưng hệ thống không tự chuyển sang trang kết quả. URL hiện tại: {current_url}"

# @pytest.mark.parametrize("part_name", ["Recording 1"])
# def test_TC_PRACTICE_06_exit_test_before_submit(practice_page, part_name):
#     practice_page.click_practice_part(part_name)
#     practice_page.click_practice_button()
#     practice_page.click_exit_button()
#     assert 'practice' in practice_page.get_url().lower(), \
#         f"Đã thoát khỏi bài luyện tập. URL hiện tại: {practice_page.get_url()}"


def test_TC_PRACTICE_07_practice_full_test(practice_page):
    part_names = practice_page.get_part_names_in_practice_part()
    time.sleep(3)
    practice_page.click_practice_full_test_button()
    assert practice_page.check_visible_start_test_button()
    practice_page.click_start_test_button()
    time.sleep(3)
    part_name_in_exam_page = practice_page.get_text_in_part_button()
    assert practice_page.check_visible_submit_button()
    for part_name in part_name_in_exam_page:
        assert part_name.strip() in part_names.strip()

    assert len(part_name_in_exam_page) == len(part_names.split("\n"))

@pytest.mark.parametrize(("part_name1, part_name2"), [("Recording 1", "Recording 2")])
def test_TC_PRACTICE_08_switch_to_another_part(practice_page, part_name1, part_name2):
    practice_page.click_practice_part(part_name1)
    practice_page.click_practice_part(part_name2)
    practice_page.click_practice_button()
    assert practice_page.check_visible_submit_button()
    assert practice_page.check_visible_part_name(part_name1) and practice_page.check_visible_part_name(part_name2)
    
    practice_page.click_part_button(part_name1)
    practice_page.type_a_answer("test")
    old_answer = practice_page.get_text_in_answer_input()
    practice_page.click_part_button(part_name2)
    assert practice_page.check_active_part_button(part_name2)
    practice_page.click_part_button(part_name1)
    time.sleep(2)
    new_answer = practice_page.get_text_in_answer_input()
    assert old_answer == new_answer
    
@pytest.mark.parametrize(("part_name1, part_name2"), [("Recording 1", "Recording 2")])
def test_TC_PRACTICE_09_clicking_next_to_move_to_next_part(practice_page, part_name1, part_name2):
    practice_page.click_practice_part(part_name1)
    practice_page.click_practice_part(part_name2)
    practice_page.click_practice_button()
    assert practice_page.check_visible_submit_button()
    assert practice_page.check_visible_part_name(part_name1) and practice_page.check_visible_part_name(part_name2)
    practice_page.click_part_button(part_name1)
    practice_page.click_continue_button()
    assert practice_page.check_active_part_button(part_name2)

@pytest.mark.parametrize(("part_name", "number_question"), [("Recording 1", 1)])
def test_TC_PRACTICE_10_check_status_question_number_after_answering(practice_page, part_name, number_question):
    practice_page.click_practice_part(part_name)
    practice_page.click_practice_button()
    assert practice_page.check_visible_submit_button()
    assert practice_page.check_visible_part_name(part_name)
    practice_page.type_a_answer("test")
    time.sleep(2)
    assert practice_page.get_done_question_number(number_question)

@pytest.mark.parametrize(("part_name", "number_question"), [("Recording 1", 5)])
def test_TC_PRACTICE_11_check_navigating_to_question_when_clicking_on_question_number(practice_page, part_name, number_question):
    practice_page.click_practice_part(part_name)
    practice_page.click_practice_button()
    assert practice_page.check_visible_submit_button()
    assert practice_page.check_visible_part_name(part_name)
    practice_page.click_question_number(number_question)
    time.sleep(2)

    assert practice_page.is_answer_input_visible(number_question)
    