'''
Author: Brian Chen
Created for CSEC
Seminar on Continuous Integration: csec.club/seminars
01/11/2018
'''

import sys

def is_palindrome(string):
    '''
    Checks if a string is a palindrome. Palindromes are strings that are
    the same forwards as backwards.
    Args:
        string (str): The string to be considered
    Returns:
        res (bool): True if string is a palindrome, False otherwise
    Examples:
        >>> is_palindrome("SoS")
        True
        >>> is_palindrome("So|163361|Os")
        True
        >>> is_palindrome("")
        True
        >>> is_palindrome("SOZE")
        False
        >>> is_palindrome(",.,.")
        False
    '''
    # Sets string to lowercase as capitialization doesn't influence palindromes
    test = string.lower()
    rev = test[::-1]
    return rev == test


def safe_open(filename):
    '''
    Safely opens a file for reading
    Args:
        filename (str): The name of the file to be opened
    Returns:
        input_file (file): The file to be read. Returns None if the file does
        not exist in the directory
    '''
    # Tries to open the file
    try:
        input_file = open(filename)
    # Catches the error if file is not found in directory
    except IOError:
        input_file = None
    return input_file


def get_filename_argument():
    '''
    Obtains the file name to be parsed and counted for palindromes as given
    in the command line. Gives usage case if no file names are given.
    Args:
        None
    Returns:
        filename (str): The name of the file to be considered
    '''
    # The input file's filename given by argv from command-line
    # Can be extended to handle multiple filenames
    filename = sys.argv[-1]
    # If argv[-1] is argv[0] the program name, no arguments are passed
    if filename is sys.argv[0]:
        print "Usage: python palindrome.py [filename]"
        filename = None
    return filename


def count_palindromes(input_file):
    '''
    Returns the total number of palindromes that exist in input file
    Args:
        input_file (file): The file to check for palindromes in
    Returns:
        total_palindromes (int): The total number of palindromes found in
        input_file
    '''
    total_palindromes = 0
    # Opens filename and iterates through all lines to find total palindromes
    for line in input_file:
        line = line.rstrip()
        # Checks if each line is a palindrome
        if is_palindrome(line):
            total_palindromes += 1
    return total_palindromes


def find_palindromes():
    '''
    Executes the main function to count palindromes in JSON-parsable lines
    associated with CONS_KEY in an input file from the command line. Prints
    the total amounts of palindromes found, or any errors that occured.
    Args:
        None
    Returns:
        None
    '''
    filename = get_filename_argument()
    # Makes sure filename was given
    if filename:
        input_file = safe_open(filename)
        # Checks that input_file exists
        if input_file:
            palindromes = count_palindromes(input_file)
            print palindromes
        else:
            print "File does not exist: " + filename


if __name__ == '__main__':
    find_palindromes()