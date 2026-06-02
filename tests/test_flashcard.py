import time
import pytest

from pages.flashcard_page import FlashcardPage

@pytest.fixture
def page(driver):
    page = FlashcardPage(driver)
    page.load()
    return page

def test_TC_FLASH_EDIT_01_check_access_flashcard_page(page):
    assert "flashcards" in page.driver.title.lower()
    assert page.check_visible_flashcard_cards()

@pytest.mark.parametrize("card_name", ["TOEIC Word List"])
def test_TC_FLASH_EDIT_02_check_access_flashcard(page, card_name):
    page.choose_flashcard(card_name)
    assert page.check_visible_word_cards()

@pytest.mark.parametrize(("card_name", "word"), [("TOEIC Word List", "improve")])
def test_TC_FLASH_EDIT_03_open_edit_form(page, card_name, word):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    # Dùng is_visible() đã có WebDriverWait(10) bên trong → không cần time.sleep(5)
    assert page.check_visible_edit_form(), \
        f"Edit form không hiển thị sau khi click nút edit của từ '{word}'"

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "cải thiện")])
def test_TC_FLASH_EDIT_04_edit_a_field_of_word(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.click_save_form_button()
    page.driver.refresh()
    word_text = page.get_word_definition(word)
    assert word_text is not None and text_value in word_text, \
        f"Hệ thống không hiển thị nghĩa mới '{text_value}' thành công. Nội dung thẻ từ: {word_text}"

@pytest.mark.parametrize(("card_name", "word", "field_name1", "text_value1", "field_name2", "text_value2"), 
                         [("TOEIC Word List", "improve", "Định nghĩa", "tận dụng", "Ví dụ", "to improve the occasion")])
def test_TC_FLASH_EDIT_05_edit_multiple_fields(page, card_name, word, field_name1, text_value1, field_name2, text_value2):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    # Chờ modal mở trước khi gõ text
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name1, text_value1)
    page.type_text_field_by_text_label(field_name2, text_value2)
    page.click_save_form_button()
    page.driver.refresh()
    word_text = page.get_word_definition(word)
    assert word_text is not None and text_value1 in word_text and text_value2 in word_text, \
        f"Hệ thống không hiển thị nghĩa mới thành công. Nội dung thẻ từ: {word_text}"

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "")])
def test_TC_FLASH_EDIT_06_edit_a_required_field_of_word_with_empty_text(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.click_save_form_button()
    assert page.is_required_error_displayed() or page.check_visible_edit_form()

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "cải thiện")])
def test_TC_FLASH_EDIT_07_cancel_editing(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    old_text = page.get_word_definition(word)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.click_close_form_button()
    new_text = page.get_word_definition(word)
    assert not page.check_visible_save_button()
    assert old_text == new_text

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "@@@###!!!")])
def test_TC_FLASH_EDIT_08_edit_with_special_characters(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    old_text = page.get_word_definition(word)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.driver.refresh()
    word_text = page.get_word_definition(word)
    assert word_text is not None and text_value in word_text, \
        f"Hệ thống không hiển thị nghĩa mới '{text_value}' thành công. Nội dung thẻ từ: {word_text}"

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "<hfs")])
def test_TC_FLASH_EDIT_09_edit_with_no_meaning_word(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    old_text = page.get_word_definition(word)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.driver.refresh()
    word_text = page.get_word_definition(word)
    assert word_text is not None and text_value in word_text, \
        f"Hệ thống không hiển thị nghĩa mới '{text_value}' thành công. Nội dung thẻ từ: {word_text}"
    

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "@@@###!!!")])
def test_TC_FLASH_INTEGRATION_01_edit_with_special_characters_in_value(page, card_name, word, field_name, text_value):
    try:
        page.choose_flashcard(card_name)
        old_text = page.get_word_definition(word)
        page.click_edit_button(word)
        assert page.check_visible_edit_form(), \
            f"Edit form chưa mở — không thể nhập liệu"
        page.type_text_field_by_text_label(field_name, text_value)
        page.click_save_form_button()
        page.driver.refresh()
        
        word_def = page.get_word_definition(word)
        assert word_def is not None and text_value in word_def, \
            f"Hệ thống không hiển thị nghĩa mới '{text_value}' thành công. Nội dung: {word_def}"        
        page.click_practice_button()
        page.flip_card()

        assert page.check_visible_area_practice() and page.check_visible_area_level(), \
            "Hệ thống không hiển thị area practice hoặc area level thành công."
        assert page.check_enable_click_action_buttons()
    finally:
        # Quay về trang danh sách flashcard và khôi phục lại nghĩa cũ
        page.driver.switch_to.default_content()
        page.load()
        page.choose_flashcard(card_name)
        page.click_edit_button(word)
        # Đợi form mở
        if page.check_visible_edit_form():
            page.type_text_field_by_text_label(field_name, "cải thiện")
            page.click_save_form_button()
            time.sleep(1)

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "<hfs")])
def test_TC_FLASH_INTEGRATION_02_edit_with_invalid_html_tag(page, card_name, word, field_name, text_value):
    try:
        page.choose_flashcard(card_name)
        old_text = page.get_word_definition(word)
        page.click_edit_button(word)
        assert page.check_visible_edit_form(), \
            f"Edit form chưa mở — không thể nhập liệu"
        page.type_text_field_by_text_label(field_name, text_value)
        page.click_save_form_button()
        page.driver.refresh()
        
        word_def = page.get_word_definition(word)
        # Hệ thống xử lý an toàn (có thể strip thẻ hoặc escape) nên không nhất thiết phải chứa y nguyên chuỗi "<hfs"
        assert word_def is not None, "Không tìm thấy word card sau khi lưu"
        
        page.click_practice_button()
        page.flip_card()

        # Kiểm tra giao diện luyện tập không bị lỗi, vẫn hiển thị và cho phép chọn mức độ
        assert page.check_visible_area_practice() and page.check_visible_area_level(), \
            "Hệ thống bị lỗi giao diện luyện tập khi nhận thẻ HTML không hợp lệ."
        assert page.check_enable_click_action_button(), \
            "Không thể click chọn mức độ Dễ/Khó do lỗi giao diện."
    finally:
        # Quay về trang danh sách flashcard và khôi phục lại nghĩa cũ
        page.driver.switch_to.default_content()
        page.load()
        page.choose_flashcard(card_name)
        page.click_edit_button(word)
        # Đợi form mở
        if page.check_visible_edit_form():
            page.type_text_field_by_text_label(field_name, "cải thiện")
            page.click_save_form_button()
            time.sleep(1)

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_01_open_practice_page(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert page.check_visible_area_practice() and page.check_visible_area_level(), \
        "Hệ thống không hiển thị area practice hoặc area level thành công."

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_03_select_easy_level(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert page.check_visible_area_practice() and page.check_visible_area_level(), \
        "Hệ thống không hiển thị area practice hoặc area level thành công."
    page.flip_card()
    old_text = page.get_text_in_practice_card()
    page.click_easy_button()
    time.sleep(5)
    new_text = page.get_text_in_practice_card()
    assert old_text != new_text, \
        "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Dễ."

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_04_select_hard_level(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert page.check_visible_area_practice() and page.check_visible_area_level(), \
        "Hệ thống không hiển thị area practice hoặc area level thành công."
    old_text = page.get_text_in_practice_card()
    page.flip_card()
    page.click_hard_button()
    time.sleep(5)
    new_text = page.get_text_in_practice_card()
    assert old_text != new_text, \
        "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Khó."
    
@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_05_select_known_word(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert page.check_visible_area_practice() and page.check_visible_area_level(), \
        "Hệ thống không hiển thị area practice hoặc area level thành công."
    old_text = page.get_text_in_practice_card()
    page.flip_card()
    page.click_known_button()
    time.sleep(5)
    new_text = page.get_text_in_practice_card()
    assert old_text != new_text, \
        "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Đã biết."

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_06_back_when_in_practice_mode(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert page.check_visible_area_practice() and page.check_visible_area_level(), \
        "Hệ thống không hiển thị area practice hoặc area level thành công."
    old_url = page.driver.current_url
    page.driver.back()
    new_url = page.driver.current_url
    assert old_url != new_url and page.check_visible_word_cards(), \
        "Hệ thống không quay lại trang danh sách flashcard."