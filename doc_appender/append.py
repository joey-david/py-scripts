import PyPDF2
import sys
import os
import time
import tkinter as tk
from tkinter import filedialog

def append_pdf(input_pdf_path, output_pdf_path):
    # Create a PDF file reader object for the input PDF
    input_pdf = PyPDF2.PdfReader(open(input_pdf_path, "rb"))
    
    # Create a PDF file writer object for the output PDF
    output_pdf = PyPDF2.PdfWriter()
    
    # Read the existing output PDF
    with open(output_pdf_path, "rb") as output_file:
        existing_pdf = PyPDF2.PdfReader(output_file)
        for page_num in range(len(existing_pdf.pages)):
            output_pdf.add_page(existing_pdf.pages[page_num])
    
    # Append the input PDF to the output PDF
    for page_num in range(len(input_pdf.pages)):
        output_pdf.add_page(input_pdf.pages[page_num])
    
    # Write the combined PDF to the output file
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

def main():
    directory_to_watch = "."
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    specific_pdf_path = filedialog.askopenfilename(
        title="Select the report PDF",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not specific_pdf_path:
        print("No file selected. Exiting.")
        sys.exit(1)
    already_seen_files = set(os.listdir(directory_to_watch))

    while True:
        current_files = set(os.listdir(directory_to_watch))
        new_files = current_files - already_seen_files

        for new_file in new_files:
            new_file_path = os.path.join(directory_to_watch, new_file)
            if new_file_path.endswith(".pdf"):
                append_pdf(specific_pdf_path, new_file_path)
                print(f"Appended {specific_pdf_path} to {new_file_path}")

        already_seen_files = current_files
        time.sleep(5)

if __name__ == "__main__":
    main()