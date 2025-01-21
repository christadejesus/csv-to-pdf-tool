import csv
import re
import sys
import os
import time
from pathlib import Path
from datetime import date
from fpdf import FPDF
from fpdf import FontFace
from fpdf.enums import TableCellFillMode
from colorama import Fore, init
import pyfiglet

def main():
    """ Reset all text color changes after each print """
    init(autoreset=True) 
    """ Display program name as ASCII character text banner """
    f = pyfiglet.figlet_format("CSV to PDF Tool", font="standard")
    print(Fore.YELLOW + f)
    """ Display program purpose """
    print("Welcome to the CSV to PDF Tool!\nThis tool converts your CSV, or Comma Separated Values,\ndocument to a clean, customized, and printable PDF.")
    print("Please make sure your CSV document has been dowloaded into your Downloads folder.")
    while True:
            try:
                # Input prompt
                file_name = input("\nEnter the name of your CSV file to be converted (e.g., my_data_export.csv): ").strip()
                # Validate, verify, extract
                if validateFileExtension(file_name, ".csv") and (file_path := verifyFileExists(file_name)) and (fieldnames := extractCSVFieldnames(file_path)):
                    # Select & extract
                    selected_fieldnames = presentFieldnames(fieldnames)
                    csv_data = extractData(file_path, selected_fieldnames)
                    cleaned_data = cleanData(csv_data)
                    sorted_data = sortData(cleaned_data, selected_fieldnames)
                    # Create
                    new_file_name = getFileName(".pdf")
                    title = getTitle(new_file_name)
                    new_csv_path = createNewCSV(sorted_data, selected_fieldnames)
                    createPDF(new_csv_path, new_file_name, title)
                    # Clean up
                    removeBackupCSV(new_csv_path)
                    # Inform
                    print(f"\n{new_file_name} was saved to your Desktop.\n")
                    # Repeat or exit
                    next = input("Would you like to create another PDF? Enter Y or N:  ").upper().strip()
                    if next == "Y" or next =="YES":
                        continue
                    else:
                        f = pyfiglet.figlet_format(f"\nEnjoy your day!\n : )\n", font="standard")
                        print(Fore.YELLOW + f)
                        time.sleep(3) # Pause for 3 seconds
                        sys.exit()

            except KeyboardInterrupt:
                f = pyfiglet.figlet_format(f"\nEnjoy your day!\n :  )\n", font="standard")
                print(Fore.YELLOW + f)
                time.sleep(3) # Pause for 3 seconds
                sys.exit()

def validateFileExtension(file_name, ext):
    if file_name.endswith(ext) == True:
        print(Fore.GREEN + f"+ File is {ext}")
        return True
    else:
        print(Fore.YELLOW + f"Not a valid {ext} file.\nPlease check the file name and try again.")
        return False

def verifyFileExists(file_name):
    # Construct the full path to the file using Path() to ensure it's a Path object, not a string
    downloads_folder = Path.home() / "Downloads"
    file_path = downloads_folder / file_name

    if file_path.exists():
        print(Fore.GREEN + "+ File located")
        return file_path
    else:
        print(Fore.YELLOW + "File does not exist in your Downloads folder.\nPlease check the file location and try again.") 
        return False

def extractCSVFieldnames(file_path):
    """
    Extracts fieldnames from the CSV file at the given path.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of fieldnames from the CSV file.
        If the file cannot be read, handles the StopIteration error
        by printing message with more information and returns False.
    """
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file)

        try:
            header = next(reader)
            fieldnames = []
            for key in header:
                fieldnames.append(key)
            print(Fore.GREEN + "+ Fieldnames extracted")
            return fieldnames

        except StopIteration:
            print(Fore.YELLOW + "No fieldnames found.\nPlease check the file content and try again.")
            return False

def presentFieldnames(fieldnames):
    """
    Present fieldnames as a numbered menu and allow the user to select
    which ones to include by entering the corresponding numbers.

    Parameters:
        fieldnames (list): A list of fieldnames.

    Returns:
        list: A list of fieldnames selected by the user.
    """
    # Get user input
    while True:
        try:
            # Display fieldnames with numbers
            print("\nPlease select which fieldnames to include by entering the numbers (e.g., 1, 3, 5).\nData will be sorted alphabetically by your first fieldname.")
            for i, fieldname in enumerate(fieldnames, 1):
                print(f"{i} - {fieldname}")
            selected_numbers = input("\nEnter your selections: ").strip()

            # Split input by commas, remove spaces, and convert to a list of integers
            selections = [int(num.strip()) for num in selected_numbers.split(',')]

            # Validate input: check if all numbers are within valid range
            if all(1 <= num <= len(fieldnames) for num in selections):
                # Select the corresponding fieldnames
                selected_fieldnames = [fieldnames[i - 1] for i in selections]  # Convert user input to zero-indexed
                if confirmFieldnames(selected_fieldnames):
                    print(Fore.GREEN + "+ Fieldnames confirmed")
                    break
            else:
                print(Fore.YELLOW + "Invalid input. Please select numbers within the provided range.")

        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter numbers separated by commas.")

    return selected_fieldnames

