import os

def search_files(directory, symbol):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f, 1):
                        if symbol in line:
                            print(f"Found in: {file_path}, Line: {line_number}")

# Replace 'path_to_your_directory' with the path to the directory containing your text files
search_files(r'D:\AI\SakuraLLM\Repos\sizefetish-jp2cn-translated-text\2.1 Text Prepared without Dict', ';')