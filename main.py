import argparse  # Import the argparse module
import re  # Import the regular expressions module


from settings import *
from exceptions import *
from text_alignment import TextAlignment


def main():
    parser = argparse.ArgumentParser(description="Align Japanese and Chinese text files.")
    parser.add_argument("jp_file", help="The file path of the Japanese text file")
    parser.add_argument("cn_file", help="The file path of the Chinese text file")

    args = parser.parse_args()

    # Process the files based on the provided arguments
    core(args.jp_file, args.cn_file)


def core(jp_file_path, cn_file_path):
    print(f"\nBegin processing files:\n    {jp_file_path}\n    {cn_file_path}")

    # Read the content of both files
    jp_content = read_file(jp_file_path)
    cn_content = read_file(cn_file_path)

    # Process the content of both files
    jp_content = preprocess_content(jp_content)
    cn_content = preprocess_content(cn_content)

    print("\nPreprocessing completed. Proceeding to align the files.")

    # Initialize lists based on the content line count
    jp_lines = initialize_list_for_content(jp_content)
    cn_lines = initialize_list_for_content(cn_content)

    # Loop through each symbol and fill the lists with occurrences
    anchor_symbols = ["「", "」", "『", "』"]
    for symbol in anchor_symbols:
        fill_list_with_anchors(jp_lines, symbol)
        fill_list_with_anchors(cn_lines, symbol)

    # Print the processed lists
    # print("\nJP List:")
    # print_list_readable(jp_lines)
    # print("\nCN List:")
    # print_list_readable(cn_lines)

    aligner = TextAlignment(jp_lines, cn_lines)

    try:
        # Test
        # raise ChaosOverflow(1000, 10)
        aligner.realign_texts()
    except ChaosOverflow as e:
        print("Realignment process ended due to Chaos Overflow:", e)
    except Exception as e:
        print("Realignment process ended due to Exception:", e)
        raise e

    print("Proceeding to overwrite the original files with the processed content.")

    # Reconstruct the content from the lists
    jp_content = '\n'.join([sublist[0] for sublist in jp_lines])
    cn_content = '\n'.join([sublist[0] for sublist in cn_lines])

    # Overwrite the original files with the processed content
    write_file(jp_file_path, jp_content)
    write_file(cn_file_path, cn_content)

    print("Files have been processed and overwritten.\n\n-----\n")


# def realign_texts(jp_lines, cn_lines, current_line=0, chaos=INITIAL_CHAOS):
#     while current_line < len(jp_lines) and current_line < len(cn_lines):
#         # TEST prints
#         # print(f"Current line: {current_line + 1}")
#         # print(f"Chaos: {chaos}")

#         # If the chaos intensity is too high, this means that the lists are too different and we should stop
#         if chaos > MAX_CHAOS_PERMITTED:
#             raise ChaosOverflow(chaos, current_line)

#         # If the lines are the same, no further processing is needed
#         if jp_lines[current_line][1:] == cn_lines[current_line][1:]:
#             chaos = lower_chaos(chaos)
#             current_line += 1
#             continue

#         # If the lines differ, we will see if we can fix the alignment by adding an empty line before one of the lists
#         # We should do so for the list that does not currently have a line that's empty
#         print(f"Difference occurred at line {current_line + 1}.")
#         if jp_lines[current_line][1:] != [] and cn_lines[current_line][1:] != []:
#             # TODO implement further processing to handle the case where both lines are not empty
#             raise Exception(f"Could not realign the lists at line {current_line + 1}. Stopping the realignment process.\n")

#         # If one of the lines is empty, add an error correct line to the other list
#         elif jp_lines[current_line][1:] == []:
#             print("JP line is empty. Adding an error correct line to the CN list.")
#             cn_lines.insert(current_line, [';'])
#             chaos = raise_chaos(chaos, CHAOS_RISE_ON_SIMPLE_LINE_FIX)
#             current_line += 1
#             continue
#         elif cn_lines[current_line][1:] == []:
#             print("CN line is empty. Adding an error correct line to the JP list.")
#             jp_lines.insert(current_line, [';'])
#             chaos = raise_chaos(chaos, CHAOS_RISE_ON_SIMPLE_LINE_FIX)
#             current_line += 1
#             continue

#         # If all else fails, something went horribly wrong
#         raise Exception(f"Something horribly wrong happened at line {current_line + 1}.\n")

#     print("Realignment process completed successfully.")
#     return


# def raise_chaos(chaos, increase=0):
#     new_chaos = chaos + increase
#     print(f"Raising chaos by {increase}, current chaos: {new_chaos}")
#     return new_chaos


# def lower_chaos(chaos, decrease=1):
#     new_chaos = chaos - decrease
#     if new_chaos < 0:
#         new_chaos = 0
#     if decrease != 1:
#         print(f"Decreasing chaos by {decrease}, current chaos: {new_chaos}")
#     return new_chaos


def initialize_list_for_content(content):
    lines = content.split('\n')
    # Initialize a list with an empty list for each line of content
    return [[line] for line in lines]


def fill_list_with_anchors(content_lines, symbol):
    lines = [entry[0] for entry in content_lines]
    for index, line in enumerate(lines):
        if symbol in line:
            # Assuming you want to store the line itself or just mark the presence of the symbol
            content_lines[index].append(symbol)  # Or append(line) to store the whole line


def read_file(file_path):
    # Read and return the content of a file
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, content):
    # For testing purposes, use a different file name to avoid overwriting the original file
    # file_path = file_path.replace('.txt', '_processed.txt')
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
