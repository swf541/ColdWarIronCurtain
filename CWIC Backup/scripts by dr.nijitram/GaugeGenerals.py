import sys
import time
from os import listdir
from os import path
from codecs import open
import random


def print_general(generals, to_find):
    print(to_find + ":", generals[to_find])


def get_extremes(pips, available = None):
    if available is None:
        available = ["A", "D", "P", "L"]

    remove = {"A", "D", "P", "L"} - set(available)

    keys = list(set(pips.keys()) - remove)

    values = list(pips.values())

    for key in list(remove):
        values.remove(pips[key])

    high = max(values)
    high_no = []
    low = min(values)
    low_no = []

    for key in keys:
        if pips[key] == high:
            high_no.append(key)
        elif pips[key] == low:
            low_no.append(key)

    #print("High:", high_no, "Low:", low_no)
    return high_no, low_no


def normalise_again(pips):
    reduce = 0
    if min(list(pips.values())) == 0:
        for x in pips:
            if pips[x] == 0:
                pips[x] = 1
                reduce += 1
    return reduce


def get_elegible(pips, lower, original_stats,  available = None):
    if available is None:
        available = ["A", "D", "P", "L"]

    high, low = get_extremes(pips)

    if len(high) == 4:  # If all are of the same value return all the values
        return available

    if lower is True:
        for key in pips:  # Yeet the 1's, can't ever lower em
            if pips[key] == 1:
                if key in available:
                    available.remove(key)

        high, low = get_extremes(pips, available)

        values = list(pips.values())  # Sort values to determine if the max value can be lowered
        sorted_values = values
        list.sort(sorted_values)

        if sorted_values[3] == (sorted_values[2]+2):  # Difference of two means that the highest can be lowered without losing specialisation
            for key in pips:
                if pips[key] == sorted_values[3]:
                    return [key]
        elif sorted_values[2] == (sorted_values[1]+2):
            for key in pips:
                if pips[key] == sorted_values[2]:
                    return [key]

        if len(high) == 1 and len(available) > 2 and (len(low) == 1 or len(low) == 2):  # If there are two nice central values, return those
            backup = list(set(available) - set(high) - set(low))
            for keys in original_stats:
                if original_stats[keys] - pips[keys] != 0:
                    if keys in backup:
                        backup.remove(keys)
            if len(backup) == 0:
                backup = available
            return backup

        if len(high) + len(low) == len(available):  # If all remaining values are either in high or low, return the larger
            if len(low) > len(high):
                return low
            else:
                return high

    else:
        if len(low) < 3:  # Raise the lowest values
            return low

        if len(low) == 3:
            if pips[high[0]] - pips[low[0]] == 1:
                return high
            else:
                return low

    return available  # Else just return what's left of available


def fix_by_one(pips, subtract, original_stats):
    elegible = get_elegible(pips, subtract, original_stats)
    #print("Pips before:", pips)
    #print("elegible:", elegible)
    if len(elegible) == 0:
        print(pips, subtract, elegible, original_stats)
        exit()
    random.seed()
    if subtract is True:
        pips[random.choice(elegible)] -= 1
        return 1
    else:
        pips[random.choice(elegible)] += 1
        return -1


def fix_by_fours(pips, to_add):
    if to_add > 0:
        add = 1
    else:
        add = -1

    while abs(to_add) > 3:

        for key in pips:
            pips[key] += add
        to_add += -add * 4

        if add == -1:
            to_add += -normalise_again(pips)

    return to_add


def not_blocked(pips):
    values = list(pips.values())  # Sort values to determine if the max value can be lowered
    sorted_values = values
    list.sort(sorted_values)
    if sorted_values[3] == (sorted_values[2] + 2):  # Difference of two means that the highest can be lowered without losing specialisation
        return False
    else:
        return True


