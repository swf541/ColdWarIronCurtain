from codecs import open
import sys
from os import listdir
import time
import os
import re

#TODO
#Unit leader events


def check_triggered(line_number, lines):
    if line_number == len(lines) or line_number == len(lines)-1 or line_number == len(lines)-2 :
        return True
    if '}' in lines[line_number+2] or 'days' in lines[line_number+2] or "hours" in lines[line_number+2]:
        #print("1: Found Triggered Event at line: " + line_number.__str__())
        return True
    if '}' in lines[line_number+1] or 'days' in lines[line_number+1] or "hours" in lines[line_number+1]:
        #print("1: Found Triggered Event at line: " + line_number.__str__())
        return True
    if '}' in lines[line_number] or 'days' in lines[line_number] or "hours" in lines[line_number]:
        #print("1: Found Triggered Event at line: " + line_number.__str__())
        return True
    for i in range(line_number, len(lines)):
        string = lines[i].strip()
        if string.startswith('#') is True:
            continue
        if string.startswith('}') is True or 'days' in string:
            #print("2: Found Triggered Event at line: " + i.__str__())
            return True
        elif string != "":
            #print("3: Found normal Event at line: " + i.__str__())
            return False
    return False


def focus(cpath):
    ttime = 0
    #immediate = {log = "Focus id: "+ id + "\n"}  # autolog
    for filename in listdir(os.path.join(cpath, "common", "national_focus")):
        if ".txt" in filename:
            file = open(os.path.join(cpath, "common", "national_focus", filename), 'r', 'utf-8')
            size = os.path.getsize(os.path.join(cpath, "common", "national_focus", filename))
            if size < 100:
                continue
            lines = file.readlines()
            line_number = 0
            ids = []
            idss = []
            new_focus = False
            find_coml = False
            timestart = time.time()
            shared_focus = False
            shared_focuseseses = []
            for line in lines:
                line_number += 1
                if line.strip().startswith('#'):
                    continue
                if '#' in line:
                    line = line.split('#')[0]
                if 'focus = {' in line:  # New Event
                    if 'shared_focus' in line:
                        shared_focus = True
                    new_focus = True
                    if find_coml is True:
                        find_coml = False
                        ids.pop()
                if line.strip().startswith('id') and new_focus is True:
                        new_focus = False
                        find_coml = True
                        focus_id = line.split('=')[1].strip()
                        if '#' in focus_id:
                            focus_id = focus_id.split('#')[0].strip()
                        ids.append(focus_id)
                        if shared_focus:
                            shared_focuseseses.append(focus_id)
                            shared_focus = False
                if 'completion_reward' in line and find_coml is True:
                        find_coml = False
                        idss.append(line_number)
                if 'log = "[GetDateText]:' in line:
                    if idss != [] or ids != []:
                        idss.pop()
                        ids.pop()
            time1 = time.time() - timestart
            line_number = 0
            file.close()
            outputfile = open(os.path.join(cpath, "common", "national_focus", filename), 'w', 'utf-8')
            outputfile.truncate()
            for line in lines:
                line_number += 1

                if line_number in idss:
                    whitespace = line[:-len(line.lstrip())]
                    focus_id = ids[idss.index(line_number)]
                    if focus_id in ["{", "}"]:
                        focus_id = "Error, focus name not found"
                    if '}' in line:
                        temp = line.split("{")
                        replacement_text = whitespace + temp[0].strip() + "{\n" + whitespace + "\tlog = \"[GetDateText]: [Root.GetName]: Focus " + focus_id + "\"\n" + "{".join(temp)[len(temp[0])+1:] + "\n"
                    else:
                        replacement_text = whitespace + "completion_reward = {\n" + whitespace + "\tlog = \"[GetDateText]: [Root.GetName]: Focus " + focus_id + "\"\n"
                    outputfile.write(replacement_text)
                    #print("Inserted loc at {0} in file {1}".format(line_number.__str__(), filename))
                else:
                    outputfile.write(line)
            time2 = time.time() - timestart - time1

            #print(filename + " 1: %.3f ms  2: %.3f ms" % (time1*1000, time2*1000))
            ttime += time1 + time2
    return ttime


