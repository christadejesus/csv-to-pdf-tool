import pytest
from pathlib import Path
from pw_pdf_tool import validateFileExtension
from pw_pdf_tool import verifyFileExists

# Function takes in file name as user input and expected extension to validate
def test_file_ext():
    assert validateFileExtension("test.csv", ".csv") == True
    assert validateFileExtension("test.txt", ".csv") == False
    assert validateFileExtension("test", ".csv") == False
    assert validateFileExtension("test.txt", ".txt") == True

# Function verifies that path to file located in user Downloads folder exist
def test_file_path():
    assert verifyFileExists("") == Path.home() / "Downloads"
    assert verifyFileExists("not_a_file.zz") == False
    assert verifyFileExists("file") == False