def normalise_stats(generals, normalise):

    rank, skill, A, D, P, L, total, tag = generals[normalise]


    # rank, skill, A, D, P, L, total, tag = 'a', 2, 2, 1, 1, 1, 6, 'BAT'
    # rank, skill, A, D, P, L, total, tag = 'a', 3, 4, 4, 2, 1, 11, 'BAT'

    return_string = normalise + " from skill {}:{}/{}/{}/{} to ".format(skill, A, D, P, L)
    pips = {"A": A, "D": D, "P": P, "L": L}
    original_stats = pips.copy()
    aim = skill * 3 + 1

    to_add = aim - total

    if to_add < 0:
        #print("Removing", -to_add)
        lower = True
    else:
        #print("Adding", to_add)
        lower = False

    if to_add != 0:
        if skill == 1:
            for key in pips.keys():
                pips[key] = 1
        else:
            if abs(to_add) > 3 and not_blocked(pips) is True:
                to_add = fix_by_fours(pips, to_add)
            while to_add != 0:
                to_add += fix_by_one(pips, lower, original_stats)

    generals[normalise] = rank, skill, pips["A"], pips["D"], pips["P"], pips["L"], sum(list(pips.values())), tag
    return_string2 = "{}/{}/{}/{}".format(pips["A"], pips["D"], pips["P"], pips["L"])

    return return_string + return_string2


def print_stats(generals, max_sum_gen, max_tag, max_tag_no, total_generals, ops, min_gen, max_gen):
    print("Max Stat:", max_sum_gen, generals[max_sum_gen])
    print("Most OP nations:", max_tag + ",", max_tag_no)
    print("Total Generals:", total_generals)

    for x in range(-6, 7):
        if x == -6:
            print("Underpowered by 6 or more:", ops[x])
        elif x == 0:
            print("Perfection:", ops[x])
        elif x == 6:
            print("Overpowered by 6 or more:", ops[x])
        elif x < 0:
            print("Underpowered by " + str(abs(x)) + ":", ops[x])
        elif x > 0:
            print("Overpowered by " + str(abs(x)) + ":", ops[x])

    print("Too OP:", sum(ops[1:7]))
    print("Most OP:")
    for name in max_gen.split(','):
        print_general(generals, name.strip())
    print("Most UP:")
    for name in min_gen.split(','):
        print_general(generals, name.strip())


