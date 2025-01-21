# CSV to PDF Tool

## Description
CSV to PDF Tool is a Python-based script that converts an exported CSV, or Comma Separated Values, document to a clean, customized, and printable PDF. It allows the user to select which fields from the CSV to include and determine the name of the new PDF file. The data is sorted and a neatly formatted PDF with a table layout is generated and saved to the Desktop. The tool also ensures that potentially sensitive files, like the temporary CSV, are removed after generating the PDF to maintain data security.

## Features
- Converts CSV exports to printable PDFs.
- Customizable field selection for CSV data.
- Customizable PDF file name.
- Alphabetically sorts the CSV data based on the first selected field.
- Cleans up long URLs, ensuring they are displayed in a concise format.
- Automatically deletes the temporary CSV file after creating the PDF.
- Provides terminal-based interaction, including validation, feedback, and file management.
- ASCII art banner and colored text for enhanced user experience in the terminal.

## Requirements
This script requires the following Python packages:

- Python 3.x
- fpdf (for generating PDF)
- colorama (for color terminal output)
- pyfiglet (for ASCII art banners)

You can install the external packages using the following pip commands:
```
pip install fpdf colorama pyfiglet
```

## Usage
- Export your data as a CSV file and save it to your Downloads folder.
- Run the Python script, and it will prompt you to enter the name of the CSV file.
- The program will validate the file, extract the fieldnames, and allow you to select which ones to include in the PDF.
- At the prompt, enter a new name for your PDF file.
- The data is cleaned, sorted, and written to a new CSV file.
- A PDF is created from this data and saved to your Desktop.
- The temporary CSV file is deleted after the PDF is generated.
- At the final prompt, you can choose to start again with a new file or exit the program.

### Example
```
python csv_to_pdf_tool.py
```
## Future Features under Consideration
- Integrate a GUI for enhanced user experience, particularly with non-technical users.
- Overwrite functionality before deletion for more secure file handling.
- Dynamically adjusted column widths in the PDF for better formatting.
- Improve input validation and error handling.
- Include additional data cleaning beyond URLs, such as phone numbers.
- Add password encryption to the PDF for enhanced security.
- More robust unit testing to ensure reliability and catch edge cases.
- Update and expand upon "Usage" section of this README.
- Add case study explaining my process, challenges faced, and how the project evolved to solve real-world problems. 

## Get in Touch
If you have any questions, suggestions, or want to contribute to this project, feel free to reach out:

Email: christa.tech@outlook.com

GitHub: [github.com/christadejesus](https://github.com/christadejesus)