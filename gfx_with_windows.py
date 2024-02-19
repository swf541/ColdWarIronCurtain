import os
import tkinter as tk
from tkinter import filedialog

# Function to open a folder dialog and return the selected folder path
def get_folder_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select the event_pictures folder")
    return folder_path

# Function to sanitize folder names (replace spaces with underscores)
def sanitize_folder_name(folder_name):
    return folder_name.replace(" ", "_")

# Ask the user for the folder path using the new function
folder_path = get_folder_path()

# Ensure the path is valid
if not os.path.exists(folder_path):
    print("Invalid path. Please provide a valid folder path.")
    exit()

# Ask the user if each first layer of subfolders should be its own file
create_individual_files = input("Do you want each first layer of subfolders to be its own file? (yes/no): ").lower()

# Ask the user if a prefix should be added to the output file names
add_prefix = input("Do you want to add a prefix to the output file names? (yes/no): ").lower()

# Get the directory of the Python script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Find the index of "gfx" in the path
gfx_index = folder_path.lower().find("gfx")

# Initialize variables for output file information
output_file_prefix = input("Enter the prefix for the output files: ")
output_file_name = f"{output_file_prefix}.gfx"
output_file_path = os.path.join(script_directory, output_file_name)

# Initialize variables for shine output file information
shine_output_file_name = f"{output_file_prefix}_shine.gfx"
shine_output_file_path = os.path.join(script_directory, shine_output_file_name)

# Initialize variables for goals output file information
goals_output_file_name = f"{output_file_prefix}_goals.gfx"
goals_output_file_path = os.path.join(script_directory, goals_output_file_name)

# Open the main output file in write mode
with open(output_file_path, "w") as output_file:
    output_file.write("spriteTypes = {\n")

    # Loop through the files in the selected folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".png", ".dds")):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path).replace(os.path.sep, "/")

                # Get the subfolder dynamically
                subfolder = os.path.dirname(relative_path)
                subfolder = os.path.normpath(subfolder).replace(os.path.sep, "/")

                # Sanitize the subfolder name (replace spaces with underscores)
                sanitized_subfolder = sanitize_folder_name(subfolder)

                # Extract the path starting from "gfx"
                gfx_subpath = folder_path[gfx_index:]
                gfx_subpath = os.path.normpath(gfx_subpath).replace(os.path.sep, "/")

                sprite_name = "GFX_" + file.split(".")[0]

                # Check if there is a subfolder
                # ... (previous code remains unchanged)

                if create_individual_files == "yes" and subfolder != '.':
                    # Sanitize the subfolder name for the output file
                    sanitized_subfolder = sanitize_folder_name(subfolder)

                    # Create a separate output file for each first layer of subfolders
                    subfolder_output_file_name = f"{output_file_prefix}_{sanitized_subfolder}.gfx"
                    subfolder_output_file_path = os.path.join(script_directory, subfolder_output_file_name)
                    os.makedirs(os.path.dirname(subfolder_output_file_path), exist_ok=True)  # Create the directory if it doesn't exist

                    # Check if the spriteTypes definition has been written for this subfolder
                    if not os.path.exists(subfolder_output_file_path):
                        with open(subfolder_output_file_path, "a") as subfolder_output_file:
                            # Write spriteTypes definition only once for each subfolder
                            subfolder_output_file.write('spriteTypes = {\n')

                            # Loop through files in the subfolder and add spriteType dictionaries to the output file
                            for file in files:
                                texture_file = f'{gfx_subpath}/{subfolder}/{file}'
                                sprite_name = f'GFX_{file.split(".")[0]}'  # Unique name based on the file
                                sprite_type = (
                                    f'\tspriteType = {{\n\t\tname = "{sprite_name}"\n\t\ttexturefile = "{texture_file}"\n\t}}\n'
                                )
                                subfolder_output_file.write(sprite_type)

                            # Close spriteTypes definition
                            subfolder_output_file.write('\n}\n\n')

                # ... (remaining code remains unchanged)


                else:
                    # Add the sprite information to the main output file
                    texture_file = f'{gfx_subpath}/{subfolder}/{file}' if subfolder != '.' else f'{gfx_subpath}/{file}'
                    sprite_name = f'GFX_{file.split(".")[0]}'  # Unique name based on the file
                    output_file.write(f'\tspriteType = {{\n\t\tname = "{sprite_name}"\n\t\ttexturefile = "{texture_file}"\n\t}},\n')


    output_file.write("}\n")

