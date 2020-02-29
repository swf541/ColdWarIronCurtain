from codecs import open
from os import listdir
import os

#put the paths down here (eaw is for the mod folder)
hoi4_folder = r''
eaw_folder = r''
language = 'english'
l_language = 'l_' + language + ':'
hoi4_loc = dict()

for filename in listdir(os.path.join(hoi4_folder, "localisation")):
    if language in filename:
        with  open(os.path.join(hoi4_folder, "localisation", filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('#') or line == "" or l_language == line:
                    continue
                if '#' in line.split("\"")[-1]:
                    line = "".join(line.split('#')[:-1])

                key = line.split(":")[0]
                value = line[:-1].split("\"")[1]
                hoi4_loc[key] = value

for filename in listdir(os.path.join(eaw_folder, "localisation", "replace")):
    if language in filename:
        with  open(os.path.join(eaw_folder, "localisation", "replace", filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('#') or line == "" or l_language == line:
                    continue
                if '#' in line.split("\"")[-1]:
                    line = "".join(line.split('#')[:-1])

                key = line.split(":")[0]
                value = line[:-1].split("\"")[1]
                hoi4_loc[key] = value

tot = [0, 0, 0, 0]

eaw_loc = dict()
for filename in listdir(os.path.join(eaw_folder, "localisation")):
    replace_exists = False
    if language in filename:
        file = open(os.path.join(eaw_folder, "localisation", filename), 'r', 'utf-8-sig')
        lines = file.readlines()
        file.close()
        outputfile = open(os.path.join(eaw_folder, "localisation", filename), 'w', 'utf-8-sig')
        outputfile.truncate()

        for line in lines:
            orig_line = line[:]
            line = line.strip()

            if line.startswith('#') or line == "" or l_language == line:
                outputfile.write(orig_line)
                continue
            if '#' in line.split("\"")[-1]:
                line = "".join(line.split('#')[:-1])

            key = line.split(":")[0]
            try:
                value = line[:-1].split("\"")[1]
            except IndexError:
                print(line)
                print(filename)
                exit(1)

            if key in eaw_loc:

                if value == eaw_loc[key]:
                    tot[0] += 1
                    #print("eaw identical", key)
                    outputfile.write(" #" + line + "# Identical duplicate from Eaw\n")
                else:
                    tot[1] += 1
                    #print("eaw diff", key)
                    outputfile.write(" #" + line + "# Different duplicate from Eaw\n")
            elif key in hoi4_loc:

                if value == hoi4_loc[key]:
                    outputfile.write(" #" + line + "# Identical duplicate from hoi4\n" )
                    tot[2] += 1
                    #print("hoi identical", key)
                else:
                    #print("hoi diff", key)
                    outputfile.write(" #" + line + "# moved to replace folder\n")
                    if replace_exists is False:
                        hoi4_replace_file = open(os.path.join(eaw_folder, "localisation", "replace", filename.split('l_' + language)[0] + "overrides_l_" + language + ".yml"), 'w', 'utf-8-sig')
                        hoi4_replace_file.write(l_language + "\n")
                        replace_exists = True
                    eaw_loc[key] = value
                    hoi4_replace_file.write(orig_line)
                    tot[3] += 1

            else:
                outputfile.write(orig_line)
                eaw_loc[key] = value


print(sum(tot), tot)
