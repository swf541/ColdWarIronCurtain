#!/usr/bin/env python3
import os, sys, fnmatch, re
import time

startTime = time.time()

__version__ = 1.0

def check_basic_style(filepath):

    fixedErrors = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        lineNum = 0
        openBraces = [0, 0]


        for line in content:
            #print(line)
            #input("Press Enter to continue...")
            lineNum +=1
            if not line.startswith("#"): #If the line doesn't start with a comment
                if "{" in line: #if there is an open brace in this line
                    hasComment = re.search(r'#.*[{}]+', line, re.M | re.I)  # If comment at the start or before {
                    if not hasComment:  #if the line doesn't have a comment before the open brace
                        openBraces[0] += line.count('{')
                        #count total open braces and subtract open braces that are easy to find and used correctly
                        closingBraces = line.count('{') - line.count(' {\n') - line.count(' { ')

                        #if there are braces we couldn't find using efficient .count, use powerful inefficient regex
                        if closingBraces > 0:
                            hasNoSpace = re.search(r'([^\s]+){|{([^\s]+)', line, re.M | re.I)  # If no space before or after brace
                            if hasNoSpace: #If regex finds open braces not styled correctly
                                print("ERROR: Missing an space before or after open brace at {0} Line number: {1}".format(filepath, lineNum))
                                #input("Press Enter to continue...")
                                fixedErrors += 1

                if "}" in line: #if there is an close brace in this line
                    hasComment = re.search(r'#.*[{}]+', line, re.M | re.I)  # If comment at the start or before {
                    if not hasComment: #if the line doesn't have a comment before the open brace
                        openBraces[0] += -line.count('}')
                        #count total close braces and subtract open braces that are easy to find and used correctly
                        openingingBraces = line.count('}') - line.count(' }\n') - line.count(' } ')

                        #if there are braces we couldn't find using efficient .count, use powerful inefficient regex
                        if openingingBraces > 0:
                            hasNoSpace = re.search(r'([^\s]+)}|}([^\s]+)', line,re.M | re.I)   # If no space before or after brace
                            if hasNoSpace: #If regex finds open braces not styled correctly
                                print("ERROR: Missing an space before or after close brace at {0} Line number: {1}".format(filepath, lineNum))
                                #input("Press Enter to continue...")
                                fixedErrors += 1
                if "\"" in line: #if the line has a qoute
                    if (line.count('\"') % 2) !=0: #if there are an odd number of qoutes on this line
                        hasComment = re.search(r'#.*[\"]+', line, re.M | re.I)  # If comment at the start or before "
                        if not hasComment: #if there is no comment before the qoute
                            print("ERROR: Missing an quotation sign at {0} Line number: {1}".format(filepath,lineNum))
                            #input("Press Enter to continue...")
                            fixedErrors += 1

                if "=" in line: #if the line has an equal sign
                    equalSign = 0
                    #count total equal signs that are easy to find and used correctly
                    equalSign = line.count('=') - line.count(' = ') - line.count(' =\n')

                    if (line.count('  =') > 0) or (line.count('=  ') > 0) :
                        print("ERROR: Two spaces before or after an equal sign at {0} Line number: {1}".format(filepath, lineNum))
                        equalSign = equalSign - line.count('  =') - line.count('=  ')
                        fixedErrors += 1
                    if equalSign != 0: #if there are equal signs that aren't used correctly
                        print("ERROR: Missing an space before or after an equal sign at {0} Line number: {1}".format(filepath,lineNum))
                        #input("Press Enter to continue...")
                        fixedErrors += 1
                if "    " in line: #if 4 spaces in the line
                    print("ERROR: spaces indent (4) detected instead of tab at {0} Line number: {1}".format(filepath,lineNum))
                    fixedErrors += 1
                if openBraces[0] <= -1:
                    print("ERROR: A possible missing curly brace {{ in file {} {{line {}}}".format(filepath, lineNum))
                    openBraces[0] = 0
                    fixedErrors +=1
                #input("Press Enter to continue...")
        else:
            if openBraces[0] < 0:
                print("ERROR: A possible missing curly brace }} in file {} {{line {}}}".format(filepath, lineNum))
                fixedErrors += 1
            elif openBraces[0] > 0:
                print("ERROR: A possible missing curly brace {{ in file {} has no matching closing bracket".format(filepath, lineNum))
                fixedErrors += 1
    file.close()

    return fixedErrors


def main():
    print("Validating Basic Style - Secondary Check")

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

    print ('The script took {0} second!'.format(time.time() - startTime))
    
    return bad_count
    
if __name__ == "__main__":
    sys.exit(main())
