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
            print(f"Difference occurred at line {self.current_line + 1}.")

            # See if we can fix the alignment by adding an empty line before one of the lists
            # If one of the lines is empty, add an error correct line to the other list
            if self.is_line_empty(self.jp_lines[self.current_line]):
                print("JP line is empty. Adding an error correct line to the CN list.")
                self.insert_error_correction_line(self.cn_lines, self.current_line)
                self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
                self.current_line += 1
                continue
            elif self.is_line_empty(self.cn_lines[self.current_line]):
                print("CN line is empty. Adding an error correct line to the JP list.")
                self.insert_error_correction_line(self.jp_lines, self.current_line)
                self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
                self.current_line += 1
                continue
            # If both lines are not empty, we need to do further processing
            if self.current_line + 1 < len(self.jp_lines) and \
                    ('「' in self.jp_lines[self.current_line][0] and '」' not in self.jp_lines[self.current_line][0]):
                print("JP line is split. Adding an error correct line to the CN list.")
                self.cn_lines.insert(self.current_line, [';'])
                self.raise_chaos(CHAOS_RISE_ON_COMPLEX_LINE_FIX)
                self.current_line += 2
                continue
            elif self.current_line + 1 < len(self.cn_lines) and \
                    ('「' in self.cn_lines[self.current_line][0] and '」' not in self.cn_lines[self.current_line][0]):
                print("CN line is split. Adding an error correct line to the JP list.")
                self.jp_lines.insert(self.current_line, [';'])
                self.raise_chaos(CHAOS_RISE_ON_COMPLEX_LINE_FIX)
                self.current_line += 2
                continue

            raise RealignmentFailed(self.current_line, "Both lines are not empty.")

            # If all else fails, something went horribly wrong
            raise Exception(f"Something horribly wrong happened at line {self.current_line + 1}.\n")

        print("Realignment process completed successfully.")
        return

    def is_line_empty(self, line):
        return line[1:] == []

    # def handle_empty_line(self, empty_line_list, other_line_list):
    #     self.insert_error_correction_line(other_line_list, self.current_line)
    #     self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)

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
