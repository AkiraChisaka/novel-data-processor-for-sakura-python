import re


class ContentPreprocessor:
    def __init__(self, content):
        self.content = content

    def preprocess_content(self):
        # Temporarily add a newline at the start and end of the content
        self.content = '\n' + self.content + '\n'

        # Apply content processing
        self.remove_multiple_newlines()
        self.remove_surrounding_symbols(' ')  # For regular spaces
        self.remove_surrounding_symbols('　')  # For Japanese full-width spaces

        # Remove the temporarily added newlines at the start and end
        self.content = self.content[1:-1]

        return self.content

    def remove_multiple_newlines(self):
        # Use a regular expression to replace two or more consecutive newlines with a single newline
        self.content = re.sub(r'\n{2,}', '\n', self.content)

    def remove_surrounding_symbols(self, symbol):
        # Use a regular expression to remove the specified symbol before and after each newline
        # This pattern targets the symbol occurring at the end of a line before a newline
        # and at the start of a line after a newline
        pattern = re.escape(symbol) + r'?\n' + re.escape(symbol) + r'?'
        self.content = re.sub(pattern, '\n', self.content)