print(f"Event pictures information saved to {output_file_path}")

# Check if the "goals" subfolder exists for generating shine and goals files
goals_subfolder_path = os.path.join(folder_path, "goals")
if os.path.exists(goals_subfolder_path):
    # Open the shine output file in write mode
    with open(shine_output_file_path, "w") as shine_output_file:
        shine_output_file.write("spriteTypes = {\n")

        # Open the goals output file in write mode
        with open(goals_output_file_path, "w") as goals_output_file:
            goals_output_file.write("spriteTypes = {\n")

            # Loop through the files in the "goals" subfolder for shine and goals generation
            for root, dirs, files in os.walk(goals_subfolder_path):
                for file in files:
                    if file.lower().endswith((".png", ".dds")):
                        sprite_name = "GFX_" + file.split(".")[0]
                        texture_file = f'"{gfx_subpath}/{os.path.relpath(os.path.join(root, file), folder_path).replace(os.path.sep, "/")}"'

                        # Write shine information
                        shine_output_file.write(f'\tSpriteType = {{\n\t\tname = "{sprite_name}_shine"\n\t\ttexturefile = {texture_file}\n\t\teffectFile = "gfx/FX/buttonstate.lua"\n')
                        shine_output_file.write("\t\tanimation = {\n")
                        shine_output_file.write(f'\t\t\tanimationmaskfile = {texture_file}\n')  # Use the same texture_file for animationmaskfile
                        shine_output_file.write("\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\"\n")
                        shine_output_file.write("\t\t\tanimationrotation = -90.0\n")
                        shine_output_file.write("\t\t\tanimationlooping = no\n")
                        shine_output_file.write("\t\t\tanimationtime = 0.75\n")
                        shine_output_file.write("\t\t\tanimationdelay = 0\n")
                        shine_output_file.write("\t\t\tanimationblendmode = \"add\"\n")
                        shine_output_file.write("\t\t\tanimationtype = \"scrolling\"\n")
                        shine_output_file.write("\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }\n")
                        shine_output_file.write("\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }\n")
                        shine_output_file.write("\t\t}\n")  # Add a comma here
                        shine_output_file.write("\t\tanimation = {\n")
                        shine_output_file.write(f'\t\t\tanimationmaskfile = {texture_file}\n')  # Use the same texture_file for animationmaskfile
                        shine_output_file.write("\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\"\n")
                        shine_output_file.write("\t\t\tanimationrotation = 90.0\n")
                        shine_output_file.write("\t\t\tanimationlooping = no\n")
                        shine_output_file.write("\t\t\tanimationtime = 0.75\n")
                        shine_output_file.write("\t\t\tanimationdelay = 0\n")
                        shine_output_file.write("\t\t\tanimationblendmode = \"add\"\n")
                        shine_output_file.write("\t\t\tanimationtype = \"scrolling\"\n")
                        shine_output_file.write("\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }\n")
                        shine_output_file.write("\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }\n")
                        shine_output_file.write("\t\t}\n")  # Add a comma here
                        shine_output_file.write("\t\tlegacy_lazy_load = no\n")
                        shine_output_file.write("\t}\n")  # Add a comma here

                        # Write goals information
                        goals_output_file.write(f'\tspriteType = {{\n\t\tname = "{sprite_name}"\n\t\ttexturefile = "{texture_file}"\n\t}}\n')

            # Close the shine output file
            shine_output_file.write("}\n")

            # Close the goals output file
            goals_output_file.write("}\n")

    print(f"Shine information saved to {shine_output_file_path}")
    print(f"Goals information saved to {goals_output_file_path}")
else:
    print("No 'goals' subfolder found. Shine and goals information not generated.")
