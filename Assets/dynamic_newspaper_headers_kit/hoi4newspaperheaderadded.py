#!/usr/bin/python
import argparse
import os
import sys
import re
import collections
import glob

#############################
###
### HoI 4 News Event Title Header Adder by Yard1, originally for Equestria at War mod
### Written in Python 3.7
###
### Copyright (c) 2018 Antoni Baum (Yard1)
### Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
### The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
### usage: hoi4newspaperheaderadded.py [-h] [--scripted_loc scripted_loc] mod_path
### 
### Given a mod folder, add a scripted localisation call to every news event title
### (including triggered titles).
### 
### positional arguments:
###   mod_path              Path to the root mod folder
### 
### optional arguments:
###   -h, --help            show this help message and exit
###   --scripted_loc scripted_loc
###                         The full string (including brackets) to prefix
###                         localisation values with (Default:
###                         [Root.GetNewspaperHeader])
### 
#############################

def readable_dir(prospective_dir):
  if not os.path.isdir(prospective_dir):
    raise Exception("readable_dir:{0} is not a valid path".format(prospective_dir))
  if os.access(prospective_dir, os.R_OK):
    return prospective_dir
  else:
    raise Exception("readable_dir:{0} is not a readable dir".format(prospective_dir))

#############################

def read_event_file(name, loc_set):
    print("Reading file " + name + "...")
    lines = []
    try:
        with open(name, "r") as f:
            lines = f.read().splitlines()
    except:
        try:
            with open(name, "r", encoding='utf-8') as f:
                lines = f.read().splitlines()
        except:
            try:
                with open(name, "r", encoding='utf-8-sig') as f:
                    lines = f.read().splitlines()
            except:
                print("Could not read file " + name + "!")

    open_blocks = 0
    is_in_news_event = False
    is_in_title = False
    for line in lines:
        line = re.sub(r'#.*?$', "", line)
        if open_blocks == 0 and "news_event" in line:
            is_in_news_event = True
        if is_in_news_event:
            match = re.search(r'^\s*title\s*=\s*([^\{]+?)(\s|$)', line)
            if match:
                loc_set.add(match.group(1).strip())
            else:
                match = re.search(r'^\s*title\s*=\s*{', line)
                if match:
                    is_in_title = True
            if is_in_title:
                match = re.search(r'^\s*text\s*=\s*([^\{]+?)\s*($|\})', line)
                if match:
                    loc_set.add(match.group(1).strip())
        open_blocks += line.count('{')
        open_blocks -= line.count('}')
        if open_blocks == 1:
            is_in_title = False
        if is_in_news_event and open_blocks == 0:
            is_in_news_event = False

    print("File " + name + " read successfully!")
    return

def read_loc_file(name, loc_set, scripted_loc_re, scripted_loc):
    print("Reading file " + name + "...")
    lines = []
    try:
        with open(name, "r", encoding='utf-8-sig') as f:
            lines = f.read().splitlines()
    except:
        print("Could not read file " + name + "!")
    print("File " + name + " read successfully!")
    new_lines = []
    has_changed = False
    for line in lines:
        match = re.search(r'^\s*?([^#\s]*?):[0-9]+', line)
        if match:
            loc_key = match.group(1).strip()
            if loc_key in loc_set:
                line = scripted_loc_re.sub("\\1\\2" + scripted_loc, line)
                has_changed = True
        new_lines.append(line)
    if has_changed:
        with open(name, "w", encoding="utf-8-sig") as f:
            f.writelines(str(line) + "\n" for line in new_lines)
        print("File " + name + " modified successfully!")
    return
###################################################################
parser = argparse.ArgumentParser(description='Given a mod folder, add a scripted localisation call to every news event title (including triggered titles).')
parser.add_argument('mod_path', metavar='mod_path',
                    help='Path to the root mod folder')
parser.add_argument( '--scripted_loc', metavar='scripted_loc', default="goals_shine.gfx", required=False,
                    help='The full string (including brackets) to prefix localisation values with (Default: [Root.GetNewspaperHeader])')

args = parser.parse_args()

events_path = os.path.join(args.mod_path, 'events')
loc_path = os.path.join(args.mod_path, 'localisation')

try:
    dir = readable_dir(events_path)
except:
    print("{0} is not a directory or does not exist." % events_path)

try:
    dir = readable_dir(loc_path)
except:
    print("{0} is not a directory or does not exist." % loc_path)

loc_set = set()

for file in glob.glob(os.path.join(events_path, '*.txt')):
    read_event_file(file, loc_set)

scripted_loc = args.scripted_loc.strip()
scripted_loc_re_string = r'\s*?([^\s]*?:[0-9]+\s*)(\")(?!' + re.escape(scripted_loc) + r')'
scripted_loc_re = re.compile(scripted_loc_re_string, re.IGNORECASE)

for file in glob.glob(os.path.join(loc_path, '*.yml'), recursive=True):
    read_loc_file(file, loc_set, scripted_loc_re, scripted_loc)
