import sys
import time
from os import listdir
from os import path
from codecs import open
import random




def main():
    #File to change has to be an argument
    cpath = sys.argv[1]
    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string

    #Set the script to either subtract the same amount each time or lower by a %
    absolute = True
    #Set the change
    change = -1

    #Open the target file
    with open(cpath, 'r', 'utf-8') as file:
        #Create a copy to ensure we dont overwrite anything and erase it if already exists
        target_file = open(cpath.split('.')[0]+'_cost_changed.txt', 'w', 'utf-8')
        target_file.truncate()
        #read all lines into memory because we dont care about a few kilobites
        lines = file.readlines()
        #Loop over all lines
        for x in range(0, len(lines)):
            #Could do a foreach, but hey, sometimes an index is needed
            line = lines[x]

            #Check for a comment, and if so, strip it away so we dont get false positives
            if '#' in line:
                line_check = line.split('#')[0].strip()
            else:
                line_check = line.strip()

            #Detect the cost command in our cleaned line
            if 'cost' in line_check:
                #Check for the absolute mode
                if absolute:
                    #Add the change
                    cost = float(line_check.split('=')[1])+change
                else:
                    #Multiply by 1 + change
                    cost = float(line_check.split('=')[1])*(1+change)

                #print("found cost", cost-1, "at line", x)
                #Print the line, copying the original whitespace and then the cost
                #Can remove comments, but hey, no one comments the cost line (right)
                target_file.write(line.split('c')[0] + 'cost = ' + str(cost) + '\n')
            else:
                #If no cost in line, just spit the og line out
                target_file.write(line)
    #Cap the sucker
    target_file.close()

if __name__ == "__main__":
    main()