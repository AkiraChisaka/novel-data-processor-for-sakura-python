import argparse  # Import the argparse module
import re  # Import the regular expressions module


def main():
    parser = argparse.ArgumentParser(description="Align Japanese and Chinese text files.")
    parser.add_argument("jp_file", help="The file path of the Japanese text file")
    parser.add_argument("cn_file", help="The file path of the Chinese text file")

    args = parser.parse_args()

    # Process the files based on the provided arguments
    core(args.jp_file, args.cn_file)


def core(jp_file_path, cn_file_path):
    print(f"Processing files: {jp_file_path} and {cn_file_path}")

    # Read the content of both files
    jp_content = read_file(jp_file_path)
    cn_content = read_file(cn_file_path)

    # Process the content of both files
    jp_content = preprocess_content(jp_content)
    cn_content = preprocess_content(cn_content)

    # Initialize lists based on the content line count
    jp_lines = initialize_list_for_content(jp_content)
    cn_lines = initialize_list_for_content(cn_content)

    # Loop through each symbol and fill the lists with occurrences
    anchor_symbols = ["「", "」", "『", "』"]
    for symbol in anchor_symbols:
        fill_list_with_anchors(jp_content, jp_lines, symbol)
        fill_list_with_anchors(cn_content, cn_lines, symbol)

    # Print the processed lists
    print("\nJP List:")
    print_list_readable(jp_lines)
    print("\nCN List:")
    print_list_readable(cn_lines)

    # Overwrite the original files with the processed content
    write_file(jp_file_path, jp_content)
    write_file(cn_file_path, cn_content)

    print("Files have been processed and overwritten with cleaned content.")


def realign_texts(jp_content, cn_content, jp_list, cn_list):
    # Convert content back to lists of lines for easy manipulation
    jp_lines = jp_content.split('\n')
    cn_lines = cn_content.split('\n')


def initialize_list_for_content(content):
    lines = content.split('\n')
    # Initialize a list with an empty list for each line of content
    return [[line] for line in lines]


def fill_list_with_anchors(content, content_line, symbol):
    lines = content.split('\n')
    for index, line in enumerate(lines):
        if symbol in line:
            # Assuming you want to store the line itself or just mark the presence of the symbol
            content_line[index].append(symbol)  # Or append(line) to store the whole line


def read_file(file_path):
    # Read and return the content of a file
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, content):
    # Overwrite a file with the given content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def preprocess_content(content):
    # Temporarily add a newline at the start and end of the content
    content = '\n' + content + '\n'

    # Apply content processing
    content = remove_multiple_newlines(content)
    content = remove_surrounding_symbols(content, ' ')  # For regular spaces
    content = remove_surrounding_symbols(content, '　')  # For Japanese full-width spaces

    # Remove the temporarily added newlines at the start and end
    content = content[1:-1]

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


def print_list_readable(lst):
    max_line_number = len(str(len(lst)))  # Get the maximum number of digits in the line number
    for index, sublist in enumerate(lst):
        if len(sublist) > 1:
            line_number = index + 1
            print(f"Line {line_number:>{max_line_number}}: ", end="")
            for item in sublist[1:]:
                print(item, end=" ")
            print()


if __name__ == "__main__":
    main()
