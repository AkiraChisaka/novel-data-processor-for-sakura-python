from settings import *
from exceptions import *




class TextAlignment:
    """
    This class is used to align two lists of text lines.
    """

    def __init__(self, jp_lines, cn_lines):
        self.jp_lines = jp_lines
        self.cn_lines = cn_lines
        self.current_line = 0
        self.chaos = INITIAL_CHAOS

    def realign_texts(self):
        while self.current_line < len(self.jp_lines) and self.current_line < len(self.cn_lines):
            # TEST prints
            # print(f"Current line: {current_line + 1}")
            # print(f"self.chaos: {self.chaos}")

            # If the chaos intensity is too high, this means that the lists are too different and we should stop
            # print(f"self.chaos: {self.chaos}")
            # print(f"MAX_CHAOS_PERMITTED: {MAX_CHAOS_PERMITTED}")
            if self.chaos > MAX_CHAOS_PERMITTED:
                raise ChaosOverflow(self.chaos, self.current_line)

            # If the lines are the same, no further processing is needed
            if self.jp_lines[self.current_line][1:] == self.cn_lines[self.current_line][1:]:
                self.lower_chaos()
                self.current_line += 1
                continue

            # If the lines differ, we will see if we can fix the alignment by adding an empty line before one of the lists
            # We should do so for the list that does not currently have a line that's empty
            print(f"Difference occurred at line {self.current_line + 1}.")
            if self.jp_lines[self.current_line][1:] != [] and self.cn_lines[self.current_line][1:] != []:
                # TODO implement further processing to handle the case where both lines are not empty
                raise Exception(f"Could not realign the lists at line {self.current_line + 1}. Stopping the realignment process.\n")

            # If one of the lines is empty, add an error correct line to the other list
            elif self.jp_lines[self.current_line][1:] == []:
                print("JP line is empty. Adding an error correct line to the CN list.")
                self.cn_lines.insert(self.current_line, [';'])
                self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
                self.current_line += 1
                continue
            elif self.cn_lines[self.current_line][1:] == []:
                print("CN line is empty. Adding an error correct line to the JP list.")
                self.jp_lines.insert(self.current_line, [';'])
                self.raise_chaos(CHAOS_RISE_ON_SIMPLE_LINE_FIX)
                self.current_line += 1
                continue

            # If all else fails, something went horribly wrong
            raise Exception(f"Something horribly wrong happened at line {self.current_line + 1}.\n")

        print("Realignment process completed successfully.")
        return

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