def main():
    cpath = sys.argv[1]
    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string

    cpath = path.join(cpath, "history", "countries")

    ttime = time.time()

    total_generals = 0
    generals = {}  # name : (G/FM/N, skill, A, D, P, L, SUM)
    tags = {}
    for filenames in listdir(cpath):
        with open(path.join(cpath, filenames),'r', 'utf-8-sig') as file:
            lines = file.readlines()
            current_general = ""
            searching = False
            skill = 999
            attack = 999
            defense = 999
            planning = 999
            logistics = 999
            level = 0
            tag = "REEEEEEEEE"
            g_or_fm = 'REEEEEEEEEEEE'
            for x in range(0, len(lines)):
                line = lines[x].strip()
                if '#' in line:
                    line = line.split('#')[0].strip()
                    if line.strip().startswith('#'):
                        continue
                if ('field_marshal' in line or 'corps_commander' in line or 'create_navy_leader' in line) and '{' in line and level == 0:
                    if 'field_marshal' in line:
                        g_or_fm = 'FM'
                    elif 'corps_commander' in line:
                        g_or_fm = 'G'
                    else:
                        g_or_fm = 'N'
                    try:
                        current_general = lines[x+1].split("\"")[1]
                    except IndexError:
                        print(filenames, x+1)
                        print(lines[x+1])
                    tag = filenames[0:3]
                    tags[tag] = 0
                    total_generals += 1
                    searching = True
                    #print(current_general)

                if '=' in line and searching is True :
                    if line.split('=')[0].strip() == "skill":
                        skill = int(line.split('=')[1])

                if 'attack_skill' in line and searching is True:
                    attack = int(line.split('=')[1])

                if 'defense_skill' in line and searching is True:
                    defense = int(line.split('=')[1])

                if 'planning_skill' in line and searching is True:
                    planning = int(line.split('=')[1])
                elif 'maneuvering_skill' in line and searching is True:
                    planning = int(line.split('=')[1])

                if 'logistics_skill' in line and searching is True:
                    logistics = int(line.split('=')[1])
                elif 'coordination_skill' in line and searching is True:
                    logistics = int(line.split('=')[1])

                if '}' in line and searching is True and level == 1 and 'trait' not in line:
                    searching = False
                    generals[filenames + current_general] = (g_or_fm, skill, attack, defense, planning, logistics, attack+defense+planning+logistics, tag)
                    #print(current_general)
                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')
                last_line = line



    file.close()
    ops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    max_sum = 0
    max_gen = ""
    min_sum = 0
    min_gen = ""

    max_sum2 = 0
    max_sum_gen = ""
    output_file = open("generals.txt", 'w', 'utf-8-sig')

    per_level = 3
    starting = 1

    fixed = 0
    fix = True

    for general in generals:
            rank, skill, A, D, P, L, total, tag = generals[general]
            target = skill * per_level + starting
            deviance = total-target
            if abs(deviance) > 0:
                fixed += 1
                output_file.write(general + ": " + str(generals[general]) + "\n")
                if fix or 'Mustafa Kemal' in general:
                    normalise_stats(generals, general)
                tags[tag] += 1

            ops[sorted((-6, deviance, 6))[1]] += 1

            if deviance > max_sum:
                max_sum = deviance
                max_gen = general
            elif deviance == max_sum:
                max_gen += ", " + general

            if total > max_sum2:
                max_sum2 = total
                max_sum_gen = general
            elif deviance == max_sum2:
                max_sum_gen += ", " + general

            if deviance < min_sum:
                min_sum = deviance
                min_gen = general
            elif deviance == min_sum:
                min_gen += ", " + general


    max_tag_no = 0
    max_tag = ""

    for tag in tags:
        if tags[tag] > max_tag_no:
            max_tag = tag
            max_tag_no = tags[tag]
        elif tags[tag] == max_tag_no:
            max_tag += ', ' + tag

    errors = 0
    for general in generals:
        rank, skill, A, D, P, L, total, tag = generals[general]
        target = skill * 3 + 1
        deviance = total-target
        if abs(deviance) > 0 and fix:
            print(general, generals[general])
            errors += 1
            fixed -= 1

    print("Total generals checked:", str(total_generals) + " with " + str(errors) + " errors and " + str(fixed) + " fixed")
    if fix is False:
        print_stats(generals, max_sum_gen, max_tag, max_tag_no, total_generals, ops, min_gen, max_gen)

    if errors != 0 and fix:
        exit("There are still broken generals, aborting")


    for filenames in listdir(cpath):

        file = open(path.join(cpath, filenames), 'r', 'utf-8-sig')
        lines = file.readlines()
        file.close()

        file = open(path.join(cpath, filenames), 'w', 'utf-8-sig')
        file.truncate()

        current_general = ""
        searching = False
        for x in range(0, len(lines)):
            comment = ""
            line = lines[x]
            if '#' in line:
                comment = "#".join(line.split('#')[1:])
                line = line.split('#')[0]
                comment = "#" + comment
            if ('field_marshal' in line or 'corps_commander' in line or 'create_navy_leader' in line) and '{' in line and level == 0:
                if 'field_marshal' in line:
                    g_or_fm = 'FM'
                elif 'corps_commander' in line:
                    g_or_fm = 'G'
                else:
                    g_or_fm = 'N'

                current_general = lines[x + 1].split("\"")[1]

                rank, skill, A, D, P, L, total, tag = generals[filenames + current_general]

                searching = True
                # print(current_general)
            if '=' in line and searching is True and line.split('=')[0].strip() == "skill":
                file.write("\tskill = " + str(skill) + comment + "\n")
            elif 'attack_skill' in line and searching is True:
                file.write("\tattack_skill = " + str(A) + comment + "\n")
            elif 'defense_skill' in line and searching is True:
                file.write("\tdefense_skill = " + str(D) + comment + "\n")
            elif 'planning_skill' in line and searching is True:
                file.write("\tplanning_skill = " + str(P) + comment + "\n")
            elif 'maneuvering_skill' in line and searching is True:
                file.write("\tmaneuvering_skill = " + str(P) + comment + "\n")
            elif 'logistics_skill' in line and searching is True:
                file.write("\tlogistics_skill = " + str(L) + comment + "\n")
            elif 'coordination_skill' in line and searching is True:
                file.write("\tcoordination_skill = " + str(L) + comment + "\n")
            elif '}' in line and searching is True and level == 1 and 'trait' not in line:
                searching = False
                file.write(line + comment)
            else:
                file.write(line + comment)
            if '{' in line:
                level += line.count('{')
            if '}' in line:
                level -= line.count('}')

        file.close()






    print("Total Time: %.3f ms" % ((time.time() - ttime) * 1000))

if __name__ == "__main__":
    main()