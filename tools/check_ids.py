#!/usr/bin/env python3
import os, sys
__version__ = 1.0

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
            sys.exit('Issues occured when listing files.')

    # add arrays to objectList array
    objectList.append(folderList)
    objectList.append(fileList)
    return objectList

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

def read(file_path="",string="",blacklist=[],trim=''):
    foundOnLines = []

    try:
        os.stat(file_path)
    except:
        print('{} could not be found...'.format(file_path))
    try:
        fileObject = open(file_path, "r")
    except:
        try:
            fileObject = open(file_path, "r", encoding="ascii", errors="surrogateescape")
        except:
            print('Can\'t read \'{}\'...'.format(file_path))
    for l in fileObject:
        l = l.replace('\n','')
        l = l.replace('\r','')
        l = l.replace('\t','')
        l = l.strip()
        if string in l:
            # check for bad word
            badword = []
            for bad in blacklist:
                badword.append(l.__contains__(bad))
            if not True in badword:
                if not trim == '':
                    l = l.replace(trim,'')
                    l = l.strip()
                foundOnLines.append(l)

    fileObject.close()

    return foundOnLines

def main():
    scriptpath = os.path.realpath(__file__)
    projectpath = os.path.dirname(os.path.dirname(scriptpath))
    os.chdir(projectpath)

    bad_count = 0
    files_list = []

    # FEATHING EVENT IDS
    print('Checking event ID\'s:')
    # getting event directory
    test_path = '{}/events'.format(projectpath)
    content_list = listFolderFiles(test_path)
    content_list = content_list[1]

    # collecting ID
    event_files_list = []
    for f in content_list:
        path = '{}/{}'.format(test_path,f)
        blacklist = ['country_event', 'news_event','#']
        event_line = read(path, "id =", blacklist, 'id =')
        event_files_list.append(event_line)
        files_list.append(f)
        # merging all ids in to one list
    event_id = []
    for ida in event_files_list:
        for eid in ida:
            event_id.append(eid)

    # Checking ID
    print('{} event files and {} event id\'s detected.\n------'.format(len(event_files_list),len(event_id)))

    duplicates_list = []
    for checkID in event_id:
        duplicate = 0
        for compareID in event_id:
            if checkID == compareID:
                duplicate += 1
        if duplicate >= 2:
            duplicates_list.append(checkID)

    # REMOVES DUPLICATES FOR PRINTING
    duplicates_list_x = []
    if len(duplicates_list) >= 1:
        for idDup in duplicates_list:
            if not idDup in duplicates_list_x:
                duplicates_list_x.append(idDup)

    for dups in duplicates_list_x:
        print(' ERROR: Duplicate Event ID detected {}'.format(dups))
        bad_count += 1




    print("------\nChecked {0} files\nErrors detected: {1}".format(len(files_list), bad_count))
    if (bad_count == 0):
        print("Config validation PASSED")
    else:
        print("Config validation FAILED")

    return bad_count
    
if __name__ == "__main__":
    sys.exit(main())
