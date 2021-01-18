#!/usr/bin/env python3

import os, sys, yaml, json

USAGE = f"""
ERROR: Missing output directory.

USAGE: {sys.argv[0]} <output_directory>
"""

INPUT_DIRECTORIES = ['capabilities', 'misc']

def check_arguments():
    if len(sys.argv) != 2:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

def scan(directory):
    files = []

    with os.scandir(directory) as it:
        for entry in it:
            if entry.name.endswith('.yml') and entry.is_file():
                files.append(entry.path)

    return files

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def create_output_path(input_file_path):
    (path, input_filename) = os.path.split(input_file_path)

    output_file_path = os.path.join(sys.argv[1], path)
    os.makedirs(output_file_path, mode=0o775, exist_ok=True)

    output_filename = input_filename.replace('.yml', '.json')
    return os.path.join(output_file_path, output_filename)

def write_output_file(contents, path):
    with open(path, 'w') as file:
        json.dump(contents, fp=file, indent=4)

check_arguments()

yaml_files = []

for d in INPUT_DIRECTORIES:
    for yaml_file in scan(d):
        yaml_files.append(yaml_file)

for f in yaml_files:
    contents = read_input_file(f)
    output_path = create_output_path(f)
    write_output_file(contents, output_path)
