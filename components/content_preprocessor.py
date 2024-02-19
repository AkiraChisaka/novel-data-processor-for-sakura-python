import re

from settings import ERROR_CORRECT_LINE_SYMBOL, REPLACEMENT_SYMBOLS, SURROUNDING_SPACES


class ContentPreprocessor:
    def __init__(self, content):
        self.content = content

    def preprocess_content(self):
        # Temporarily add a newline at the start and end of the content
        self.content = '\n' + self.content + '\n'

        # Apply content processing
        self.remove_surrounding_spaces()
        self.remove_error_correction_lines()
        self.remove_multiple_newlines()
        self.replace_symbols()

        # Remove the temporarily added newlines at the start and end
        self.content = self.content[1:-1]

        return self.content

    def remove_multiple_newlines(self):
        # Use a regular expression to replace two or more consecutive newlines with a single newline
        self.content = re.sub(r'\n{2,}', '\n', self.content)
    
    def remove_surrounding_spaces(self):
        # Use a regular expression to remove spaces before and after each newline
        for symbol in SURROUNDING_SPACES:
            while self.remove_surrounding_symbol(symbol):
                pass

    def remove_surrounding_symbol(self, symbol):
        # Use a regular expression to remove the specified symbol before and after each newline
        # This pattern targets the symbol occurring at the end of a line before a newline
        # and at the start of a line after a newline
        pattern = re.escape(symbol) + r'?\n' + re.escape(symbol) + r'?'
        old_length = len(self.content)
        self.content = re.sub(pattern, '\n', self.content)
        new_length = len(self.content)
        return old_length != new_length

    def remove_error_correction_lines(self):
        # Use a regular expression to match lines containing only a semicolon
        # '^' matches the start of a line, '\s*' matches any number of whitespace characters,
        # ';' matches the semicolon, '\s*$' matches any number of whitespace characters at the end of a line
        self.content = re.sub(rf'^\s*{re.escape(ERROR_CORRECT_LINE_SYMBOL)}\s*$', '', self.content, flags=re.MULTILINE)

    def replace_symbols(self):
        for old_symbol, new_symbol in REPLACEMENT_SYMBOLS.items():
            self.replace_symbol(old_symbol, new_symbol)

    def replace_symbol(self, old_symbol, new_symbol):
        # Use a regular expression to replace all occurrences of old_symbol with new_symbol
        self.content = re.sub(re.escape(old_symbol), new_symbol, self.content)
