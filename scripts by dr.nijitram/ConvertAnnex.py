from codecs import open
import sys


def grab_bad(event_no, lines):
    flag = False
    line_number = 0
    flag3 = 0
    bad_stuff = ""
    prev_line = ""
    level = 1
    #print(event_no)
    for line in lines:
        line_number += 1
        if '}' in line and flag:
            level -= line.count('}')
            first_number = False
        if '{' in line and flag:
            level += line.count('{')
        if level == 0:
            flag3 = 0
            break
        if event_no in line:
            if line.split('.')[1].strip() == event_no.split('.')[1].strip():
                flag = True
        if flag:
            if '#' in line:
                if line.strip().startswith('#') is True:
                    continue
                else:
                    line = line.split('#')[0].strip()
            if 'factor = 0' in line and 'modifier' not in prev_line and 'modifier' not in line:
                if 'ai_chance' in line:
                    if line.split('=')[2].split('}')[0].strip() == "0":
                        flag3 = line_number
                        #print("found " + line_number.__str__())
                        break
                else:
                    if line.split('=')[1].strip() == "0":
                        flag3 = line_number
                        #print("found " + line_number.__str__())
                        break
        prev_line = line

    first_number = True
    level = 2
    while True:
        if flag3 == 0:
            break
        if 'factor = 0' and '}' in lines[flag3-1]:
            first_number = False
            #level -= 1
        line = lines[flag3]
        flag3 += 1
        if line.strip() is not "" and first_number is False:
            bad_stuff += line.strip() + ","
        if '}' in line:
            level -= line.count('}')
            first_number = False
        if '{' in line:
            level += line.count('{')
        if level == 0:
            break
        if 'option' in line:
            break

    bad_stuff = bad_stuff[:len(bad_stuff)-3]

    if 'option' in bad_stuff:
        bad_stuff = bad_stuff[:len(bad_stuff)- len(bad_stuff.split(',')[len(bad_stuff.split(','))-1])-3]
    if bad_stuff.strip() == "" or flag3 == 0:
        bad_stuff = "country_event = { " + event_no + " }"
    if 'trigger' in bad_stuff:
        bad_stuff = bad_stuff[len(bad_stuff.split('}')[0])+4:]
    #print(bad_stuff)
    return bad_stuff


def finddup(array, string):
    if string in array:
        return True
    else:
        return False


def fill_activation(dec_file, start_no, lines):
    level = 0
    flag = True
    while True:
        line = lines[start_no-1].strip()

        if '}' in line and flag:
            level -= line.count('}')
        if '{' in line and flag:
            level += line.count('{')
        white = "\t"*(3+level)

        start_no += 1
        if level == 0:
            if flag:
                flag = False
            else:
                break
        dec_file.write(white + line + "\n")


def get_loc(base_lines, id):
    for line in base_lines:
        if "annex." + id.__str__() + ".t:0" in line:
            return line.split(':')[1].strip()
    return  "0 \"War with Australasia\""


def get_desc(base_lines, id):
    for line in base_lines:
        if "annex." + id.__str__() + ".d:0" in line:
            return line.split(':')[1].strip()
    return  "0 \"It seems we have no choice but to face down our former colony. We are now at war with [AST.GetNameDef], and we will not rest until the islands are back in British hands.\""

