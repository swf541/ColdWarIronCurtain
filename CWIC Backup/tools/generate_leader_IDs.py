#!/usr/bin/env python3
import os, sys, fnmatch, re

__version__ = 1.0

def main():
    print("Validating Basic Style")

    files_list = []
    leaderID = 1
    idRange = 0

    # Allow running from root directory as well as from inside the tools directory
    scriptDir = os.path.realpath(__file__)
    rootDir = os.path.dirname(os.path.dirname(scriptDir))

    for root, dirnames, filenames in os.walk(rootDir + '/' + 'history/countries/'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            files_list.append(os.path.join(root, filename))
            print(filename)

    for filename in files_list:
        newContent = ""
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.readlines()
            writeSkill = 1
            for line in content:
                hasSkill = re.search(r'([ \t]+)skill[ \t]+?=[ \t]+?([0-9]+)', line, re.M | re.I)
                hasNavyLeader = re.search(r'[ \t]+?create_navy_leader', line, re.M | re.I)

                if hasNavyLeader:
                    writeSkill = 0

                if hasSkill:
                    newContent += hasSkill.group(1)+ "id = " + str(leaderID) + "\n"
                    leaderID += 1
                    if writeSkill == 1:
                        newContent += hasSkill.group(1)+ "skill = " + hasSkill.group(2) + "\n"
                        newContent += hasSkill.group(1)+ "attack_skill = " + hasSkill.group(2)+ "\n"
                        newContent += hasSkill.group(1)+ "defense_skill = " + hasSkill.group(2)+ "\n"
                        newContent += hasSkill.group(1)+ "planning_skill = " + hasSkill.group(2)+ "\n"
                        newContent += hasSkill.group(1)+ "logistics_skill = " + hasSkill.group(2)+ "\n"
                    writeSkill = 1
                else:
                    newContent += line
        #print(newContent)
        file.close()
        with open(filename, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(newContent)
            print("Updated: ", filename, "/n")
        file.close()
        idRange +=300
        leaderID = (idRange)
        #input("Press Enter to continue...")

    print ("Generation completed")

if __name__ == "__main__":
    sys.exit(main())
