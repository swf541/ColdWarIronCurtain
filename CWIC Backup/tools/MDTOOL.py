#!/usr/bin/env python3
import sys, os
import argparse, shutil, subprocess, tempfile
__version__ = 1.0

########## GLOBALS ##########

BLACKLIST = ['ISI','SHB','ERI']
WHITELIST = ['ISI','SHB','ERI']
INPUTLINES = [
    "add_opinion_modifier = { target = SHB modifier = ISIS_Are_Terrorists }",
    "add_opinion_modifier = { target = ISI modifier = ISIS_Are_Terrorists }",
    "add_opinion_modifier = { target = SHB modifier = ISIS_Are_Terrorists_Trade }",
    "add_opinion_modifier = { target = ISI modifier = ISIS_Are_Terrorists_Trade }"
]


#############################

def listFolderFiles(path=""):
    if path == "":
        sys.exit('No path defined.')
    os.chdir(path)
    path = os.listdir(path)

    objectList = []

    folderList = [] # Collect directories
    fileList = []   # Collect files

    for obj in path:
        if os.path.isfile(obj):
            fileList.append(obj)
        elif os.path.isdir(obj):
            folderList.append(obj)
        else:
            print()
            sys.exit('Issues occured when listing files.')

    # add arrays to objectList array
    objectList.append(folderList)
    objectList.append(fileList)
    return objectList


def testFile(file_path):
    linesRead = 0
    try:
        filetoTest = open(file_path, "r", encoding="ascii", errors="surrogateescape")
        for l in filetoTest:
            linesRead =+ 1
        filetoTest.close()
        return True
    except:
        print('\033[31mCan\'t read \'{}\'. Skipping file and moving on...\033[0m'.format(file_path,linesRead+1))
        filetoTest.close()
        return False


def grep(file_path,string):
    lineNr = 0
    foundOnLines = []
    try:
        os.stat(file_path)
    except:
        print('{} could not be found...'.format(file_path))
    try:
        fileObject = open(file_path, "r", encoding="ascii", errors="surrogateescape")
        for l in fileObject:
            lineNr += 1
            if (string in l):
                foundOnLines.append(lineNr)
    except:
        print('Can\'t read \'{}\'...'.format(file_path))
    fileObject.close()

    return foundOnLines

def add(file_path='', string='', line=-1):
    if line == -1:
        fileObject = open(file_path, "a", encoding="ascii", errors="surrogateescape")
        fileObject.write(string)
        fileObject.close()
    else:
        fileObject = open(file_path, "r", encoding="ascii", errors="surrogateescape")
        insertLine = fileObject.readlines()
        fileObject.close()

        insertLine.insert(line, string)

        fileObject = open(file_path, "w", encoding="ascii", errors="surrogateescape")
        insertLine = "".join(insertLine)
        fileObject.write(insertLine)
        fileObject.close()

def findClosestBraket(start=0,lineArray=[]):
    for nex in lineArray:
        if nex > start:
            return nex


def main():
    parser = argparse.ArgumentParser(prog='MDTOOL', formatter_class=argparse.RawTextHelpFormatter,
                        description='MDTOOL allow users to save time when dealing with diffrent tasks. \nThis by chunk edit allot of file with the same information.')
    parser.add_argument('program', choices=['relations'],
                        help='relations: Allow for a quick and effective way to add of new relations to all contry tags.\n           Require stringinsert argument')
    parser.add_argument('-w', '--stringinsert', default=[], type=str, nargs='+', metavar='STRING',
                        help='define what kind of insertion you whant to write.')
    
    filtergroup = parser.add_mutually_exclusive_group()
    filtergroup.add_argument('-B', '--blacklist', default=[], type=str, nargs='*', metavar='TAG',
                        help='this allow you to blacklist sertain contrytags.\nBy using blacklist you cant use the whitelist')
    filtergroup.add_argument('-W', '--whitelist', default=[], type=str, nargs='*', metavar='TAG',
                        help='this allow you to whitelist sertain contrytags.\nBy using whitelist you cant use the blacklist')
    parser.add_argument('-Y', '--yearfilter', default=[], type=int, metavar='YEAR', choices=[2011,2017],
                        help='this allow you to skip adding strings to sertain years.')
    
    parser.add_argument('--redpanda', action='store_true', help='show a secret and exit')
    parser.add_argument('-v', '--version', action='version', version='Build script version {}.'.format(__version__))

    args = parser.parse_args()

    PROGRAM = args.program
    INPUTLINES = args.stringinsert
    BLACKLIST = args.blacklist
    WHITELIST = args.whitelist
    YEARFILTER = args.yearfilter
    EGG = args.redpanda

    # set projecty path
    scriptpath = os.path.realpath(__file__)
    projectpath = os.path.dirname(os.path.dirname(scriptpath))
    os.chdir(projectpath)
    
    if EGG:
        sys.exit('The Red Panda is watching you. She is watching...')

    if PROGRAM == 'relations':
        if not len(INPUTLINES) < 1:
            input('WARNING! this will write lines inside of a exising files. Press enter to start...')
            pathToCountries = '{}\\history\\countries\\'.format(projectpath)
            
            nationFileList = listFolderFiles(pathToCountries)[1]

            for nation in nationFileList:
                fileName = "{}{}".format(pathToCountries,nation)
                if not BLACKLIST == []:
                    WHITELIST.append(nation[:3])
                if (nation[:3] in WHITELIST) and (not nation[:3] in BLACKLIST):
                    print('\033[1mReading and decoding {}...\033[0m'.format(nation[:3]))
                    testPassed = testFile(fileName)
                    if testPassed:
                        print('Looking for default relation position...'.format(nation[:3]))
                        ideasTopics = grep(fileName,'add_ideas')
                        endbrackets = grep(fileName,'}')
                        if not ideasTopics == []:
                            print('Default location discoverd inserting new relations.')
                            run = 0
                            for ideaTopic in ideasTopics:
                                onNewline = findClosestBraket(ideaTopic,endbrackets)
                                onNewline += run
                                run += 1
                                if ((YEARFILTER == 2011 and run == 1) or (YEARFILTER == 2017 and run >= 2)):
                                    add(fileName,"\r",onNewline) # add line after
                                for lineinput in INPUTLINES:
                                    lineinput = '\r\t{}'.format(lineinput)
                                    if ((YEARFILTER == 2011 and run == 1) or (YEARFILTER == 2017 and run >= 2)):
                                        add(fileName,lineinput,onNewline)

                                run += len(INPUTLINES)
                        else:
                            print('Could not find default location inserting on last line(s)...')
                            add(fileName,"\r") # add line after
                            for lineinput in INPUTLINES:
                                lineinput = '\r\t{}'.format(lineinput)
                                add(fileName,lineinput)
        else:
            sys.exit('MDTOOL Relations: error: Relations program require --stringinsert argument...')


if __name__ == "__main__":
    sys.exit(main())


