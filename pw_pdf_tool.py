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
                if checkFileType(file_name, ".csv"):
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

if __name__ == "__main__":
    main()
