from codecs import open
import sys
from os import listdir
import os


def tech(cpath):
    #on_research_complete = {  log = "[GetDateText] [Root.GetName]: add tech advanced_light_spaa"}
    for filename in listdir(cpath + "\\common\\technologies"):
        outputfile = open(cpath + "\\common\\technologies\\" + filename, 'r', 'utf-8')
        size = os.path.getsize(cpath + "\\common\\technologies\\" + filename)
        if size < 100:
            continue
        lines = outputfile.readlines()
        outputfile.close()
        outputfile = open(cpath + "\\common\\technologies\\" + filename, 'w', 'utf-8')
        outputfile.truncate()

        for x in range(len(lines)):
            line = lines[x]
            #print(x.__str__()+":", line[:-1])
            if 'log = "[GetDateText]' in line and (("{" in line and "}" in line) or ("{" not in line and "}" not in line)):
                outputfile.write("")
            elif 'log = "[GetDateText]' in line and "{" in line:
                outputfile.write(line.split("{")[0] + "{\n")
            elif 'on_research_complete' in line and 'log = "[GetDateText]' in lines[x+1] and ( '}' in lines[x+2] or '}' in lines[x+1]):
                #print("Deleted logging at line", x, "in file", filename)
                outputfile.write("")
            elif 'log = "[GetDateText]' in lines[x-1]and '}' in line and 'on_research_complete' in lines[x-2]:
                outputfile.write("")
            else:
                outputfile.write(line)

def focus(cpath):
    #immediate = { log = "Focus id: "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\common\\national_focus"):
        if ".txt" in filename:
            linenumber = 0
            outputfile = open(cpath + "\\common\\national_focus\\" + filename, 'r', 'utf-8')
            size = os.path.getsize(cpath + "\\common\\national_focus\\" + filename)
            if size < 100:
                continue
            lines = outputfile.readlines()
            outputfile.close()
            outputfile = open(cpath + "\\common\\national_focus\\" + filename, 'w', 'utf-8')
            outputfile.truncate()
            for line in lines:
                linenumber += 1
                if 'log = "[GetDateText]' not in line:
                    outputfile.write(line)
                else:
                    outputfile.write("")

def event(cpath):
    # immediate = { log = "[Root.GetName]: event "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\events"):
        if ".txt" in filename:
            outputfile = open(cpath + "\\events\\" + filename, 'r', 'utf-8-sig')
            size = os.path.getsize(cpath + "\\events\\" + filename)
            if size < 100:
                continue
            try:
                lines = outputfile.readlines()
            except UnicodeDecodeError:
                print(filename)
                continue
            outputfile.close()
            outputfile = open(cpath + "\\events\\" + filename, 'w', 'utf-8-sig')
            outputfile.truncate()
            for line in lines:
                if 'log = ' not in line:
                    outputfile.write(line)
                else:
                    if '}' in line:
                        outputfile.write("")
                    elif "immediate" in line:
                        outputfile.write("\timmediate = {\n")
                    else:
                        outputfile.write("")

    for filename in listdir(cpath + "\\events"):
        if ".txt" in filename:
            delete_next_line = False
            outputfile = open(cpath + "\\events\\" + filename, 'r', 'utf-8-sig')
            size = os.path.getsize(cpath + "\\events\\" + filename)
            if size < 100:
                continue
            try:
                lines = outputfile.readlines()
            except UnicodeDecodeError:
                print(filename)
                continue
            outputfile.close()
            outputfile = open(cpath + "\\events\\" + filename, 'w', 'utf-8-sig')
            outputfile.truncate()
            for linenumber, line in enumerate(lines):
                if delete_next_line is True:
                    outputfile.write("")
                    delete_next_line = False
                elif "immediate = {" == line.strip() and "}" == lines[linenumber+1].strip():
                    outputfile.write("")
                    delete_next_line = True
                else:
                    outputfile.write(line)


def idea(cpath):
    # immediate = { log = "[Root.GetName]: event "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\common\\ideas"):
        if ".txt" in filename and filename.startswith('_') is False:
            outputfile = open(cpath + "\\common\\ideas\\" + filename, 'r', 'utf-8')
            size = os.path.getsize(cpath + "\\common\\ideas\\" + filename)
            if size < 100:
                continue
            lines = outputfile.readlines()
            outputfile.close()
            outputfile = open(cpath + "\\common\\ideas\\" + filename, 'w', 'utf-8')
            outputfile.truncate()
            for line in lines:
                if 'log = ' not in line:
                    outputfile.write(line)
                else:
                    outputfile.write("")


def decision(cpath):
    # immediate = { log = "[Root.GetName]: event "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\common\\decisions"):
        if ".txt" in filename and 'categories' not in filename:
            outputfile = open(cpath + "\\common\\decisions\\" + filename, 'r', 'utf-8')
            size = os.path.getsize(cpath + "\\common\\decisions\\" + filename)
            if size < 100:
                continue
            lines = outputfile.readlines()
            outputfile.close()
            outputfile = open(cpath + "\\common\\decisions\\" + filename, 'w', 'utf-8')
            outputfile.truncate()
            for line in lines:
                if 'log = "[GetDateText]' not in line:
                    outputfile.write(line)
                else:
                    if 'complete_effect' in line:
                        outputfile.write("complete_effect = {\n\t\t}\n")
                    else:
                        outputfile.write("")


def main():
    cpath = sys.argv[1]


    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string

    if cpath is "":
        print("Expected a path to a mod folder.")
    else:
        event(cpath)
        focus(cpath)
        idea(cpath)
        decision(cpath)
        tech(cpath)

if __name__ == "__main__":
    main()

