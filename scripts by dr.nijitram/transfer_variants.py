from codecs import open
from os import listdir
from os import path
import re

def main():
    mod_path = r'C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU'
    countries_folder = path.join(mod_path, 'history', 'countries')

    filenames = listdir(countries_folder)
    for filename in filenames:
        with open(path.join(countries_folder, filename), 'r', 'utf-8') as file:
            lines = file.readlines()
            level = 0
            find = False
            append_file = []
            for line_number, line in enumerate(lines):
                og_line = line
                if '#' in line:
                    if line.strip().startswith("#") is True:
                        continue
                    else:
                        stripped_line = line.split('#')[1]
                        line = line.split('#')[0]
                else:
                    stripped_line = ""


                if ' service' in stripped_line.lower() and 'focus' not in stripped_line.lower():
                    append_file = []
                    find = True
                    matches = re.findall('[A-Z]{3}', stripped_line)

                    for tag in matches:
                        if tag in filename:
                            continue
                        file_to_append = [_ for _ in filenames if tag in _][0]
                        print(line, tag)
                        append_file.append(file_to_append)

                        with open(path.join(countries_folder, file_to_append), 'a', 'utf-8') as to_append:
                            to_append.write("\nset_country_flag = " + line.split("\"")[1].split("\"")[0].replace(" ", '_').lower() + "_ship_variant\ncreate_equipment_variant = {\n")




                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

                if find:
                    for file_to_append in append_file:
                        with open(path.join(countries_folder, file_to_append), 'a', 'utf-8') as to_append:
                            if ' service' in stripped_line.lower():
                                to_append.write(line + '\n')
                            else:
                                to_append.write(og_line)
                    if level is 0:
                        find = False







main()