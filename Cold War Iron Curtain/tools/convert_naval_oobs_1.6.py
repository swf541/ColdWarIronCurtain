#!/usr/bin/env python3
import os, sys, fnmatch, re
import time

startTime = time.time()

__version__ = 1.0

def analyzeMyOOB(filename, rootDir):
    newContent = ""
    oldContent = ""
    with open(os.path.join(rootDir, filename), 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        navyFound = 0
        openBraces = 0
        units = 0
        location = ""
        name = ""
        for line in content:
            if "navy" in line and "{" in line:
                navyFound = 1
                if units == 0:
                    newContent += "units = {\n\n\t### Naval OOB ###\n"
                    units = 1
                line = line.replace('navy', 'fleet')
            if navyFound ==1:
                if "{" in line:
                    openBraces += 1
                if "location" not in line:
                    if "base" in line:
                        line = line.replace('base', 'naval_base')
                    newContent += line
                    if "name" in line:
                        hasName = re.search(r'\s+?name\s?=\s?(.*)', line, re.M | re.I)  # Search for the name
                        if hasName:
                            name = str(hasName.group(1))
                else:
                   hasLocation = re.search(r'\s?location\s=\s(.*)', line, re.M | re.I)  # search for the location
                   if hasLocation:
                        location = str(hasLocation.group(1))
                   navyFound = 2
                   newContent += "\t\ttask_force = {\n"
                   newContent += "\t\t\tname = " + name + "\n"
                   newContent += "\t\t\tlocation = " + location + "\n"

                if "}" in line:
                    openBraces -= 1
                if openBraces <= 0:
                    navyFound = 0
            elif navyFound == 2:
                if "{" in line:
                    openBraces += 1

                newContent += "\t" + line
                #if filename == "AGL_2000.txt":
                    #print(line)



                if "}" in line:
                    openBraces -= 1
                if openBraces <=0:
                    navyFound = 0
                    newContent += "\t}\n"

            else:

                oldContent +=line
    newContent += "}\n"

    #print(rootDir)
    #input()
    #if filename == "CHI_2000.txt":

    rootDir += "generated/"
    if not os.path.isdir(rootDir):
        os.mkdir(rootDir)

    with open(os.path.join(rootDir, filename), 'w', encoding='utf-8', errors='ignore') as file:
        file.write(oldContent)

    fileNameNoExt = re.match(r'(.*).txt', filename, re.M | re.I)  #get filename without the .ext ectension
    filename = str(fileNameNoExt.group(1)) + "_naval_mtg.txt"
    if newContent != "}\n":
        with open(os.path.join(rootDir, filename), 'w', encoding='utf-8', errors='ignore') as file:
            file.write(newContent)

        filename = str(fileNameNoExt.group(1)) + "_naval_legacy.txt"
        with open(os.path.join(rootDir, filename), 'w', encoding='utf-8', errors='ignore') as file:
            file.write(newContent)

    return filename

def main():

    bad_count = 0
    # Allow running from root directory as well as from inside the tools directory
    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))
    global totalErrors
    totalErrors = 0
    for root, dirnames, filenames in os.walk(rootDir + '/' + 'history' + '/units' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            analyzeMyOOB(filename, root)
            #input()




    print('The script took {0} second!'.format(time.time() - startTime) + " therea are a total of: " + str(totalErrors) + " errors.")

    return bad_count


if __name__ == "__main__":
    sys.exit(main())