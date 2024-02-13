from settings import ERROR_CORRECT_LINE_SYMBOL
from text_aligner import TextAligner


def test_initialize_list_for_content():
    content = "line1\nline2\nline3"
    aligner = TextAligner(content, content)
    expected = [['line1'], ['line2'], ['line3']]
    assert aligner.initialize_list_for_content(content) == expected


def test_fill_list_with_anchors_auto():
    content = "line1\n「line2」\nline3"
    # Initialize the list with the content should automatically fill the list with anchors as specified by settings.py
    aligner = TextAligner(content, content)
    expected = [['line1'], ['「line2」', '「', '」'], ['line3']]
    assert aligner.jp_lines == expected


def test_is_line_empty():
    aligner = TextAligner("", "")
    assert aligner.is_line_empty(['']) == True
    assert aligner.is_line_empty(['text']) == True
    assert aligner.is_line_empty(['', '「', '」']) == False


def test_insert_error_correction_line():
    aligner = TextAligner("", "")
    aligner.insert_error_correction_line(aligner.jp_lines, 0)
    assert aligner.jp_lines[0] == [ERROR_CORRECT_LINE_SYMBOL]
    aligner.insert_error_correction_line(aligner.cn_lines, 0)
    assert aligner.cn_lines[0] == [ERROR_CORRECT_LINE_SYMBOL]