def event(cpath):
    ttime = 0
    adding_keyword = "immediate"
    # immediate = {log = "[Root.GetName]: event "+ id + "\n"}  # autolog
    for filename in listdir(os.path.join(cpath, "events")):
        if ".txt" in filename:
            file = open(os.path.join(cpath, "events", filename), 'r', 'utf-8-sig')
            try:
                lines = file.readlines()
            except UnicodeDecodeError:
                print(filename)
                continue
            size = os.path.getsize(os.path.join(cpath, "events", filename))
            if size < 100:
                continue
            event_id = None
            line_number = 0
            triggered = False
            ids = []
            idss = []
            has_add_keyword = dict()
            timestart = time.time()
            for line in lines:
                line_number += 1
                if line.strip().startswith('#'):
                    continue
                if '#' in line:
                    line = line.split('#')[0]
                if 'country_event' in line or 'news_event' in line or 'unit_leader_event' in line or 'state_event' in line: #New Event
                    if check_triggered(line_number, lines) is False:
                        if "}" not in line or "days" not in line:
                            new_event = True
                            if event_id is not None:
                                triggered = False
                        else:
                            triggered = True
                            new_event = False
                            #print("1: Found Triggered Event at line: " + line_number.__str__())
                    else:
                        triggered = True
                        new_event = False
                if line.strip().startswith('id') and new_event is True :
                    if triggered is False:
                        new_event = False
                        event_id = line.split('=')[1].strip()
                        idss.append(event_id)
                        ids.append(line_number)
                    else:
                        triggered = False
                if line.strip().startswith(adding_keyword):
                    has_add_keyword[event_id] = line_number


            time1 = time.time() - timestart
            line_number = 0
            file.close()
            outputfile = open(os.path.join(cpath, "events", filename), 'w', 'utf-8-sig')
            outputfile.truncate()


            event_id = "THIS SHOULD NEVER SHOW UP"
            insert_in_trigger = -1
            for line in lines:
                line_number += 1
                replacement_text = line

                if line_number in ids:
                    extra = ""
                    event_id = idss[ids.index(line_number)]
                    if event_id not in has_add_keyword:
                        if '#' in line:
                            extra = " #" + line.split('#')[len(line.split('#'))-1].strip()
                        if '.' not in event_id:
                            outputfile.write(line)
                            continue
                        white_space = line[:-len(line.lstrip())]
                        replacement_text = white_space + "id = " + event_id + extra + "\n" + white_space + "immediate = { log = \"[GetDateText]: [Root.GetName]: event " + event_id + "\" }\n"
                    else:
                        insert_in_trigger = has_add_keyword[event_id]

                elif line_number == insert_in_trigger:
                    white_space = line[:-len(line.lstrip())]
                    if '#' in line:
                        extra = " #" + line.split('#')[len(line.split('#')) - 1].strip()

                    if '}' in line:
                        command = line.split("{")[1].split("}")[0].strip()
                        replacement_text = white_space + adding_keyword + " = {" + "\n" + white_space + "\t" + "log = \"[GetDateText]: [Root.GetName]: event " + event_id + "\"\n" + white_space + "\t" + command + extra + "\n" + white_space + "}\n"
                    else:
                        replacement_text = white_space + adding_keyword + " = {" + extra + "\n" + white_space + "\t" + "log = \"[GetDateText]: [Root.GetName]: event " + event_id + "\"\n"
                    #print("Inserted loc at {0} in file {1}".format(line_number.__str__(), filename))

                outputfile.write(replacement_text)


            time2 = time.time() - timestart - time1

            #print(filename + " 1: %.3f ms  2: %.3f ms" % (time1*1000, time2*1000))
            ttime += time1 + time2
    return ttime


