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

def checkAirBases (rootDir, tags):
    hasAirBase = []

    with open(rootDir, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        owner = ""
        airBase = 0
        for line in content:
            if "owner" in line:
                hasOwner = re.search(r'owner\s=\s([A-Z]{3})', line, re.M | re.I)  # If it's a tag
                #print (line)
                if hasOwner:
                    if hasOwner.group(1) in tags:
                        owner = hasOwner.group(1)
            if "air_base" in line:
                airBase = 1
        else:
            if owner != "" and airBase != 0:
                hasAirBase.append(owner
                                  )
    return hasAirBase

def main():
    print("Who doesn't have airbases?")

    files_list = []
    nation_focus_files = []
    idea_files = []
    bad_count = 0
    tags = []
    hasAirBases = []

    # Allow running from root directory as well as from inside the tools directory
    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))

    tags = get_tags(rootDir + "/common/country_tags/00_countries.txt")
    for root, dirnames, filenames in os.walk(rootDir + '/' + 'history' + '/states' + '/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            hasAirBases = hasAirBases + checkAirBases ((os.path.join(root, filename)), tags)

    #hasAirBases = noAirbases + tags
    hasAirBases = list(set(hasAirBases))
    noAirbases = [x for x in tags if x not in hasAirBases]
    for x in noAirbases:
      print(x)

    print('The script took {0} second!'.format(time.time() - startTime))

    return bad_count


if __name__ == "__main__":
    sys.exit(main())
