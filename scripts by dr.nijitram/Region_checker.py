from codecs import open
import sys
from os import listdir
import time
import os
import re


def convert_oob(modpath):

    path = os.path.join(modpath, "history", "units")
    path_3 = os.path.join(modpath, "history", "countries")

    examine_path = path
    navies = set()
    uniquely_navies = set()

    for filename in listdir(examine_path):
        with open(os.path.join(examine_path, filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()

            level = 0
            search = False
            others = False
            navy_pairs = dict() # Start line: end line
            temp_line = 0

            for line_number, line in enumerate(lines):

                if '#' in line:
                    if line.strip().startswith("#") is True:
                        continue
                    else:
                        line = line.split('#')[0]

                if 'navy' in line:
                    temp_line = line_number
                    search = True

                if "division" in line or "air_wings" in line:
                    others = True

                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

                if search is True and '}' in line and level == 1:
                    navy_pairs[temp_line] = line_number +1
                    search = False




            if(len(navy_pairs)) == 0:
                continue
            elif others is False:
                uniquely_navies.add("\"" + filename[:-4] + "\"")
            else:
                navies.add("\"" + filename[:-4] + "\"")

            start_numbers = list(navy_pairs.keys())
            end_numbers = list(navy_pairs.values())


            if others is True:
                with open(os.path.join(examine_path, filename), 'w', 'utf-8-sig') as outputfile:
                    outputfile.truncate()

                    navy_file = open(os.path.join(examine_path, filename[:-4] + "_naval.txt"), 'w', 'utf-8-sig')
                    navy_file.truncate()

                    navy_file.write("### OOB for file " + filename + "\nunits = {\n")

                    other_file = False
                    inline = False
                    name = ""

                    for line_number, line in enumerate(lines):
                        if line_number in end_numbers:
                            inline = False
                            navy_file.write("\t}\n\n")
                            other_file = False
                        if line_number in start_numbers:
                            other_file = True


                        if other_file is False:
                            outputfile.write(line)
                        else:

                            if "navy" in line:
                                line = "\tfleet = {\n"
                                inline = False
                            if 'base' in line:
                                line = "\t\tnaval_base =" + line.split("=")[1]
                            if 'name' in line:
                                name = line.split("=")[1].strip()
                            if 'location' in line:
                                line = "\ttask_force = {\n\t\t\tname = " + name + "\n\t\t\t" + line.strip() + "\n"
                                inline = True

                            if inline:
                                line = "\t" + line

                            navy_file.write(line)

                    navy_file.write("}")
                    navy_file.close()
            else:
                with open(os.path.join(examine_path, filename), 'w', 'utf-8-sig') as outputfile:
                    outputfile.truncate()

                    other_file = False
                    inline = False
                    name = ""

                    for line_number, line in enumerate(lines):
                        if line_number in start_numbers:
                            other_file = True
                        elif line_number in end_numbers:
                            inline = False
                            outputfile.write("\t}\n\n")
                            other_file = False

                        if other_file is False:
                            outputfile.write(line)
                        else:

                            if "navy" in line:
                                line = "\tfleet = {\n"
                            if 'base' in line:
                                line = "\t\tnaval_base =" + line.split("=")[1]
                            if 'name' in line:
                                name = line.split("=")[1].strip()
                            if 'location' in line:
                                line = "\ttask_force = {\n\t\t\tname = " + name + "\n\t\t\t" + line.strip() + "\n"
                                inline = True

                            if inline:
                                line = "\t" + line

                            outputfile.write(line)

    print(navies)
    print(uniquely_navies)

    examine_path = path_3
    for filename in listdir(examine_path):
        with open(os.path.join(examine_path, filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()

        with open(os.path.join(examine_path, filename), 'w', 'utf-8-sig') as outputfile:
            outputfile.truncate()

            for line_number, line in enumerate(lines):
                if 'oob' in line or 'OOB' in line:
                    if line.split("=")[1].strip() in navies:
                        line = line + "set_naval_oob = " + line.split("=")[1].strip()[:-1] + "_naval\"\n"
                    elif line.split("=")[1].strip() in uniquely_navies:
                        print(line.split("=")[1].strip())
                        line = "set_naval_oob = " + line.split("=")[1].strip()[:-1] + "_naval\"\n"
                outputfile.write(line)


def strat_region(gamepath, modpath):

    path = os.path.join(modpath, "map", "strategicregions")
    path_2 = os.path.join(gamepath, "map", "strategicregions")
    path_3 = os.path.join(modpath, "map", "definition.csv")


    filenames = {"filename": "naval_terrain = x"}


    for filename in listdir(path_2):
        with open(os.path.join(path_2, filename), 'r', 'utf-8') as file:
            lines = file.readlines()
            for lineno, line in enumerate(lines):
                if 'naval_terrain' in line:
                    filenames[filename] = line.strip()

    ocean = set()
    files = list(filenames.keys())
    print(files)

    with open(path_3, 'r', 'utf-8') as file:
        lines = file.readlines()
        for lineno, line in enumerate(lines):
            stuff = line.strip().split(";")
            if stuff[6] == 'ocean':
                ocean.add(int(stuff[0]))



    for filename in listdir(path):
        with open(os.path.join(path, filename), 'r', 'utf-8') as file:
            lines = file.readlines()

        to_check = False

        for lineno, line in enumerate(lines):
            if 'provinces' in line:
                this_id = set([int(_) for _ in lines[lineno + 1].strip().split(" ") if _ not in ["", " "]])

                if ocean.intersection(this_id) != set():

                    if filename in files:
                        to_check = True
                    else:
                        print(filename)

            if 'naval_terrain' in line:
                to_check = False

        if to_check:
            with open(os.path.join(path, filename), 'w', 'utf-8') as outputfile:
                outputfile.truncate()

                for line_number, line in enumerate(lines):

                    if line.strip().startswith('#'):
                        outputfile.write(line)
                        continue

                    replacement_text = line

                    if 'weather' in line:
                        replacement_text = "\t" + filenames[filename] + "\n" + line

                    outputfile.write(replacement_text)


def tech(modpath):

    path_1 = os.path.join(modpath, "common", "technologies")
    path_2 = os.path.join(modpath, "common", "ideas")
    path_3 = os.path.join(modpath, "common", "country_leader")

    for path in [path_1, path_2, path_3]:
        for filename in listdir(path):
            with open(os.path.join(path, filename), 'r', 'utf-8') as file:
                lines = file.readlines()

            with open(os.path.join(path, filename), 'w', 'utf-8') as outputfile:

                outputfile.truncate()

                for line_number, line in enumerate(lines):

                    if line.strip().startswith('#'):
                        outputfile.write(line)
                        continue

                    replacement_text = line

                    if 'research_time_factor' in line:

                        if '{' in line:
                            amount = float(line.split("=")[2].split("}")[0].split("#")[0].strip())
                        else:
                            amount = float(line.split("=")[1].split("}")[0].split("#")[0].strip())

                        if amount < abs(0.1000000001):
                            amount = round(-1*amount, 3)
                        else:
                            amount = round((1/(amount + 1))-1, 3)

                        replacement_text = "\t\t\t\t" + "research_speed_factor = " + str(amount) + line.split('=')[1][6:]



                    outputfile.write(replacement_text)


def fix_oob_calls(modpath):

    path = os.path.join(modpath, "history", "units")

    naval_oobs = set()

    for filename in listdir(path):
        if "_naval" in filename:
            naval_oobs.add(filename[:-4])

    #print(naval_oobs)

    # Scripted Effects
    # Decisions
    # National Focus
    # Events
    # Technologies


    paths = ["events", "common\\decisions", "common\\scripted_triggers", "common\\technologies", "common\\national_focus"]
    for pth in paths:
        if pth == "events":
            encoding = "utf-8-sig"
        else:
            encoding = "utf-8"
        for filename in listdir(os.path.join(modpath, pth)):

            # listdir also provides directories and this is very annoying thank you very much
            if 'categories' in filename:
                continue

            with open(os.path.join(modpath, pth, filename), 'r+', encoding) as file:
                lines = file.readlines()

                line_nos = set()

                for line_number, line in enumerate(lines):
                    if '#' in line:
                        if line.strip().startswith("#") is True:
                            continue
                        else:
                            line = line.split('#')[0]

                    if "oob" in line:
                        oob = line.split("=")[1].strip()
                        if "\"" in oob or "\'" in oob:
                            oob = oob[1:-1]

                        oob = "" + oob + "_naval"
                        if oob in naval_oobs and 'naval' not in lines[line_number+1]:
                            line_nos.add(line_number)

            if line_nos == set():
                continue

            with open(os.path.join(modpath, pth , filename), 'w', encoding) as outputfile:
                outputfile.truncate()

                for line_number, line in enumerate(lines):

                    if line.strip().startswith('#'):
                        outputfile.write(line)
                        continue

                    if line_number in line_nos:


                        if '}' in line:
                            if line.count("}") > 1:
                                print(line)
                                exit(-1)

                            line = line.split("}")[0]

                        oob = line.split("=")[1].strip()
                        if "\"" in oob or "\'" in oob:
                            oob = oob[1:-1]
                        oob = "" + oob + "_naval"

                        outputfile.write(line)
                        outputfile.write(line[:len(line)-len(line.lstrip())] + "load_oob = " + oob + "\n")
                        if '}' in line:
                            outputfile.write("}\n")

                    else:
                        outputfile.write(line)


def check_ship_names(modpath):

    names_path = os.path.join(modpath, "common", "units", "names")
    oob_path = os.path.join(modpath, "history", "units")

    # names in oob, always over namelists
    bad = False

    oob_names_total = set()

    pattern = r'{\s?name\s?=\s?"([1-9.a-zA-Z ]+)"'
    for filename in listdir(oob_path):
        oob_names = set()
        with open(os.path.join(oob_path, filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()

            for line in lines:
                math = re.search(pattern, line)
                if math is not None:
                    if math.group(1) not in oob_names:
                        oob_names.add(math.group(1))
                        oob_names_total.add(math.group(1))
                    else:
                        print(filename, math.group(1))
                        bad = True

    if bad:
        print("Found duplicate names in oobs, aborting")
        return(-1)
    else:
        print("Found no duplicate ships in oobs, continuing")

    names_list_names = set()


    for filename in listdir(names_path):
        with open(os.path.join(names_path, filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()
            level = 0
            searching = False
            super_search = False
            names = ""
            prefix = ""
            names_list = []
            i = 0
            for line in lines:

                if '#' in line:
                    if line.strip().startswith("#") is True:
                        continue
                    else:
                        line = line.split('#')[0]

                if level == 1 and '{' in line:
                    name = line.split("=")[0].strip()
                    if name in ['submarine', 'destroyer', 'light_cruiser', 'heavy_cruiser', 'battleship', 'SH_battleship', 'carrier', 'heavy_carrier']:
                        names = ""
                        searching = True
                    else:
                        searching = False

                if searching:
                    if 'prefix' in line:
                        prefix = line.split("=")[1].strip()[1:-1]
                        if len(prefix) > 0:
                            prefix += " "

                        print(filename, prefix)
                    elif 'unique' in line:
                        super_search = True
                    elif super_search is True:
                        if '}' in line:
                            super_search = False
                            searching = False

                            names = [prefix + name for name in names[1:-1].split("\" \"") if name.strip() != ""]

                            names_set = set(names)

                            #if oob_names_total.intersection(names_set) != set():
                            #print("already present in an oob:", len(oob_names_total.intersection(names_set)))
                            #if names_list_names.intersection(names_set) != set():
                            #print("already present in another namelist:", len(names_list_names.intersection(names_set)))


                            #print("Total names in namelist:", len(names_set))
                            #print("Total names left", len(names_set.difference(oob_names_total).difference(names_list_names)))
                            #print(names_set.difference(oob_names_total).difference(names_list_names))
                            #if len(names_set.difference(oob_names_total).difference(names_list_names)) == 0:
                            #    zero_left += 1
                            #names_list.append(names_set.difference(oob_names_total).difference(names_list_names))
                            names_list.append([name[len(prefix):] for name in names if name not in list(oob_names_total) and name not in list(names_list_names)])
                            names_list_names.update(names_set)
                            i += 1
                            #print("\n")
                        else:
                            names += line.strip() + " "



                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

        # Read the file

        with open(os.path.join(names_path, filename), 'w', 'utf-8-sig') as file:
            file.truncate()
            i = 0
            level = 0
            searching = False
            super_search = False
            block = False
            for lineno, line in enumerate(lines):

                if line.strip().startswith("#") is True:
                    file.write(line)
                    continue



                if level == 1 and '{' in line:
                    name = line.split("=")[0].strip()
                    if name in ['submarine', 'destroyer', 'light_cruiser', 'heavy_cruiser', 'battleship', 'SH_battleship', 'carrier', 'heavy_carrier']:
                        names = ""
                        searching = True
                    else:
                        searching = False

                    file.write(line)
                else:

                    if searching:
                        if 'unique' in line:
                            super_search = True
                            file.write(line)
                            block = False
                        elif super_search is True:
                            if '}' in line:
                                super_search = False
                                searching = False
                                file.write(line)
                            elif block is False:
                                if names_list[i] == list():
                                    continue
                                to_write = "\" \"".join(list(names_list[i]))
                                if to_write.strip().endswith("\"") is False:
                                    to_write = to_write + "\""
                                if to_write.strip().startswith("\"") is False:
                                    to_write = "\"" + to_write
                                file.write("\t\t\t" + to_write + "\n")
                                block = True
                                i += 1
                        else:
                            file.write(line)
                    else:
                        file.write(line)

                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')






def main():

    modpath = r"C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU"
    gamepath = r"G:\Games\steamapps\common\Hearts of Iron IV"

    check_ship_names(modpath)
    #strat_region(gamepath, modpath)
    #tech(modpath)
    #convert_oob(modpath)
    #fix_oob_calls(modpath)

if __name__ == "__main__":
    main()