def idea(cpath):
    ttime = 0
    timestart = time.time()
    adding_keyword = "on_add"
    has_add_keyword = dict()

    #First bit
    # 			on_add = {log = "[GetDateText]: [Root.GetName]: add idea "}
    for filename in listdir(os.path.join(cpath, "common", "ideas")):
        if ".txt" in filename and filename.startswith('_') is False:
            file = open(os.path.join(cpath, "common", "ideas", filename), 'r', 'utf-8')
            size = os.path.getsize(os.path.join(cpath, "common", "ideas", filename))
            if size < 100:
                continue
            level = 0
            line_number = 0
            ids = []
            lines = file.readlines()
            for line in lines:
                line_number += 1
                if '#' in line:
                    if line.strip().startswith("#") is True:
                        continue
                    else:
                        line = line.split('#')[0]
                re.sub(r'".+?"', '', line)
                if '= {' in line:
                    if level == 2:
                        if 'on_add = { log = ' not in lines[line_number]:
                            #print(line.split('=')[0].strip())
                            ids.append(line_number)

                if line.strip().startswith(adding_keyword):
                    has_add_keyword[idea_id] = line_number

                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

            file.close()
            line_number = 0
            outputfile = open(os.path.join(cpath, "common", "ideas", filename), 'w', 'utf-8')
            outputfile.truncate()

            idea_id = "THIS SHOULNT EVER BE SEEN"

            for line in lines:
                line_number += 1
                replacement_text = line
                if line_number in ids:
                    extra = ""
                    if '#' in line:
                        line = line.strip()
                        extra = " #" + line.split('#')[len(line.split('#'))-1].strip()
                    idea_id = line.split('=')[0].strip()
                    replacement_text = "\t\t" + idea_id + " = {" + extra + "\n\t\t\ton_add = { log = \"[GetDateText]: [Root.GetName]: add idea " + idea_id + "\"}\n"

                    #print("Inserted loc at {0} in file {1}".format(line_number.__str__(), filename))


                if line_number in list(has_add_keyword.values()):
                    white_space = line[:-len(line.lstrip())]
                    if '#' in line:
                        extra = " #" + line.split('#')[len(line.split('#')) - 1].strip()

                    if '}' in line:
                        command = line.split("{")[1].split("}")[0].strip()
                        replacement_text = white_space + adding_keyword + " = {" + "\n" + white_space + "\t" + "log = \"[GetDateText]: [Root.GetName]: add idea " + idea_id + "\"\n" + white_space + "\t" + command + extra + "\n" + white_space + "}\n"
                    else:
                        replacement_text = white_space + adding_keyword + " = {" + extra + "\n" + white_space + "\t" + "log = \"[GetDateText]: [Root.GetName]: add idea " + idea_id + "\"\n"

                outputfile.write(replacement_text)





    time1 = time.time() - timestart
    #Second Bit

    time2 = time.time() - timestart - time1
    ttime += time1 + time2
    return ttime


def decision_improved(cpath):

    timestart = time.time()

    # log = "[GetDateText] [Root.GetName]: decision (remove) name (target: [From.GetName])"

    # Thanks Yard Very Cool
    for filename in listdir(os.path.join(cpath, "common", "decisions")):

        # listdir also provides directories and this is very annoying thank you very much
        if 'categories' in filename:
            continue

        # We gottem boys
        # This check is here because sometimes smart people put other files in this directory
        if ".txt" in filename:
            # Open that sucker right up
            with open(os.path.join(cpath, "common", "decisions", filename), 'r', 'utf-8') as file:

                # Because this scripts hates empty files, we just ignore all that are below 100 bytes
                if os.path.getsize(os.path.join(cpath, "common", "decisions", filename)) < 100:
                    continue

                # Get them lines
                lines = file.readlines()

                # This is the var that indicates the bracket level
                level = 0

                # The dictionary that will hold all our stuff
                found_decisions = {}  # Numbers denote line numbers: decision_name: [complete_effect, remove_effect, timeout_effect, targeted_decision_bool]

                #Initialise the latest found to an unreachable value
                latest_found = -1

                # Loop over all lines this file to detect where the decisions are
                for line_number, line in enumerate(lines):

                    # If the line is a comment, we skip it, and if it contains a comment, strip it out
                    if '#' in line:
                        if line.strip().startswith("#") is True:
                            continue
                        else:
                            line = line.split('#')[0]

                    # Check for a ={ and the right level denoting a new decision
                    if ('= {' in line or '={' in line) and level == 1:

                        # Keep track of the latest decision found
                        latest_found = line_number
                        # Add an default reference to this decision
                        found_decisions[line_number] = [0, 0, 0, False]

                    if latest_found in found_decisions:
                        if 'complete_effect' in line:
                            found_decisions[latest_found][0] = line_number

                        elif 'remove_effect' in line:
                            found_decisions[latest_found][1] = line_number

                        elif 'timeout_effect' in line:
                            found_decisions[latest_found][2] = line_number

                        elif 'target_trigger' in line or 'targets' in line:
                            found_decisions[latest_found][3] = True


                    if '{' in line:
                        level += line.count('{')
                    if '}' in line:
                        level -= line.count('}')


            if found_decisions == {}:
                continue

            found_decisions_filtered = {}
            for key, value in found_decisions.items():
                # Check if key is even then add pair to new dictionary
                if value:
                    found_decisions_filtered[key] = value

            found_decisions = found_decisions_filtered

            id = ""
            index = [-1, -1, -1, False]

            main_line_numbers = list(found_decisions.keys())

            with open(os.path.join(cpath, "common", "decisions", filename), 'w', 'utf-8') as outputfile:
                outputfile.truncate()

                for line_number, line in enumerate(lines):

                    if line.strip().startswith('#'):
                        outputfile.write(line)
                        continue

                    replacement_text = line

                    if line_number in main_line_numbers:
                        index = found_decisions[line_number]

                        id = line.split('=')[0].strip()

                        if index[3] is True:
                            id += " target: [From.GetName]"

                    elif line_number == index[0]:
                        if '}' in line:
                            temp = line.split("{")
                            replacement_text = temp[0] + "{\n\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision " + id + "\"\n" + "{".join(temp)[len(temp[0]) + 1:] + "\n"
                        else:
                            replacement_text = "\t\tcomplete_effect = {\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision " + id + "\"\n"

                    elif line_number == index[1]:
                        if '}' in line:
                            temp = line.split("{")
                            replacement_text = temp[0] + "{\n\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision remove " + id + "\"\n" + "{".join(temp)[len(temp[0]) + 1:] + "\n"
                        else:
                            replacement_text = "\t\tremove_effect = {\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision remove " + id + "\"\n"

                    elif line_number == index[2]:
                        if '}' in line:
                            temp = line.split("{")
                            replacement_text = temp[0] + "{\n\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision timeout " + id + "\"\n" + "{".join(temp)[len(temp[0]) + 1:] + "\n"
                        else:
                            replacement_text = "\t\ttimeout_effect = {\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision timeout " + id + "\"\n"


                    outputfile.write(replacement_text)

    return time.time() - timestart

