#!/usr/bin/env python3
import os, sys, fnmatch, re
import time

startTime = time.time()

__version__ = 1.0


def get_tags(rootDir):
    tags = []
    with open(rootDir, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        for line in content:
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                hasTag = re.match(r'^[A-Z]{3}', line, re.M | re.I)  # If it's a tag
                if hasTag:
                    tags.append(hasTag.group())
    return tags


def checkFocuses(filepath):
    bad_count_file = 0
    lineNum = 0;
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        for line in content:
            lineNum += 1
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "id =" in line or "id=" in line:
                    hasFocus = re.match(r'[ \t]+id\s?=\s?([A-za-z0-9-?_?]+)', line, re.M | re.I)  # If it's a tag
                    if hasFocus:
                        #print(hasFocus.group(1))
                        hasFocusFormet = re.match(r'[ \t]+id\s?=\s?([A-Z]{3}_[a-z0-9_-]+)', line, re.M | re.U )  # If it's a tag
                        #if not hasFocusFormet:
                            #print("ERROR: " + hasFocus.group(1) + " is formatted incorrectly, must be TAG_focus_name  {0} Line number: {1}".format(filepath, lineNum ))
                            #print(hasFocus.group(1))
                            #bad_count_file +=1

    return bad_count_file


def check_ideas(filepath):
    bad_count_file = 0
    lineNum = 0
    pdxIdeaCode = ["allowed", "modifier", "country", "allowed_civil_war", "OR", "AND", "ideas", "NOT", "CANCEL",
                 "on_add", "available", "ai_will_do", "rule", "do_effect"]

    pdxIdeaCode = [element.lower() for element in pdxIdeaCode]
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        braces = 0
        for line in content:
            lineNum +=1
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "{" in line:
                    braces +=1
                if braces == 3:
                    hasIdea = re.search(r'([A-Za-z0-9_-]+)\s?=\s?{', line, re.M | re.I)  # If it's a tag
                    if hasIdea:
                        countryIdea = re.search(r'([A-Z]{3}_[a-z0-9_-]+)\s?=\s?{', line, re.M )  # If it's a tag
                        #if countryIdea:
                            #print(countryIdea.group(1))
                            #input()
                        genericIdea = re.search(r'([a-z0-9_-]+)\s?=\s?{', line, re.M )  # If it's a tag
                        if not countryIdea and not genericIdea:
                            print("ERROR: " + hasIdea.group(
                                1) + " is formatted incorrectly, must be TAG_idea_name or generic_idea_name {0} Line number: {1}".format(
                               filepath, lineNum))
                            bad_count_file +=1
                            #print(hasFocus.group(1))
                            #print("wrong: " + hasIdea.group(1))
                if "}" in line:
                    braces -=1

    return bad_count_file

def check_event_for_logs(filepath):
    bad_count_file = 0
    lineNum = 0
    hasLog = 0
    optionFound = 0
    optionName = ""

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        braces = 0
        for line in content:
            lineNum +=1
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "option" in line and "=" in line:
                    optionFound = 1
                    optionLine = lineNum
                    hasLog = 0
                if optionFound == 1:
                    if "name" in line and "=" in line:
                        hasName = re.search(r'name\s?=\s([a-zA-Z0-9-_.]+)', line, re.M | re.I)  # If it's a tag
                        if hasName:
                            optionName = hasName.group(1)
                    if "{" in line:
                        braces += line.count("{")

                    if braces > 0 and hasLog == 0 and "log" in line:
                        hasLog = 1
                        optionFound = 0
                        braces = 0
                    if "}" in line:
                        braces -= line.count("}")
                    if braces == 0 and hasLog == 0:
                        print("ERROR: Event " + optionName + " doesn't have logging {0} Line number: {1}".format(
                            filepath, optionLine))
                        optionFound = 0
                        braces = 0
                        hasLog = 0
                        bad_count_file += 1

    return bad_count_file

def check_Flags(filepath):
    bad_count_file = 0
    lineNum = 0

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        advFlag = 0
        isGlobalFlag = 0
        countryFlags = []
        globalFlags = []
        for line in content:
            lineNum +=1
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "set_country_flag" in line or "has_country_flag" in line or "set_global_flag" in line or "has_global_flag" in line:
                    #print("here: " + filepath + str(lineNum))
                    if advFlag == 0:
                        hasSimpleFlag = re.search(r'[a-z_]+_flag\s?=\s?([A-Za-z0-9-_]+)', line, re.M )  # If it's a tag
                        hasAdvFlag = re.search(r'[a-z_]+_flag\s?=\s?{', line, re.M | re.I)  # If it's a tag
                        if hasAdvFlag:
                            advFlag = 1
                            if "global_flag" in line:
                                isGlobalFlag = 1
                            #print("Test: " + str(lineNum))
                        elif hasSimpleFlag:
                            simpleFlagFormat = re.search(r'([a-z_]+_flag\s?=\s?)([A-Z0-9]{1}([a-z0-9]+)?_[A-Z0-9]{1}([a-z0-9]+)?)(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?$', line, re.M | re.I)
                            if not hasSimpleFlag:
                                print("ERROR: " + hasSimpleFlag.group(
                                    1) + " is formatted incorrectly, must be The_Flags_Name {0} Line number: {1}".format(
                                    filepath, lineNum))
                                bad_count_file += 1
                            else:
                                if "global_flag" in line:
                                    globalFlags.append(hasSimpleFlag.group(1))
                                else:
                                    countryFlags.append(hasSimpleFlag.group(1))

                if advFlag == 1 and ("flag=" or "flag =" in line):
                    hasAdvFlag2 = re.search(r'flag\s?=\s([a-zA-Z0-9\-\_]+)', line, re.M )  # If it's a tag
                    #print("Test2: " + str(lineNum))
                    if hasAdvFlag2:
                        advFlag = 0
                        #print("Test3: " + str(lineNum))
                        advFlagFormat = re.search(
                            r'flag\s?=\s?(([A-Z0-9]{1}([a-z0-9]+)?_[A-Z0-9]{1}([a-z0-9]+)?)(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?(_[A-Z0-9]{1}([a-z0-9]+)?)?$)',
                           line, re.M)
                        if not advFlagFormat:
                            print("ERROR: " + hasAdvFlag2.group(
                                1) + " is formatted incorrectly, must be The_Flags_Name {0} Line number: {1}".format(
                                filepath, lineNum))
                            bad_count_file += 1
                        else:
                            if isGlobalFlag ==1:
                                globalFlags.append(hasSimpleFlag.group(1))
                                isGlobalFlag = 0
                            else:
                                countryFlags.append(hasSimpleFlag.group(1))
    return bad_count_file, globalFlags, countryFlags

def findPdxSyntax(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        typeOfCode = 0  # 1 = trigger, 2 = effects
        pdxTriggers = []
        pdxEffects = []
        # 0 0 0 = trigger name
        # 0 1 x = scopes
        # 0 2 x = targets
        # 0 3 x = examples
        triggerNum = 0
        EffectrNum = 0

        for line in content:
            if "==" in line:  # check for triggers
                if "TRIGGER DOCUMENTATION" in line:
                    typeOfCode = 1
                    # print(typeOfCode)
                elif "EFFECT DOCUMENTATION" in line:
                    typeOfCode = 2

            if typeOfCode == 1:
                if "Supported scopes:" in line:
                    if "state" in line:
                        pdxTriggers[triggerNum - 1].append(["state"])
                        #print("scope: " + pdxTriggers[triggerNum-1][1][0])
                    elif "country" in line:
                        pdxTriggers[triggerNum - 1].append(["country"])
                        #print("scope: " + pdxTriggers[triggerNum-1][1][0])
                    elif "Supported scopes: ???" == line:
                        pdxTriggers[triggerNum - 1].append(["N/A"])
                        # print("scope: " + pdxTriggers[triggerNum-1][1][0])
                    elif "Supported scopes:\n" == line:
                        pdxTriggers[triggerNum - 1].append(["N/A"])
                        # print("scope: " + pdxTriggers[triggerNum-1][1][0])

                elif "Supported targets:" in line:
                    if "none" in line:
                        pdxTriggers[triggerNum - 1].append(["none"])
                        # print("scope: " + pdxTriggers[triggerNum-1][2][0])
                    elif "Supported targets:\n" == line:
                        pdxTriggers[triggerNum - 1].append(["N/A"])
                        # print("scope: " + pdxTriggers[triggerNum-1][2][0])

                elif "" != line:
                    isTrigger = re.search(r'^([A-Z_?-?]+) -', line, re.M | re.I)  # If it's a tag
                    if isTrigger:
                        isTrigger = re.search(r'^([A-Z_?-?]+) -', line, re.M | re.I)  # If it's a tag
                        pdxTriggers.append([[isTrigger.group(1)]])
                        triggerNum += 1


            if typeOfCode == 2:
                if "Supported scopes:" in line:
                    if "state" in line:
                        pdxEffects[EffectrNum - 1].append(["state"])
                        # print("scope: " + pdxTriggers[triggerNum-1][1][0])
                    elif "country" in line:
                        pdxEffects[EffectrNum - 1].append(["country"])
                        # print("scope: " + pdxTriggers[triggerNum-1][1][0])
                    elif "Supported scopes: ???" == line:
                        pdxEffects[EffectrNum - 1].append(["N/A"])
                        # print("scope: " + pdxTriggers[triggerNum-1][1][0])
                    elif "Supported scopes:\n" == line:
                        pdxEffects[EffectrNum - 1].append(["N/A"])
                        # print("scope: " + pdxTriggers[triggerNum-1][1][0])
                elif "Supported targets:" in line:
                    if "none" in line:
                        pdxEffects[EffectrNum - 1].append(["none"])
                        # print("scope: " + pdxTriggers[triggerNum-1][2][0])
                    elif "country" in line:
                        pdxEffects[EffectrNum - 1].append(["country"])
                        # print("scope: " + pdxTriggers[triggerNum-1][2][0])
                    elif "Supported targets: none\n" == line:
                        pdxEffects[EffectrNum - 1].append(["N/A"])
                        #print("scope: " + pdxTriggers[triggerNum-1][2][0])
                        #print(content)
                        #input()

                elif "" != line:
                    isEffect = re.search(r'^([A-Z_?-?]+) -', line, re.M | re.I)  # If it's a tag
                    if isEffect:
                        isEffect = re.search(r'^([A-Z_?-?]+) -', line, re.M | re.I)  # If it's a tag
                        pdxEffects.append([[isEffect.group(1)]])
                        EffectrNum += 1

    return pdxTriggers, pdxEffects

def getCountryTriggers (allTriggers):
    countryTriggers = []
    for x in allTriggers:
        # print("x = " + str(len(x)))
        for y in x:
            for z in y:
                if z == "country":
                    countryTriggers.append(x)
    #for x in countryTriggers:
    #    # print("x = " + str(len(x)))
     #   for y in x:
     #       for z in y:
     #           print("x = " + str(x))
     #           print("y = " + str(y))
     #           print("z = " + str(z))


    return countryTriggers

def getStateTriggers (allTriggers):
    stateTriggers = []
    for x in allTriggers:
        # print("x = " + str(len(x)))
        for y in x:
            for z in y:
                if z == "state":
                    stateTriggers.append(x)
    #for x in stateTriggers:
    #   # print("x = " + str(len(x)))
    #    for y in x:
    #        for z in y:
    #            print("x = " + str(x))
    #            print("y = " + str(y))
    #            print("z = " + str(z))


    return stateTriggers

def getUnkownTriggers (allTriggers):
    #print ("test")
    unkownTriggers = []
    for x in allTriggers:
        #print("x = " + str(x))
        for y in x:
            for z in y:
                #print(z)
                if z == "N/A":
                    unkownTriggers.append(x)
    #for x in unkownTriggers:
       # print("x = " + str(len(x)))
    #    for y in x:
    #        for z in y:
    #           print("x = " + str(x))
    #            print("y = " + str(y))
    #            print("z = " + str(z))


    return unkownTriggers

def getCountryEffects (allEffects):
    countryEffects = []
    for x in allEffects:
        # print("x = " + str(len(x)))
        for y in x:
            for z in y:
                if z == "country":
                    countryEffects.append(x)
    #for x in countryEffects:
    #    # print("x = " + str(len(x)))
    #    for y in x:
     #       for z in y:
    #            print("x = " + str(x))
     #           print("y = " + str(y))
     #           print("z = " + str(z))


    return countryEffects

def getStateEffects (allEffects):
    stateEffects = []
    for x in allEffects:
        # print("x = " + str(len(x)))
        for y in x:
            for z in y:
                if z == "state":
                    stateEffects.append(x)
    #for x in stateEffects:
        # print("x = " + str(len(x)))
        #for y in x:
        #   for z in y:
        #        print("x = " + str(x))
        #       print("y = " + str(y))
        #        print("z = " + str(z))


    return stateEffects
def getUnkownEffects (allEffects):
    unkownEffects = []
    for x in allEffects:
        # print("x = " + str(len(x)))
        for y in x:
            for z in y:
                if z == "N/A":
                    unkownEffects.append(x)
    #for x in unkownEffects:
        # print("x = " + str(len(x)))
        #for y in x:
        #   for z in y:
        #        print("x = " + str(x))
        #       print("y = " + str(y))
        #        print("z = " + str(z))


    return unkownEffects

def main():
    print("Validating Basic Style - Secondary Check")

    files_list = []
    nation_focus_files = []
    idea_files = []
    bad_count = 0
    tags = []


    # Allow running from root directory as well as from inside the tools directory
    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))

    tags = get_tags(rootDir + "/common/country_tags/00_countries.txt")
    allTriggers, allEffects = findPdxSyntax(rootDir + "/Modding resources/List of triggers and effects 1_5_4.txt")
    countryTriggers = getCountryTriggers(allTriggers)
    stateTriggers = getStateTriggers(allTriggers)
    unkownTriggers = getUnkownTriggers(allTriggers)
    countryEffects = getCountryEffects(allEffects)
    stateEffects = getStateEffects(allEffects)
    unkownEffects = getUnkownEffects(allEffects)
    globalFlags = []
    countryFlags = []

    for root, dirnames, filenames in os.walk(rootDir + '/' + 'common' + '/national_focus' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            if filename != "generic.txt":
                bad_count = bad_count + checkFocuses(os.path.join(root, filename))
                files_list.append(os.path.join(root, filename))

    for root, dirnames, filenames in os.walk(rootDir + '/' + 'common' + '/ideas' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            bad_count = bad_count + check_ideas(os.path.join(root, filename))
            files_list.append(os.path.join(root, filename))


    #for root, dirnames, filenames in os.walk(rootDir + '/' + 'common/'):
        #for filename in fnmatch.filter(filenames, '*.txt'):
            #temp, temp1, temp2 = check_Flags(os.path.join(root, filename))
            #bad_count += temp
            #globalFlags += temp1
            #countryFlags += temp1
    #for root, dirnames, filenames in os.walk(rootDir + '/' + 'events/'):
        #for filename in fnmatch.filter(filenames, '*.txt'):
            #temp, temp1, temp2 = check_Flags(os.path.join(root, filename))

            # globalFlags += temp1
            # countryFlags += temp1
    #for root, dirnames, filenames in os.walk(rootDir + '/' + 'history/'):
        #for filename in fnmatch.filter(filenames, '*.txt'):
            # temp, temp1, temp2 = check_Flags(os.path.join(root, filename))
            # bad_count += temp
            # globalFlags += temp1
            # countryFlags += temp1
    for root, dirnames, filenames in os.walk(rootDir + '/' + 'events/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            bad_count = bad_count + check_event_for_logs(os.path.join(root, filename))
            files_list.append(os.path.join(root, filename))

    #input()
    # bad_count = bad_count + check_focus_tree_file_name(nation_focus_files)

    # for root, dirnames, filenames in os.walk(rootDir + '/'+ 'common' + '/' + 'national_focus' + '/'):
    #    for filename in fnmatch.filter(filenames, '*.txt'):
    #       files_list.append(os.path.join(root, filename))
    # for root, dirnames, filenames in os.walk(rootDir + '/'+ 'common' + '/' + 'national_focus' + '/'):
    #   for filename in fnmatch.filter(filenames, '*.txt'):
    #       files_list.append(os.path.join(root, filename))

    # for root, dirnames, filenames in os.walk(rootDir + '/'+ 'events' + '/'):
    #    for filename in fnmatch.filter(filenames, '*.txt'):
    #        files_list.append(os.path.join(root, filename))

    # for root, dirnames, filenames in os.walk(rootDir + '/'+ 'history' + '/'):
    #   for filename in fnmatch.filter(filenames, '*.txt'):
    #       files_list.append(os.path.join(root, filename))

    # for filename in files_list:
    #    bad_count = bad_count + check_basic_style(filename)

    print("------\nChecked {0} files\nErrors detected: {1}".format(len(files_list), bad_count))
    if (bad_count == 0):
        print("File validation PASSED")
    else:
        print("File validation FAILED")

    print('The script took {0} second!'.format(time.time() - startTime))

    return bad_count


if __name__ == "__main__":
    sys.exit(main())
