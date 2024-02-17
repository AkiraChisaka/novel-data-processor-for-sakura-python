from settings import ERROR_CORRECT_LINE_SYMBOL, INITIAL_CHAOS, MAX_CHAOS_PERMITTED, CHAOS_RISE_ON_SIMPLE_LINE_FIX, CHAOS_RISE_ON_COMPLEX_LINE_FIX, ANCHOR_SYMBOLS_QUOTE, ANCHOR_SYMBOLS_STAND_ALONE
from exceptions import ChaosOverflow, RealignmentFailed


class TextAligner:
    """
    This class is used to align two lists of text lines.
    """

    def __init__(self, jp_content, cn_content):
        # Initialize lists based on the content line count
        self.jp_lines = self.initialize_list_for_content(jp_content)
        self.cn_lines = self.initialize_list_for_content(cn_content)
        self.current_line_id = 0
        self.chaos = INITIAL_CHAOS
        self.likely_issue_line_id = 0
        self.untouched = True

        # Loop through each symbol and fill the lists with occurrences
        self.anchor_symbols = []
        for quote_pair in ANCHOR_SYMBOLS_QUOTE:
            self.anchor_symbols.extend(quote_pair)
        self.anchor_symbols.extend(ANCHOR_SYMBOLS_STAND_ALONE)

        for symbol in self.anchor_symbols:
            self.fill_list_with_anchors(self.jp_lines, symbol)
            self.fill_list_with_anchors(self.cn_lines, symbol)

    def realign_texts(self):
        while self.current_line_id < len(self.jp_lines) and self.current_line_id < len(self.cn_lines):
            # TEST prints
            # print(f"Current line: {current_line + 1}")
            # print(f"self.chaos: {self.chaos}")

            # If the chaos intensity is too high, this means that the lists are too different and we should stop
            if self.chaos > MAX_CHAOS_PERMITTED:
                raise ChaosOverflow(self.current_line_id, self.chaos, self.likely_issue_line_id)
            elif self.chaos <= 5:
                self.likely_issue_line_id = self.current_line_id

            # If the lines are the same, no further processing is needed
            if self.jp_lines[self.current_line_id][1:] == self.cn_lines[self.current_line_id][1:]:
                self.lower_chaos()
                self.current_line_id += 1
                continue

            # If the lines differ, we will need to do something about it
            print(f"\nDifference occurred at line {self.current_line_id + 1}.")
            self.untouched = False

            # See if we can fix the alignment by adding an empty line before one of the lists
            # If one of the lines is empty, add an error correct line to the other list
            if self.fix_simple_misalignment():
                continue

            # If both lines are not empty, we need to do further processing
            if self.fix_bracket_quotes_being_split():
                continue

            raise RealignmentFailed(self.current_line_id, "Both lines are not empty, and no simple fix is available.")

            # If all else fails, something went horribly wrong
            raise Exception(f"Something horribly wrong happened at line {self.current_line_id + 1}.\n")

        if self.untouched:
            print("[UNTOUCHED] No differences found between the two files. No realignment needed.")
        else:
            print("[SUCCESS] Realignment completed.")
        return

    def fix_bracket_quotes_being_split(self):
        for quote_symbols in ANCHOR_SYMBOLS_QUOTE:
            start_quote, end_quote = quote_symbols
            if start_quote in self.jp_lines[self.current_line_id] and end_quote not in self.jp_lines[self.current_line_id]:
                for end_line in range(self.current_line_id + 1, min(self.current_line_id + 6, len(self.jp_lines))):
                    if '」' in self.jp_lines[end_line]:
                        self.combine_lines(self.jp_lines, self.current_line_id, end_line)
                        self.raise_chaos(CHAOS_RISE_ON_COMPLEX_LINE_FIX)
                        return 1
                raise RealignmentFailed(self.current_line_id, "Quotes correction failed.")
            elif start_quote in self.cn_lines[self.current_line_id] and end_quote not in self.cn_lines[self.current_line_id]:
                for end_line in range(self.current_line_id + 1, min(self.current_line_id + 6, len(self.cn_lines))):
                    if end_quote in self.cn_lines[end_line]:
                        self.combine_lines(self.cn_lines, self.current_line_id, end_line)
                        self.raise_chaos(CHAOS_RISE_ON_COMPLEX_LINE_FIX)
                        return 1
                raise RealignmentFailed(self.current_line_id, "Quotes correction failed.")
        return 0

    @staticmethod
    def combine_lines(line_list, start_line_id, end_line_id):
        combined_line = [""]
        for line_id in range(start_line_id, end_line_id + 1):
            print(f"end_line_id: {end_line_id}, line_id: {line_id}")
            combined_line[0] += line_list[line_id][0]
            for symbol in line_list[line_id][1:]:
                if symbol not in combined_line:
                    combined_line.append(symbol)
        print(f"Combined line: {combined_line}")
        line_list[start_line_id:end_line_id + 1] = [combined_line]

    def fix_simple_misalignment(self):
        if self.is_line_empty(self.jp_lines[self.current_line_id]):
            print("JP line is empty. Adding an error correct line to the CN list.")
            self.insert_error_correction_line(self.cn_lines, self.current_line_id)
            self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
            return 1
        elif self.is_line_empty(self.cn_lines[self.current_line_id]):
            print("CN line is empty. Adding an error correct line to the JP list.")
            self.insert_error_correction_line(self.jp_lines, self.current_line_id)
            self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
            return 1
        return 0

    @staticmethod
    def insert_error_correction_line(line_list, current_line):
        line_list.insert(current_line, [ERROR_CORRECT_LINE_SYMBOL])

    def remove_duplicated_error_correction_lines(self):
        index = 0
        while index < len(self.jp_lines) and index < len(self.cn_lines):
            if self.jp_lines[index][0] == ERROR_CORRECT_LINE_SYMBOL and self.cn_lines[index][0] == ERROR_CORRECT_LINE_SYMBOL:
                del self.jp_lines[index]
                del self.cn_lines[index]
            else:
                index += 1

    def is_line_empty(self, line):
        return line[1:] == []

    def raise_chaos(self, increase=0):
        self.chaos += increase
        # print(f"Raising chaos by {increase}, current chaos: {self.chaos}")
        return

    def lower_chaos(self, decrease=1):
        self.chaos -= decrease
        if self.chaos < 0:
            self.chaos = 0
            return
        if decrease != 1:
            # print(f"Decreasing chaos by {decrease}, current chaos: {self.chaos}")
            return

    @staticmethod
    def initialize_list_for_content(content):
        lines = content.split('\n')
        # Initialize a list with an empty list for each line of content
        return [[line] for line in lines]

    @staticmethod
    def fill_list_with_anchors(content_lines, symbol):
        lines = [entry[0] for entry in content_lines]
        for index, line in enumerate(lines):
            if symbol in line:
                # Assuming you want to store the line itself or just mark the presence of the symbol
                content_lines[index].append(symbol)  # Or append(line) to store the whole line