def tech(cpath):
    ttime = time.time()
    adding_keyword = "on_research_complete"
    # on_research_complete = {  log = "[GetDateText] [Root.GetName]: add tech advanced_light_spaa"}
    for filename in listdir(os.path.join(cpath, "common", "technologies")):
        if ".txt" in filename:
            file = open(os.path.join(cpath, "common", "technologies", filename), 'r', 'utf-8')
            size = os.path.getsize(os.path.join(cpath, "common", "technologies", filename))
            if size < 100:
                continue
            lines = file.readlines()
            line_number = 0
            level = 0
            ids = []
            has_add_keyword = dict()
            idea_id = None

            for line in lines:
                line_number += 1
                if '#' in line:
                    if line.strip().startswith("#") is True:
                        continue
                    else:
                        line = line.split('#')[0]

                if '= {' in line:
                    if level == 1:
                        #print(line.split('=')[0].strip())
                        ids.append(line_number)
                        idea_id = line.split('=')[0].strip()

                if line.strip().startswith(adding_keyword):
                    has_add_keyword[idea_id] = line_number

                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

            file.close()
            line_number = 0
            outputfile = open(os.path.join(cpath, "common", "technologies", filename), 'w', 'utf-8')
            outputfile.truncate()

            idea_id = "THIS SHOULNT EVER BE SEEN"


            for line in lines:
                line_number += 1
                replacement_text = line

                if line_number in ids:
                    extra = ""
                    if '#' in line:
                        extra = "#" + line.split('#')[1].strip()
                    idea_id = line.split('=')[0].strip()

                    if idea_id not in has_add_keyword:
                        replacement_text = "\t" + idea_id + " = {" + extra + "\n\t\ton_research_complete = { log = \"[GetDateText]: [Root.GetName]: add tech " + idea_id + "\"}\n"

                    #print("Inserted loc at {0} in file {1}".format(line_number.__str__(), filename))

                if line_number in list(has_add_keyword.values()):
                    white_space = line[:-len(line.lstrip())]
                    if '#' in line:
                        extra = " #" + line.split('#')[len(line.split('#')) - 1].strip()

                    if '}' in line:
                        command = line.split("{")[1].split("}")[0].strip()
                        replacement_text = white_space + adding_keyword + " = {" + "\n" + white_space + "\t" + "log = \"[GetDateText]: [Root.GetName]: add tech " + idea_id + "\"\n" + white_space + "\t" + command + extra + "\n" + white_space + "}\n"
                    else:
                        replacement_text = white_space + adding_keyword + " = {" + extra + "\n" + white_space + "\t" + "log = \"[GetDateText]: [Root.GetName]: add tech " + idea_id + "\"\n"

                outputfile.write(replacement_text)



    return time.time() - ttime

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
        ttime = 0
        ttime += event(cpath)
        ttime += focus(cpath)
        ttime += idea(cpath)
        ttime += decision_improved(cpath)
        ttime += tech(cpath)
        print("Total Time: %.3f ms" % (ttime * 1000))

if __name__ == "__main__":
    main()