def confirmFieldnames(selected_fieldnames):

    for fieldname in selected_fieldnames:
        print(Fore.CYAN + f"{fieldname} | ", end="")
    # Prompt user for confirmation of fieldnames
    next_step = input("\n\nEnter 'Y' to accept these fieldnames, 'N' to try again: ").upper().strip()
    if next_step == "Y" or next_step == "YES":
        return True

def extractData(file_path, selected_fieldnames):
    """
    Extracts data from the CSV file at the given path.

    Parameters:
        file_path (str): Path to the CSV file.
        selected_fieldnames (list): A list of fieldnames selected by the user.

    Returns:
        list: A list of dictionaries with all data from the CSV file to be included in PDF.
    """
    csv_data = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row = {key: value for key, value in row.items() if key in selected_fieldnames}
            csv_data.append(row)

        print(Fore.GREEN + "+ CSV data extracted")
        return csv_data

""" 
Iterating through list of dicts:

for item in my_list_of_dicts:
    for value in item.values():
        if value == "one":
            print(value)
"""
def cleanData(data):
    # Clean up any long URIs (e.g., https://site.subsite.com/login?redirect=%bla%bla%bla becomes https://site.com)
    pattern = re.compile(r"((https?://)?(www\.)?[\w\-]+(\.[a-zA-Z]{2,})+)(/)?")

    cleaned_data = []

    for item in data:
        cleaned_item = {}
        for key, value in item.items():         
            if isinstance(value, str):
                match = pattern.search(value)
                if match:
                    cleaned_item[key] = match.group(1)
                else:
                    cleaned_item[key] = value
            else:
                cleaned_item[key] = value
        cleaned_data.append(cleaned_item)
    return cleaned_data

def sortData(data, selected_fieldnames):
    # Sort data alphabetically by the first fieldname
        return sorted(data, key=lambda item: item[selected_fieldnames[0]])

def getFileName(extension):
    while True:
        try:
            file_name = input(f"\nEnter a name for your new {extension} file (e.g., my_new_file{extension}): \n").strip()
            file_name_lower = file_name.lower()
            valid_chars = re.search(r"^[a-z0-9-_]+.pdf$", file_name_lower)

            if valid_chars:
                return f"{file_name}"
            else:
                print(Fore.YELLOW + f"File names may contain only letters, numbers, dashes, or underscores (e.g., my_new_file{extension}).\n Please try again.")
                continue
        except KeyboardInterrupt:
            raise KeyboardInterrupt
            
def getTitle(file_name):
    while True:
        try:
            title = input(f'\nEnter the heading to display at the top of each {file_name} page (e.g. "Login Information - 2/2025"): \n')
            next_step = input(f"\nEnter 'Y' to accept '{title}', 'N' to try again: ").upper().strip()
            if next_step == "Y" or next_step == "YES":
                return title
            else:
                continue
        except KeyboardInterrupt:
            raise KeyboardInterrupt

def createNewCSV(csv_data, selected_fieldnames):
    """
    Creates path for a new CSV file to be temporarily stored in user's Desktop folder,
    and opens this new file. Using CSV DictWriter, it parses the passed in csv data
    and fieldnames, writes the data to the new file, displays a confirmation message
    in the terminal, and returns the new csv file path.

    Parameters:
        csv_data (list): A list of dictionaries including all CSV data to be included.
        selected_fieldnames (list): A list of fieldnames selected by the user.

    Returns:
        str: Path to the new CSV file.
    """
    desktop_folder = Path.home() / "Desktop"
    new_csv_file_name = f"temp.csv"
    new_csv_path = desktop_folder / new_csv_file_name

    with open(new_csv_path, 'w', newline='') as new_csv:
        writer = csv.DictWriter(new_csv, fieldnames=selected_fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    print(Fore.GREEN + "+ New CSV created")
    return new_csv_path

def createPDF(new_csv_path, file_name, title):
    """
    Creates new PDF spreadsheet from the newly generated CSV file, saved to the user Desktop.
    Prints confirmation message to the terminal and returns the PDF file name.

    Parameters:
        new_csv_path (str): Path to the new CSV file.

    Returns:
        str: Name of the new PDF file.
    """
    desktop_folder = Path.home() / "Desktop"
    pdf_path = desktop_folder / file_name

    # create PDF from csv file
    with open(new_csv_path, encoding="utf8") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))

    class PDF(FPDF):
        def header(self):
            self.set_font("helvetica", style="B", size=16)
            self.cell(0, 10, text=f"{title}", align="C")
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font("helvetica", style="I", size=8)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    pdf = PDF(orientation="L", unit="mm", format="Letter")
    pdf.set_font("helvetica", size=8)

    # Creat a table from data in the new csv file
    pdf.add_page()
    headings_style = FontFace(emphasis="BOLD")

    with pdf.table(
        cell_fill_color=(230, 230, 230),
        cell_fill_mode=TableCellFillMode.ROWS
    ) as table:
        for data_row in data:
            row = table.row()
            for item in data_row:
                row.cell(item)

    # Output the PDF file to the Desktop
    pdf.output(pdf_path)
    print(Fore.GREEN + "+ New PDF created")

""" Delete the temporary CSV file and display confirmation to user. """
def removeBackupCSV(new_csv_path):
    os.remove(new_csv_path)
    print(Fore.GREEN + "+ New CSV removed")

if __name__ == "__main__":
    main()
