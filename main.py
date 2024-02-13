import argparse  # Import the argparse module


from text_aligner import TextAligner
from content_preprocessor import ContentPreprocessor
from exceptions import ChaosOverflow, RealignmentFailed


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
    jp_content = ContentPreprocessor(jp_content).preprocess_content()
    cn_content = ContentPreprocessor(cn_content).preprocess_content()

    print("\nPreprocessing completed. Proceeding to align the files.")

    # Creating an instance of the TextAlignment class to realign the texts
    aligner = TextAligner(jp_content, cn_content)
    try:
        # Test
        # raise ChaosOverflow(1000, 10)
        aligner.realign_texts()
    except ChaosOverflow as e:
        print("Realignment process ended due to Chaos Overflow:", e)
    except RealignmentFailed as e:
        print("Realignment process ended due to Exception:", e)
    except Exception as e:
        print("Realignment process ended due to unforeseen Exception:", e)
        raise e

    print("Removing duplicated error correction lines.")
    aligner.remove_duplicated_error_correction_lines()

    print("Proceeding to overwrite the original files with the processed content.")
    # Reconstruct the content from the lists
    jp_content = '\n'.join([sublist[0] for sublist in aligner.jp_lines])
    cn_content = '\n'.join([sublist[0] for sublist in aligner.cn_lines])

    # Overwrite the original files with the processed content
    write_file(jp_file_path, jp_content)
    write_file(cn_file_path, cn_content)

    print("Files have been processed and overwritten.\n\n-----\n")


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
