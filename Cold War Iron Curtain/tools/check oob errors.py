#!/usr/bin/env python3
import os, sys, fnmatch, re
import time

startTime = time.time()

__version__ = 1.0


def get_tags(rootDir):
    tags = []
    pos =0
    with open(rootDir, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        for line in content:
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                hasTag = re.match(r'^[A-Z]{3}', line, re.M | re.I)  # If it's a tag
                if hasTag:
                    tags.append([[hasTag.group()]])
                    pos +=1
    #input()
    return tags

def get_tech(rootDir, tags, tagPos):
    with open(rootDir, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        foundTech = 0
        openBrace = 0
        startDate = 0
        updatedTags = tags
        updatedTags[tagPos].append([])
        updatedTags[tagPos].append([])

        #input()
        for line in content:
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "2000.1.1" in line:
                    startDate = 1
                if startDate == 1:
                    if "set_technology" in line:
                        foundTech = 1
                    if foundTech ==1:
                         if "{" in line:
                            openBrace =1
                         if "}" in line:
                            openBrace = 0
                            foundTech =0

                    if openBrace ==1:
                        hasTech = re.search(r'[ \t]+([A-Za-z0-9_\-]+)\s?=\s?1', line, re.M | re.I)  # If it's a tag
                        if hasTech:
                           #updatedTags[tagPos].append([])
                           updatedTags[tagPos][1].append(hasTech.group(1))

                if "2017.1.1" in line:
                    startDate = 2
                if startDate == 2:
                    if "set_technology" in line:
                        foundTech = 1
                    if foundTech ==1:
                        if "{" in line:
                            openBrace =1
                        if "}" in line:
                            openBrace = 0
                            foundTech = 0

                    if openBrace ==1:
                        hasTech = re.search(r'[ \t]+([A-Za-z0-9_\-]+)\s?=\s?1', line, re.M | re.I)  # If it's a tag
                        if hasTech:
                            #updatedTags[tagPos].append([])
                            updatedTags[tagPos][2].append(hasTech.group(1))
                            #print(updatedTags[tagPos][2])
        #print(updatedTags[tagPos][1])
        #print(updatedTags[tagPos][2])
        #input()
    return updatedTags

def get_variants(rootDir, tags, tagPos):
    with open(rootDir, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        foundVariant = 0
        openBrace = 0
        startDate = 0
        variants = tags
        variants[tagPos].append([[]])
        variants[tagPos].append([[]])
        variantCount = 0

        for line in content:
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "2000.1.1" in line:
                    startDate = 1
                if startDate == 1:
                    if "create_equipment_variant" in line:
                        foundVariant = 1
                    if foundVariant ==1:
                        if "{" in line:
                            openBrace +=1
                        if "}" in line:
                            openBrace -= 1
                    if openBrace ==0:
                        foundVariant = 0

                    if openBrace ==1 and ("name" in line or "type" in line):
                        variantName = re.search(r'name\s?=\s?\"(.*)\"', line, re.M | re.I)  # If it's a tag
                        variantType = re.search(r'type\s?=\s?(.*)', line, re.M | re.I)  # If it's a tag

                        if variantName:
                            variants[tagPos][3][0].append(variantName.group(1))
                            variantCount +=1
                        if variantType:
                            variants[tagPos][3][0].append(variantType.group(1))

                if "2017.1.1" in line:
                    startDate = 2
                if startDate == 2:
                    if "create_equipment_variant" in line:
                        foundVariant = 1
                    if foundVariant ==1:
                        if "{" in line:
                            openBrace +=1
                        if "}" in line:
                            openBrace -= 1
                    if openBrace ==0:
                        foundVariant = 0

                    if openBrace ==1 and ("name" in line or "type" in line):
                        variantName = re.search(r'name\s?=\s?\"(.*)\"', line, re.M | re.I)  # If it's a tag
                        variantType = re.search(r'type\s?=\s?(.*)', line, re.M | re.I)  # If it's a tag
                        if variantName:
                            variants[tagPos][4][0].append(variantName.group(1))
                            variantCount += 1
                        if variantType:
                            variants[tagPos][4][0].append(variantType.group(1))
    return variants

def get_tagPos(text, tags):
    isValidTag = re.match(r'^([A-Z]{3})\s.*-', text, re.M | re.I)  # If filename has a tag in it
    tagPos = -1
    if isValidTag:
        for pos, x in enumerate(tags):
            for y in x:
                # pos = 0
                for z in y:
                    if z == isValidTag.group(1):
                        tagPos = pos
                        return tagPos


def get_tagPos2(text, tags):
    isValidTag = re.match(r'([A-Z]{3})', text, re.M | re.I)  # If filename has a tag in it
    tagPos = -1
    if isValidTag:
        for pos, x in enumerate(tags):
            for y in x:
                # pos = 0
                for z in y:
                    if z == isValidTag.group(1):
                        tagPos = pos
                        return tagPos

def analyzeMyVariants(tags, rootDir, fileName):
    variants = tags
    # tagPos = get_tagPos2("SOV", tags)
    # for pos, x in enumerate(tags[tagPos]):
    #     if pos ==0:
    #         print("~~~~tag:~~~~")
    #     if pos ==1:
    #         print("~~~2000 tech:~~~")
    #     if pos ==2:
    #         print("~~~2017 tech:~~~")
    #     if pos ==3:
    #         print("~~~2000 var:~~~")
    #     if pos ==4:
    #         print("~~~2017 var:~~~")
    #
    #     for y in x:
    #         if pos != 3 and pos != 4:
    #             print (y)
    #         else:
    #             #input()
    #             for pos1, z in enumerate(y):
    #                 print(z)
    # input()

    startDate = 0
    has2kStart = re.search(r'2000', rootDir, re.I)  # If it's a tag
    has2k17Start = re.search(r'2017', rootDir, re.I)  # If it's a tag
    if has2kStart:
        startDate = 1
    elif has2k17Start:
        startDate = 2

    global totalErrors

    with open(rootDir, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()

        startReading = 0
        openBrace = 0
        creator = ""
        version_name = ""
        equipment_name = ""
        tagPos = -1
        stockpile = 0
        production = 0
        ship = 0

        for line in content:
            if not line.startswith("#") or line.startswith(""):  # If the line doesn't start with a comment or blank
                if "ship" in line and "#ship" not in line:
                    ship = 1
                    startReading = 1
                if "add_equipment_to_stockpile" in line and "#add_equipment_to_stockpile" not in line:
                    stockpile = 1
                    startReading = 1
                if "add_equipment_production" in line and "#add_equipment_production" not in line:
                    production = 1
                    startReading = 1
                if startReading ==1:
                    if "{" in line:
                        openBrace += 1
                    if "}" in line:
                        openBrace -=1
                    if ship ==1:
                        hasEquipment = re.search(r'equipment\s?=\s?{\s?([A-Za-z0-9_\-]+)\s?=', line, re.M | re.I)  # If it's a tag
                        hasVersion = re.search(r'version_name\s?=\s?\"(.*)\"', line, re.M | re.I)  # If it's a tag
                        hasCreator = re.search(r'creator\s?=\s?([A-Z]{3})', line, re.M | re.I)  # If it's a tag
                        hasOwner = re.search(r'owner\s?=\s?([A-Z]{3})', line, re.M | re.I)  # If it's a tag
                        if hasCreator:
                            creator = hasCreator.group(1)
                        if hasVersion:
                            version_name = hasVersion.group(1)
                        if hasEquipment:
                            equipment_name = hasEquipment.group(1)
                        if not hasCreator and hasOwner:
                            creator = hasOwner.group(1)
                        if not hasVersion and hasOwner:
                            hasVersion = "yes"
                            version_name = "yes"
                            ship = 2
                    if stockpile ==1: #change to 1, set at 5 as I need to fix techs
                        hasEquipment = re.search(r'type\s?=\s?([A-Za-z0-9_\-]+)', line, re.M | re.I)  # If it's a tag
                        hasVersion = re.search(r'version_name\s?=\s?\"(.*)\"', line, re.M | re.I)  # If it's a tag
                        hasCreator = re.search(r'producer\s?=\s?([A-Z]{3})', line, re.M | re.I)  # If it's a tag
                        hasOwner = re.search(r'([A-Z]{3})_', fileName, re.M | re.I)  # If it's a tag
                        if hasCreator:
                            creator = hasCreator.group(1)
                        if hasVersion:
                            version_name = hasVersion.group(1)
                        if hasEquipment:
                            equipment_name = hasEquipment.group(1)
                        if not creator and hasOwner and openBrace ==0:
                            creator = hasOwner.group(1)
                        if not hasVersion and hasOwner:
                            hasVersion = "yes"
                            version_name = "yes"
                            ship = 2
                    if production ==1: #change to 1, set at 5 as I need to fix techs
                        hasEquipment = re.search(r'type\s?=\s?([A-Za-z0-9_\-]+)', line, re.M | re.I)  # If it's a tag
                        hasVersion = re.search(r'version_name\s?=\s?\"(.*)\"', line, re.M | re.I)  # If it's a tag
                        hasCreator = re.search(r'creator\s?=\s?\"([A-Z]{3})\"', line, re.M | re.I)  # If it's a tag
                        hasOwner = re.search(r'([A-Z]{3})_', fileName, re.M | re.I)  # If it's a tag
                        if hasCreator:
                            creator = hasCreator.group(1)
                        if hasVersion:
                            version_name = hasVersion.group(1)
                        if hasEquipment:
                            equipment_name = hasEquipment.group(1)
                        if creator == hasOwner.group(1):
                            creator = hasOwner.group(1)
                        if not version_name and creator:
                            hasVersion = "yes"
                            version_name = "yes"
                            production = 2



                    if creator and version_name and equipment_name:
                        foundVar, foundTech = check_variant(creator, version_name, equipment_name, startDate, tags)

                        if version_name != "yes" and foundVar == 0 and (ship == 1 or production == 1):
                            #print(startDate)
                            print("ERROR: " + version_name + " " + equipment_name + " from " + creator +" was used in " + fileName + " but doesn't exist")
                            totalErrors += 1
                            #input()
                            ship = 0
                            stockpile = 0
                            production = 0
                            startReading = 0
                        if foundTech == 0:
                            #print(startDate)
                            print("ERROR: " + equipment_name + " from " + creator +" was used in " + fileName + " but " + creator + " doesn't have this tech unlocked")
                            #print(equipment_name)
                            #print(creator)
                            totalErrors += 1
                            #input()
                            ship = 0
                            stockpile = 0
                            production = 0
                            startReading = 0
                        creator = ""
                        version_name = ""
                        equipment_name = ""


                    if openBrace == 0:
                        ship = 0
                        stockpile = 0
                        production = 0
                        startReading = 0
                        creator = ""
                        version_name = ""
                        equipment_name = ""



    return variants

def check_variant (creator, version_name, equipment_name, startDate, tags):
    foundVar = 0
    foundTech = 0

    tagPos = get_tagPos2(creator, tags)
    if tagPos != -1 and creator == tags[tagPos][0][0]:
        foundVar = 0
        if startDate == 1 or startDate == 2:
            for x in tags[tagPos][3]:
                for y in x:
                    # print(y)
                    if version_name == y:
                        foundVar = 1
            for x in tags[tagPos][1]:
                #print (x)
                #input()
                if equipment_name == x:
                    foundTech = 1

        if foundVar == 0 and startDate == 2:
            for x in tags[tagPos][4]:
                for y in x:
                    # print(y)
                    if version_name == y:
                        foundVar = 1
            for x in tags[tagPos][2]:
                if equipment_name == x:
                    foundTech = 1
    return foundVar, foundTech


def main():
    files_list = []
    nation_focus_files = []
    idea_files = []
    bad_count = 0
    tags = []
    hasAirBases = []
    tagPos = -1
    # Allow running from root directory as well as from inside the tools directory
    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))
    global totalErrors
    totalErrors = 0

    tags = get_tags(rootDir + "/common/country_tags/00_countries.txt")

    for root, dirnames, filenames in os.walk(rootDir + '/' + 'history' + '/countries' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            tagPos = -1
            tagPos = get_tagPos(filename, tags)
            if tagPos != -1:
                tags = get_tech((os.path.join(root, filename)), tags, tagPos)
                tags = get_variants((os.path.join(root, filename)), tags, tagPos)
                #tags = analyzeMyVariants(tags)
                #tagPos = get_tagPos2("SOV", tags)

    for root, dirnames, filenames in os.walk(rootDir + '/' + 'history' + '/units' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            analyzeMyVariants(tags, os.path.join(root, filename), filename)




    print('The script took {0} second!'.format(time.time() - startTime) + " therea are a total of: " + str(totalErrors) + " errors.")

    return bad_count


if __name__ == "__main__":
    sys.exit(main())