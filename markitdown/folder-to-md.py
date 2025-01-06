from markitdown import MarkItDown
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os


def choose_folder():
    root = Tk()
    root.withdraw()  # Hide the root window
    folder_path = askdirectory(title='Select Folder')
    root.destroy()
    return folder_path

def clean_md_file(md_content):
    lines = [line.replace('\n', ' ') for line in md_content.splitlines()]
    # count all lines, and remove all lines shorter than 20 chars that appear more than 10 times
    cleaned_lines = [line for line in lines if not (len(line) < 20 and lines.count(line) > 10)]
    # remove lines that contain no letters or numbers
    cleaned_lines = [line for line in cleaned_lines if any(char.isalnum() for char in line)]
    return '\n'.join(cleaned_lines)
        

def folder_to_md(folder_path, filename, rec):
    def convert_to_md(file_path):
        try:
            md = MarkItDown()
            return clean_md_file(md.convert(file_path).text_content)
        except Exception as e:
            return f"Error : {e}"

    def process_folder(folder_path, md_file, rec):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                print(f"converting : {os.path.basename(item_path)}")
                md_content = convert_to_md(item_path)
                md_file.write(f"# {item}\n\n")
                md_file.write(md_content)
                md_file.write("\n\n")
            elif os.path.isdir(item_path) and rec:
                md_file.write(f"## {item}\n\n")
                process_folder(item_path, md_file, rec)

    output_filename = f"{filename}.md"
    with open(output_filename, 'w', encoding='utf-8') as md_file:
        process_folder(folder_path, md_file, rec)


if __name__ == '__main__':
    folder_path = choose_folder()
    filename = input("name of the target markdown (folder name by default) : ")
    if filename == '':
        filename = folder_path.split('/')[-1]
    rec = input("include all subfolders recursively (y) : ")
    rec = rec.lower() == 'y' or rec.lower() == ''
    folder_to_md(folder_path, filename, rec)
