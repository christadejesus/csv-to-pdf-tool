import csv
import re
import sys
import os
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
    f = pyfiglet.figlet_format("PW PDF Tool", font="standard")
    print(Fore.YELLOW + f)
    """ Display program purpose """
    print("Welcome to the PW PDF Tool!\nLet's quickly convert your exported password manager CSV\nto a clean, customized, and printable PDF.\n")

    while True:
            try:
                """ Prompt user for filename """
                file_name = input("Enter the name of your CSV file (e.g., pw_export.csv): ").strip()
                if not checkFileType(file_name, ".csv"):
                    continue
                file_path = checkFilePath(file_name)
                if not file_path:
                    continue
                print("So far so good!")
                break

            except KeyboardInterrupt:
                """ On Ctrl+C, exit """
                sys.exit(Fore.CYAN + "\nHave an awesome day!\n")

    sys.exit(Fore.CYAN + "\nHave an awesome day!\n")

""" Validate file type """
def checkFileType(file_name, ext):
    if file_name.endswith(ext) == True:
        print(Fore.GREEN + f"✔ {ext} file")
        return True
    else:
        print(Fore.YELLOW + f"Not a valid {ext} file.\nPlease check the file name and try again.\n")
        return False

""" Contruct file path and validate """    
def checkFilePath(file_name):
    # Construct the full path to the file using Path() to ensure it's a Path object, not a string
    downloads_folder = Path.home() / "Downloads"
    file_path = downloads_folder / file_name

    if file_path.exists():
        print(Fore.GREEN + "✔ file found")
        return file_path
    else:
        print(Fore.YELLOW + "File does not exist in your Downloads folder.\nPlease check the file name and try again.\n") 


if __name__ == "__main__":
    main()
