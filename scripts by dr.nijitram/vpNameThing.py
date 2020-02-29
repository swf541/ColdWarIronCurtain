import sys
import os
from codecs import open

def main():
    cpath = sys.argv[1]
    filename = sys.argv[2]
    file = open(os.path.join(cpath, filename), 'r', 'utf-8')
    newfile = open(os.path.join(cpath, 'vp_output.txt'), 'w+', 'utf-8')
    for line in file:
        if "VICTORY_POINTS_" in line and "TOOLTIP" not in line:
            newline = line.split("_POINTS_")[1]
            final = newline.split(':')
            final[1] = final[1].split('"')[1]
            output = "set_province_name = {\n    id = " + final[0] + "\n    name = \"" + final[1] + "\"\n}"
            print(output)
            newfile.write(output)

if __name__ == "__main__":
    main()