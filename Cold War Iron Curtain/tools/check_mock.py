#!/usr/bin/env python3
import os, sys, fnmatch
__version__ = 1.0
def check_basic_style(filename):
    bad_count_file = 0
    return bad_count_file

def main():

    print("Running mockup test")

    files_list = []
    bad_count = 0

    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))

    for root, dirnames, filenames in os.walk(rootDir + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            files_list.append(os.path.join(root, filename))

    for filename in files_list:
        bad_count = bad_count + check_basic_style(filename)

    print("------\nChecked {0} files\nErrors detected: {1}".format(len(files_list), bad_count))
    if (bad_count == 0):
        print("File validation PASSED")
    else:
        print("File validation FAILED")

    return bad_count
    
if __name__ == "__main__":
    sys.exit(main())