#!/usr/bin/env python3
import os, sys, fnmatch
import time

#startTime = time.time()

__version__ = 1.0

def check_basic_style(filepath):
    bad_count_file = 0

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

        # Store all brackets we find in this file, so we can validate everything on the end
        brackets_list = []
        indent_List = []

        # To check if we are in a comment block.
        checkIfInComment = False
        # Used in case we are in a line comment (//)
        ignoreTillEndOfLine = False
        # Used in case we are in a comment block (/* */). This is true if we detect a * inside a comment block.
        # If the next character is a /, it means we end our comment block.
        checkIfNextIsClosingBlock = False

        lastIsCurlyBrace = False

        # Extra information so we know what line we find errors at
        lineNumber = 1

        indexOfCharacter = 0

        for c in content:
            if (lastIsCurlyBrace):
                lastIsCurlyBrace = False
            if c == '\n': # Keeping track of our line numbers
                lineNumber += 1 # so we can print accurate line number information when we detect a possible error
            if c != ' ':
                indent_List = []
            # if we are not in a comment block, we will check if we are at the start of one or count the () {} and []
            elif (checkIfInComment == False):
                if (ignoreTillEndOfLine): # we are in a line comment, just continue going through the characters until we find an end of line
                    if (c == '\n'):
                        ignoreTillEndOfLine = False
                else: # validate brackets
                    if (c == '#'):
                        ignoreTillEndOfLine = True
                    elif (c == '('):
                        brackets_list.append('(')
                    elif (c == ')'):
                        if (len(brackets_list) > 0 and brackets_list[-1] in ['{', '[']):
                            print("ERROR: Possible missing round bracket ')' detected at {0} Line number: {1}".format(filepath,lineNumber))
                            bad_count_file += 1
                        brackets_list.append(')')
                    elif (c == '['):
                        brackets_list.append('[')
                    elif (c == ']'):
                        if (len(brackets_list) > 0 and brackets_list[-1] in ['{', '(']):
                            print("ERROR: Possible missing square bracket ']' detected at {0} Line number: {1}".format(filepath,lineNumber))
                            bad_count_file += 1
                        brackets_list.append(']')
                    elif (c == '{'):
                        brackets_list.append('{')
                    elif (c == '}'):
                        lastIsCurlyBrace = True
                        if (len(brackets_list) > 0 and brackets_list[-1] in ['(', '[']):
                            print("ERROR: Possible missing curly brace '}}' detected at {0} Line number: {1}".format(filepath,lineNumber))
                            bad_count_file += 1
                        brackets_list.append('}')

                    elif (c == ' '): # checking indent
                        indent_List.append('space')
                        if (len(indent_List) == 4):
                            print("ERROR: spaces indent (4) detected instead of tab at {0} Line number: {1}".format(filepath,lineNumber))
                            bad_count_file += 1

            indexOfCharacter += 1

        if brackets_list.count('[') != brackets_list.count(']'):
            print("ERROR: A possible missing square bracket [ or ] in file {0} [ = {1} ] = {2}".format(filepath,brackets_list.count('['),brackets_list.count(']')))
            bad_count_file += 1
        if brackets_list.count('(') != brackets_list.count(')'):
            print("ERROR: A possible missing round bracket ( or ) in file {0} ( = {1} ) = {2}".format(filepath,brackets_list.count('('),brackets_list.count(')')))
            bad_count_file += 1
        if brackets_list.count('{') != brackets_list.count('}'):
            print("ERROR: A possible missing curly brace {{ or }} in file {0} {{ = {1} }} = {2}".format(filepath,brackets_list.count('{'),brackets_list.count('}')))
            bad_count_file += 1

    return bad_count_file


def main():
    print("Validating Basic Style")

    files_list = []
    bad_count = 0
  
    # Allow running from root directory as well as from inside the tools directory
    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))

    for root, dirnames, filenames in os.walk(rootDir + '/'+ 'common' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            files_list.append(os.path.join(root, filename))

    for root, dirnames, filenames in os.walk(rootDir + '/'+ 'events' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            files_list.append(os.path.join(root, filename))

    for root, dirnames, filenames in os.walk(rootDir + '/'+ 'history' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            files_list.append(os.path.join(root, filename))

    for filename in files_list:
        bad_count = bad_count + check_basic_style(filename)

    print("------\nChecked {0} files\nErrors detected: {1}".format(len(files_list), bad_count))
    if (bad_count == 0):
        print("File validation PASSED")
    else:
        print("File validation FAILED")

    #print ('The script took {0} second!'.format(time.time() - startTime))

    return bad_count
    
if __name__ == "__main__":
    sys.exit(main())
