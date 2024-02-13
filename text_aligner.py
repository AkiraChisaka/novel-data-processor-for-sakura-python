from settings import INITIAL_CHAOS, ANCHOR_SYMBOLS, MAX_CHAOS_PERMITTED, CHAOS_RISE_ON_SIMPLE_LINE_FIX, CHAOS_RISE_ON_COMPLEX_LINE_FIX
from exceptions import ChaosOverflow, RealignmentFailed


class TextAligner:
    """
    This class is used to align two lists of text lines.
    """

    def __init__(self, jp_content, cn_content):
        # Initialize lists based on the content line count
        self.jp_lines = self.initialize_list_for_content(jp_content)
        self.cn_lines = self.initialize_list_for_content(cn_content)
        self.current_line = 0
        self.chaos = INITIAL_CHAOS

        # Loop through each symbol and fill the lists with occurrences
        self.anchor_symbols = ANCHOR_SYMBOLS
        for symbol in self.anchor_symbols:
            self.fill_list_with_anchors(self.jp_lines, symbol)
            self.fill_list_with_anchors(self.cn_lines, symbol)

    def realign_texts(self):
        while self.current_line < len(self.jp_lines) and self.current_line < len(self.cn_lines):
            # TEST prints
            # print(f"Current line: {current_line + 1}")
            # print(f"self.chaos: {self.chaos}")

            # If the chaos intensity is too high, this means that the lists are too different and we should stop
            if self.chaos > MAX_CHAOS_PERMITTED:
                raise ChaosOverflow(self.current_line, self.chaos)

            # If the lines are the same, no further processing is needed
            if self.jp_lines[self.current_line][1:] == self.cn_lines[self.current_line][1:]:
                self.lower_chaos()
                self.current_line += 1
                continue

            # If the lines differ, we will need to do something about it
            print(f"\nDifference occurred at line {self.current_line + 1}.")

            # See if we can fix the alignment by adding an empty line before one of the lists
            # If one of the lines is empty, add an error correct line to the other list
            if self.fix_one_side_being_empty():
                continue

            # If both lines are not empty, we need to do further processing
            # TODO LMAO

            raise RealignmentFailed(self.current_line, "Both lines are not empty, and no simple fix is available.")

            # If all else fails, something went horribly wrong
            raise Exception(f"Something horribly wrong happened at line {self.current_line + 1}.\n")

        print("Realignment process completed successfully.")
        return

    def fix_one_side_being_empty(self):
        if self.is_line_empty(self.jp_lines[self.current_line]):
            print("JP line is empty. Adding an error correct line to the CN list.")
            self.insert_error_correction_line(self.cn_lines, self.current_line)
            self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
            self.current_line += 1
            return 1
        elif self.is_line_empty(self.cn_lines[self.current_line]):
            print("CN line is empty. Adding an error correct line to the JP list.")
            self.insert_error_correction_line(self.jp_lines, self.current_line)
            self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
            self.current_line += 1
            return 1
        else:
            return 0

    def remove_duplicated_error_correction_lines(self):
        index = 0
        while index < len(self.jp_lines) and index < len(self.cn_lines):
            if self.jp_lines[index] == [';'] and self.cn_lines[index] == [';']:
                del self.jp_lines[index]
                del self.cn_lines[index]
            else:
                index += 1

    def is_line_empty(self, line):
        return line[1:] == []

    def raise_chaos(self, increase=0):
        self.chaos += increase
        print(f"Raising chaos by {increase}, current chaos: {self.chaos}")
        return

    def lower_chaos(self, decrease=1):
        self.chaos -= decrease
        if self.chaos < 0:
            self.chaos = 0
            return
        if decrease != 1:
            print(f"Decreasing chaos by {decrease}, current chaos: {self.chaos}")
            return

    @staticmethod
    def insert_error_correction_line(line_list, current_line):
        line_list.insert(current_line, [';'])

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
