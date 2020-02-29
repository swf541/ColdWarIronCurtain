from codecs import open
import sys

def build_event(event_id, mode, options, filename):
    print("Event:" + event_id + " with mode " + mode.__str__() + " with " + len(options).__str__() + " options")
    if mode == 1 or mode == 2:
        filename.write(" " + event_id + ".t:0\"\"\n")
    if mode == 2 or mode == 3:
        filename.write(" " + event_id + ".d:0\"\"\n")
    for strings in options:
        filename.write(" " + event_id + "." + strings + ":0\"\"\n")

def check_triggered(line_number, lines):
    if line_number == len(lines) or line_number == len(lines)-1 or line_number == len(lines)-2 :
        return True
    if '}' in lines[line_number+2] or 'days' in lines[line_number+2]:
        #print("1: Found Triggered Event at line: " + line_number.__str__())
        return True
    if '}' in lines[line_number+1] or 'days' in lines[line_number+1]:
        #print("1: Found Triggered Event at line: " + line_number.__str__())
        return True
    if '}' in lines[line_number] or 'days' in lines[line_number]:
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


def main():

    file_paths = sys.argv[1:]
    filenames = []
    for p in file_paths:
        filenames.append(p)

    for filename in filenames:
        if ".txt" in filename:
            counter = 0
            temp_string = filename.split('\\')[len(filename.split('\\')) - 1].split('.')[0]
            print("Working on " + temp_string)
            temp_string = temp_string + "_loc.yml"
            output_file = open(temp_string, 'w', 'utf-8-sig')
            output_file.write("l_english: \n\n")

            file = open(filename, 'r', 'ansi')
            lines = file.readlines()
            event_id = None
            options = []
            line_number = 0
            triggered = False
            for line in lines:
                line_number += 1
                if 'country_event' in line: #New Event
                    if check_triggered(line_number, lines) is False:
                        new_event = True
                        if event_id is not None:
                            build_event(event_id, mode, options, output_file)
                        mode = 0
                        options = []
                        triggered = False
                    else:
                        triggered = True
                if 'id' in line and new_event is True:
                    if triggered is False:
                        new_event = False
                        event_id = line.split('=')[1].strip()
                    else:
                        triggered = False
                if 'title' in line:
                    mode = 1
                if 'desc' in line:
                    if mode == 1:
                        mode = 2
                    else:
                        mode = 3
                if 'name' in line:
                    options.append(line.split('.')[len(line.split('.'))-1].strip())
            build_event(event_id, mode, options, output_file)
        else:
            temp_string = filename.split('\\')[len(filename.split('\\')) - 1]
            print("Error: " + temp_string + " is not a event file")



if __name__ == "__main__":
    main()