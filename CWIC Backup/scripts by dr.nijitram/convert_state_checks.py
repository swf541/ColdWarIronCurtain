from codecs import open
import sys
from os import listdir
import time
import os
import re

global_start = "create_ambitions = {\n\tevery_state = {\n"
global_end = "\t}\n}"
template = "\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tOR = {\n\t\t\t\t\tis_core_of = %(tag)s\n\t\t\t\t\tis_claimed_by = %(tag)s\n%(script)s\t\t\t\t}\n\t\t\t}\n\t\t\tset_variable = { ambition@%(tag)s = 1 }\n\t\t}\n"
chyna_ones = set()

def parse_block(lines_to_parse):

    lines_to_parse = ["\t" + _ for _ in lines_to_parse]
    #print(lines_to_parse)
    tag = lines_to_parse[1].split('=')[1].strip()

    if 'is_mainland_china = yes' == lines_to_parse[3].strip():
        chyna_ones.add(tag)
        return (template % {"tag": tag, "script": ""})

    if 'FROM = {' == lines_to_parse[2].strip():
        if "OR = {" == lines_to_parse[3].strip():
            lines_to_parse = [_[1:] for _ in lines_to_parse[4:-2]]
        else:
            lines_to_parse = lines_to_parse[3:-1]
    else:
        # Path should never have to be taken with proper formatting of the source file
        lines_to_parse = lines_to_parse[2:-1]

    return (template % {"tag": tag, "script": "".join(lines_to_parse)})




def scrub_checks():
    """
    FROM:
    # AFG = Afghanistan
    AND = {
        tag = AFG
        FROM = {
            OR = {
                region = 162 #Afghanistan
                state = 442 #West of Indus
                state = 445
                state = 444
            }
        }
    }

    TO:
    # AFG = Afghanistan
    if = {
        limit = {
            OR = {
                is_core_of = AFG
                is_claimed_by = AFG
                region = 162 #Afghanistan
                state = 442 #West of Indus
                state = 445
                state = 444
            }
        }
        set_variable = { ambition@AFG = 1 }
    }

    """
    modpath = r"C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU"
    main_file = modpath + r"\common\scripted_triggers\KR_peace_conf_triggers_trimmed.txt"
    main_path = modpath + r"\common\scripted_effects"


    to_write = global_start


    with open(os.path.join(main_file), 'r', 'utf-8') as file:
        lines = file.readlines()
        level = 0

        start_no = 0
        end_no = 0
        set = True

        for lineno, line in enumerate(lines):
            if '#' in line:
                if line.strip().startswith("#") is True:
                    continue
                else:
                    line = line.split('#')[0]

            if '{' in line:
                level += line.count('{')
            if '}' in line:
                level -= line.count('}')

            if level == 3 and set:
                start_no = lineno
                set = False

            if level == 2 and start_no != 0:
                end_no = lineno
                set = True

                to_write = to_write + lines[start_no - 1] + parse_block(lines[start_no:end_no])

    to_write = to_write + "\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tis_mainland_china = yes\n\t\t\t}\n"
    for tags in chyna_ones:
        to_write = to_write + "\t\t\tset_variable = { ambition@" + tags + "= 1 }\n"
    to_write = to_write + "\t\t}\n"

    to_write = to_write + global_end

    with open(os.path.join(main_path, "testing_trigger.txt"), 'w', 'utf-8') as file:
        file.truncate()
        file.write(to_write)

if __name__ == "__main__":
    scrub_checks()