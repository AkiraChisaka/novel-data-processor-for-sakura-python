import argparse  # Import the argparse module
import re  # Import the regular expressions module


def main():
    parser = argparse.ArgumentParser(description="Align Japanese and Chinese text files.")
    parser.add_argument("jp_file", help="The file path of the Japanese text file")
    parser.add_argument("cn_file", help="The file path of the Chinese text file")

    args = parser.parse_args()

    # Process the files based on the provided arguments
    process_files(args.jp_file, args.cn_file)


def process_files(jp_file_path, cn_file_path):
    print(f"Processing files: {jp_file_path} and {cn_file_path}")

    # Read the content of both files
    jp_content = read_file(jp_file_path)
    cn_content = read_file(cn_file_path)

    # Process the content of both files
    jp_content = preprocess_content(jp_content)
    cn_content = preprocess_content(cn_content)

    # Overwrite the original files with the processed content
    write_file(jp_file_path, jp_content)
    write_file(cn_file_path, cn_content)

    print("Files have been processed and overwritten with cleaned content.")


def read_file(file_path):
    # Read and return the content of a file
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, content):
    # Overwrite a file with the given content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def preprocess_content(content):
    # Apply any content processing, starting with removing multiple newlines
    content = remove_multiple_newlines(content)
    # Remove spaces and Japanese spaces surrounding newlines
    content = remove_surrounding_symbols(content, ' ')  # For regular spaces
    content = remove_surrounding_symbols(content, '　')  # For Japanese full-width spaces

    return content


def remove_multiple_newlines(content):
    # Use a regular expression to replace two or more consecutive newlines with a single newline
    return re.sub(r'\n{2,}', '\n', content)


def remove_surrounding_symbols(content, symbol):
    # Use a regular expression to remove the specified symbol before and after each newline
    # This pattern targets the symbol occurring at the end of a line before a newline
    # and at the start of a line after a newline
    pattern = re.escape(symbol) + r'?\n' + re.escape(symbol) + r'?'
    return re.sub(pattern, '\n', content)


if __name__ == "__main__":
    main()
