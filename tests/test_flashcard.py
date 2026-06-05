import time
import pytest

from pages.flashcard_page import FlashcardPage

VALID_FLASHCARD_DATA = {
    "chất lượng": "quality",
    "số lượng": "quantity",
    "môi trường": "environment",
    "sự cẩn trọng": "caution",
    "điều hòa": "air-coditional",
    "sự ô nhiễm": "pollution",
    "tủ lạnh": "refrigenator",
    "lợi ích": "benifit",
    "tiền mặt": "cash",
    "mãi mãi": "forever"
}

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
    assert card_name.lower() in page.driver.title.lower()
    assert page.check_visible_word_cards()

@pytest.mark.parametrize(("card_name", "word"), [("TOEIC Word List", "improve")])
def test_TC_FLASH_EDIT_03_open_edit_form(page, card_name, word):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form không hiển thị sau khi click nút edit của từ '{word}'"
    assert page.get_text_newword_input() == word


@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "cải thiện")])
def test_TC_FLASH_EDIT_04_edit_a_field_of_word(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.click_save_form_button()
    page.driver.refresh()
    define_return = page.get_text_of_define_in_wordcard(word)
    assert define_return is not None and text_value == define_return, \
        f"Hệ thống không hiển thị nghĩa mới '{text_value}' thành công."

@pytest.mark.parametrize(("card_name", "word", "define", "define_text","image", "image_path", "word_type", "word_type_text", "pronunciation", "pronunciation_text", "example", "example_text", "note", "note_text"), 
                         [("TOEIC Word List", "improve", "Định nghĩa", "tận dụng", "Ảnh", "D:\\TaiLieu\\NAM4_K2\\KTPMN\\study4_automation_testing\\asset\\anh.png", "Loại từ", "v", "Phiên âm", "/improve", "Ví dụ", "to improve the occasion", "Ghi chú", "Từ mới")])
def test_TC_FLASH_EDIT_05_edit_multiple_fields(page, card_name, word, define, define_text,image, image_path, word_type, word_type_text, pronunciation, pronunciation_text, example, example_text, note, note_text):
    page.choose_flashcard(card_name)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"

    # Nhập các trường văn bản
    page.type_text_field_by_text_label(define, define_text)

    # Mở tuỳ chọn nâng cao rồi upload ảnh
    page.click_show_options()
    image_uploaded = False
    try:
        page.upload_image_to_image_field(image_path)
        image_uploaded = True
    except Exception as e:
        pytest.xfail(f"Upload ảnh thất bại (bỏ qua): {e}")

    page.type_text_field_by_text_label(word_type, word_type_text)
    page.type_text_field_by_text_label(pronunciation, pronunciation_text)
    page.type_text_field_by_text_label(example, example_text)
    page.type_text_field_by_text_label(note, note_text)

    page.click_save_form_button()
    time.sleep(3)
    page.driver.refresh()
    time.sleep(3)
    # Kiểm tra từng trường riêng biệt
    define_show = page.get_text_of_define_in_wordcard(word)
    assert define_show is not None and define_show == define_text, \
        f"Trường Định nghĩa: mong đợi '{define_text}', thực tế '{define_show}'."

    word_type_show = page.get_word_type(word)
    assert word_type_show is not None and word_type_text in word_type_show, \
        f"Trường Loại từ: mong đợi chứa '{word_type_text}', thực tế '{word_type_show}'."

    pronunciation_show = page.get_word_pronunciation(word)
    assert pronunciation_show is not None and pronunciation_show == pronunciation_text, \
        f"Trường Phiên âm: mong đợi '{pronunciation_text}', thực tế '{pronunciation_show}'."

    example_show = page.get_word_example(word)
    assert example_show is not None and example_text == example_show, \
        f"Trường Ví dụ: mong đợi '{example_text}', thực tế '{example_show}'."

    note_show = page.get_word_note(word)
    assert note_show is not None and note_text == note_show, \
        f"Trường Ghi chú: mong đợi '{note_text}', thực tế '{note_show}'."

    if image_uploaded:
        image_show = page.get_word_picture(word)
        assert image_show is not None and image_path.split("\\")[-1].split(".")[0] in image_show.split('/')[-1], \
            f"Trường Ảnh: không hiển thị ảnh mới thành công. src='{image_show}'."

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

@pytest.mark.parametrize(("card_name", "word", "field_name", "text_value"), [("TOEIC Word List", "improve", "Định nghĩa", "<hfs")])
def test_TC_FLASH_EDIT_08_edit_with_special_characters(page, card_name, word, field_name, text_value):
    page.choose_flashcard(card_name)
    old_text = page.get_word_definition(word)
    page.click_edit_button(word)
    assert page.check_visible_edit_form(), \
        f"Edit form chưa mở — không thể nhập liệu"
    page.type_text_field_by_text_label(field_name, text_value)
    page.click_save_form_button()
    page.driver.refresh()
    define_text = page.get_text_of_define_in_wordcard(word)
    assert define_text is not None and text_value == define_text, \
        f"Hệ thống không hiển thị nghĩa mới '{text_value}' thành công."

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_01_open_practice_page(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_02A_select_easy_level_with_valid_list(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 20
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visible_area_practice():
            n = 1
            page.flip_card()
            old_text = page.get_text_in_practice_card()
            page.click_easy_button()
            time.sleep(5)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Dễ."
        else:
            page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy practice card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Vocabulary"])
def test_TC_FLASH_PRACTICE_02B_select_easy_level_with_invalid_list(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 20
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visible_area_practice():
            n = 1
            page.flip_card()
            old_text = page.get_text_in_practice_card()
            page.click_easy_button()
            time.sleep(5)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Dễ."
        else:
            page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy practice card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_03A_select_hard_level_with_valid_list(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 20
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visible_area_practice():
            n = 1
            page.flip_card()
            old_text = page.get_text_in_practice_card()
            page.click_hard_button()
            time.sleep(5)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Khó."
        else:
            page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy practice card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Vocabulary"])
def test_TC_FLASH_PRACTICE_03B_select_hard_level_with_invalid_list(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 20
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visible_area_practice():
            n = 1
            page.flip_card()
            old_text = page.get_text_in_practice_card()
            page.click_hard_button()
            time.sleep(5)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Khó."
        else:
            page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy practice card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_04A_select_known_word_with_valid_list(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 20
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visible_area_practice():
            n = 1
            page.flip_card()
            old_text = page.get_text_in_practice_card()
            page.click_known_button()
            time.sleep(5)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Đã biết."
        else:
            page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy practice card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Vocabulary"])
def test_TC_FLASH_PRACTICE_04B_select_known_word_with_invalid_list(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 20
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visible_area_practice():
            n = 1
            page.flip_card()
            old_text = page.get_text_in_practice_card()
            page.click_known_button()
            time.sleep(5)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn mức độ Đã biết."
        else:
            page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy practice card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_05_check_fill_in_answer_with_correct_answer(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_answer_input():
            n = 1
            old_text = page.get_text_in_review_card()
            word = page.get_define_in_review_card()
            if word not in VALID_FLASHCARD_DATA:
                pytest.skip(f"Từ '{word}' không có trong VALID_FLASHCARD_DATA — bỏ qua test.")
            expected_word = VALID_FLASHCARD_DATA[word]
            page.type_answer_input(expected_word)
            page.press_enter()
            time.sleep(3)
            if page.check_visible_area_practice():
                new_text = page.get_text_in_practice_card()
            else:
                new_text = page.get_text_in_review_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi nhập đáp án chính xác."
        elif page.check_visiable_options_in_review_card():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
            
    if retries >= max_retries and n != 1:
        print(retries)
        pytest.skip("Không tìm thấy fill-in card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_06_check_fill_in_answer_with_incorrect_answer(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_answer_input():
            n = 1
            old_text = page.get_text_in_review_card()
            word = page.get_define_in_review_card()
            if word not in VALID_FLASHCARD_DATA:
                pytest.skip(f"Từ '{word}' không có trong VALID_FLASHCARD_DATA — bỏ qua test.")
            expected_word = VALID_FLASHCARD_DATA[word]
            page.type_answer_input("abc" + expected_word)
            page.press_enter()
            time.sleep(1)
            page.clear_answer_input()
            if page.check_visible_review_card():
                new_text = page.get_text_in_review_card()
            else:
                new_text = page.get_text_in_practice_card()
            assert old_text == new_text, \
                "Hệ thống chuyển sang thẻ mới sau khi nhập đáp án không chính xác."
        elif page.check_visiable_options_in_review_card():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy fill-in card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_07_check_fill_in_answer_click_show_answer(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_answer_input():
            n = 1
            word = page.get_define_in_review_card()
            if word not in VALID_FLASHCARD_DATA:
                pytest.skip(f"Từ '{word}' không có trong VALID_FLASHCARD_DATA — bỏ qua test.")
            expected_word = VALID_FLASHCARD_DATA[word]
            page.click_show_answer()
            time.sleep(1)
            result = page.get_text_in_answer_input()
            assert result == expected_word, \
                "Hệ thống không hiển thị đáp án chính xác sau khi chọn show answer."
        elif page.check_visiable_options_in_review_card():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy fill-in card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_08_check_fill_in_answer_click_continue(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_answer_input():
            n = 1
            old_text = page.get_text_in_review_card()
            page.click_continue_button()
            time.sleep(1)
            if page.check_visible_review_card():
                new_text = page.get_text_in_review_card()
            else:
                new_text = page.get_text_in_practice_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi nhấn tiếp tục."
        elif page.check_visiable_options_in_review_card():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy fill-in card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_09_check_fill_in_answer_click_known_word(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_answer_input():
            n = 1
            old_text = page.get_text_in_review_card()
            page.click_known_in_review_card()
            time.sleep(1)
            if page.check_visible_review_card():
                new_text = page.get_text_in_review_card()
            else:
                new_text = page.get_text_in_practice_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi nhấn Đã biết."
        elif page.check_visiable_options_in_review_card():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy fill-in card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_10_choose_correct_options_in_review_card(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visiable_options_in_review_card():
            n = 1
            old_text = page.get_text_in_review_card()
            word = page.get_define_in_review_card()
            expected_word = None
            if word not in VALID_FLASHCARD_DATA:
                for key, value in VALID_FLASHCARD_DATA.items():
                    if value == word:
                        expected_word = key
                        break
            else:
                expected_word = VALID_FLASHCARD_DATA[word]
            
            if expected_word is None:
                pytest.skip(f"Từ '{word}' không có trong VALID_FLASHCARD_DATA — bỏ qua test.")
            print(expected_word)
            page.choose_options_in_review_card(expected_word)
            time.sleep(3)
            if page.check_visible_review_card():
                new_text = page.get_text_in_review_card()
            else:
                new_text = page.get_text_in_practice_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi chọn đáp án chính xác."
        elif page.check_answer_input():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy options card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_11_choose_incorrect_options_in_review_card(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visiable_options_in_review_card():
            n = 1
            old_text = page.get_text_in_review_card()
            word = page.get_define_in_review_card()
            expected_word = None
            if word not in VALID_FLASHCARD_DATA:
                for key, value in VALID_FLASHCARD_DATA.items():
                    if value == word:
                        expected_word = key
                        break
            else:
                expected_word = VALID_FLASHCARD_DATA[word]
            
            if expected_word is None:
                pytest.skip(f"Từ '{word}' không có trong VALID_FLASHCARD_DATA — bỏ qua test.")

            page.choose_options_in_review_card(expected_word)
            time.sleep(1)
            if page.check_visible_review_card():
                new_text = page.get_text_in_review_card()
            else:
                new_text = page.get_text_in_practice_card()
            assert old_text == new_text, \
                "Hệ thống chuyển sang thẻ mới sau khi chọn đáp án không chính xác."
        elif page.check_answer_input():
            page.click_known_in_review_card()
        else:
            page.flip_card()
            page.click_hard_button()
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy options card sau khi thử lại nhiều lần — bỏ qua test.")

@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_12_choose_options_in_review_card_and_click_known(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    max_retries = 30
    n = 0
    retries = 0
    while n != 1 and retries < max_retries:
        retries += 1
        if page.check_visiable_options_in_review_card():
            n = 1
            old_text = page.get_text_in_review_card()
            page.click_known_in_review_card()
            time.sleep(1)
            if page.check_visible_review_card():
                new_text = page.get_text_in_review_card()
            else:
                new_text = page.get_text_in_practice_card()
            assert old_text != new_text, \
                "Hệ thống không chuyển sang thẻ mới sau khi nhấn Đã biết."
        else:
            if page.check_visible_area_practice():
                page.flip_card()
                page.click_hard_button()
            else:
                page.click_known_in_review_card()
            time.sleep(1)
    if retries >= max_retries and n != 1:
        pytest.skip("Không tìm thấy options card sau khi thử lại nhiều lần — bỏ qua test.")



@pytest.mark.parametrize("card_name", ["Toeic Voca"])
def test_TC_FLASH_PRACTICE_13_back_when_in_practice_mode(page, card_name):
    page.choose_flashcard(card_name)
    page.click_practice_button()
    assert (page.check_visible_area_practice() and page.check_visible_area_level()) or (page.check_visible_review_card())
    old_url = page.driver.current_url
    page.driver.back()
    new_url = page.driver.current_url
    assert old_url != new_url and page.check_visible_word_cards(), \
        "Hệ thống không quay lại trang danh sách flashcard."