def main():
    cpath = sys.argv[1]
    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string
    annex_event_file = open(cpath + "\\events\\KR_Annexations.txt", "r", "utf-8-sig")
    annex_on_action_file = open("C:\\Users\\Martijn\\Desktop\\KR_on_actions_annexations.txt", "r", "utf-8")
    lines_event = annex_event_file.readlines()
    #I need three things:
    #Negative effects from event file
    #event Triggers from on action file
    #trigger states from action files
    line_number = 0
    lines_on = annex_on_action_file.readlines()

    start_no = []
    end_no = []
    states = ""
    states_arr = []
    event_trigger = ""
    event_trigger_arr = []
    bad_stuff = ""
    bad_stuff_arr = []
    id_event = []
    flag = ""
    flag_arr = []
    counter = 0
    loc_arr = []
    found = False

    for line in lines_on:
        line_number += 1
        if line.strip().startswith('#') is False:
            if 'ROOT = {' in line:
                start_no.append(line_number)
                #print("Got ROOT for " + lines_on[line_number-3].split('#')[1].strip() + ", " + start_no.index(line_number).__str__())
            if 'owns_state' in line:
                states += line.split('#')[0].strip() + ","
                #print(line.split('#')[0].strip())
            if 'id = annex' in line:
                id_event = line.split('.')[1].split('}')[0].strip()
                #print('id = annex.' + id_event)
                event_trigger += id_event + ","
                if id_event is not "0":
                    bad_stuff = grab_bad('id = annex.' + id_event, lines_event)
            if 'set_country_flag' in line or 'clr_country_flag' in line:
                flag += line.strip() + ","
            if 'IF' in line:
                if '#' in line:
                    loc_arr.append(line.split('#')[1])
                else:
                    loc_arr.append("You Shouldnt see this, and if you do, blame nijato")
                if found is False:
                    found = True
                else:
                    end_no.append(line_number - 1)
                    states_arr.append(states[:len(states)-1])
                    event_trigger_arr.append(event_trigger[:len(event_trigger)-1])
                    if '0,231' in event_trigger[:len(event_trigger)-1]:
                        flag = "set_country_flag = SIC_NORTH_ITALY_CONQ,"
                    flag_arr.append(flag[:len(flag)-1])
                    bad_stuff_arr.append(bad_stuff)
                    #print((counter+1).__str__() + ": " + start_no[counter].__str__() + ": " + end_no[counter].__str__() + ": " + states[:len(states)-1] + ": " + event_trigger[:len(event_trigger)-1] + ": " + bad_stuff_arr[counter] + ": " + flag_arr[counter])
                    states = ""
                    event_trigger = ""
                    flag = ""
                    counter += 1

    end_no.append(line_number - 1)
    states_arr.append(states[:len(states) - 1])
    event_trigger_arr.append(event_trigger[:len(event_trigger) - 1])
    if '0,231' in event_trigger[:len(event_trigger) - 1]:
        flag = "set_country_flag = SIC_NORTH_ITALY_CONQ,"
    flag_arr.append(flag[:len(flag) - 1])
    bad_stuff_arr.append(bad_stuff)
    #print((counter + 1).__str__() + ": " + start_no[counter].__str__() + ": " + end_no[counter].__str__() + ": " + states[:len(states) - 1] + ": " + event_trigger[:len( event_trigger) - 1] + ": " +bad_stuff_arr[counter] + ": " + flag_arr[counter])
    dec_path = cpath + "\\common\\decisions\\"
    dec_file = open(dec_path + "KR_Annexation_decisions.txt", "w", "ansi")
    dec_file.truncate()
    #category is KR_Annexations

    dec_name_arr = []

    dec_file.write("political_actions = {\n")
    for x in range(0, counter):
        dec_file.write("    annexation_")
        if ',' in flag_arr[x]:
            temp_list = flag_arr[x].split(',')
            for flags in temp_list:
                if 'CONQ' in flags:
                    temp = flags
                    break
        else:
            temp = flag_arr[x]
        if '=' in temp:
            temp = temp.split('=')[1].strip()
        if finddup(dec_name_arr, "annexation_" + temp):
            if finddup(dec_name_arr, "annexation_" + temp + "2"):
                temp += '3'
            else:
                temp += "2"
        dec_name_arr.append("annexation_" + temp)
        dec_file.write(temp + " = {\n")
        dec_file.write("        icon = generic_decision\n")
        dec_file.write("        allowed = { always = yes }\n")
        dec_file.write("        activation = {\n")
        fill_activation(dec_file, start_no[x], lines_on)
        dec_file.write("        }\n")
        dec_file.write("        selectable_mission = yes\n")
        dec_file.write("        days_mission_timeout = 60\n")
        dec_file.write("        is_good = no\n")
        dec_file.write("        fire_only_once = no\n")
        dec_file.write("        cancel_trigger = {\n")
        dec_file.write("            NOT = {\n")
        #NOT = {owns_state =  # All key states}
        states_list = states_arr[x].split(',')
        for states in states_list:
            dec_file.write("                " + states + "\n")
        dec_file.write("            }\n")
        dec_file.write("        }\n")
        dec_file.write("        complete_effect = {\n")
        dec_file.write("            log = \"[GetDateText]: [Root.GetName]: Decision annexation_" + temp + "\"\n")
        trigger_list = event_trigger_arr[x].split(',')
        if 'Fate of Australasia - specific to Entente' in loc_arr[x]:
            dec_file.write("            country_event = austral.173\n") #bloody exception
        else:
            for triggers in trigger_list:
                dec_file.write("            country_event = annex." + triggers + "\n")
        dec_file.write("        }\n")
        dec_file.write("        timeout_effect = {\n")
        dec_file.write("            log = \"[GetDateText]: [Root.GetName]: Decision timeout annexation_" + temp + "\"\n")
        trigger_list = bad_stuff_arr[x].split(',')
        level = 0
        for triggers in trigger_list:
            if '}' in triggers and flag:
                level -= triggers.count('}')
            if '{' in triggers and flag:
                level += triggers.count('{')
            white = "\t" * (3 + level)
            dec_file.write(white + triggers + "\n")
        dec_file.write("        }\n")
        dec_file.write("        ai_will_do = {\n")
        dec_file.write("            factor = 100\n")
        dec_file.write("        }\n")
        dec_file.write("    }\n")
    dec_file.write("}\n")

    base_loc = open(cpath + "\\localisation\\KR_Annexations_l_english.yml", 'r', 'utf-8-sig')
    base_lines = base_loc.readlines()
    loc_file = open(cpath + "\\localisation\\KR_Annexation_Decisions_l_english.yml", 'w', 'utf-8-sig')
    loc_file.write("l_english: \n")
    loc_thing = ""
    for x in range(0, counter):
        trigger_list = event_trigger_arr[x].split(',')
        if trigger_list[0] is not "0":
            y = trigger_list[0]
        else:
            y = trigger_list[1]
        loc_thing = get_loc(base_lines, y)
        desc_thing = get_desc(base_lines, y)
        loc_file.write("" + dec_name_arr[x] + ":" + loc_thing + "\n")
        loc_file.write("" + dec_name_arr[x] + "_desc:" + desc_thing + "\n")


if __name__ == "__main__":
    main()
