# ------------------------
# Gif2SVMU
# By VincentNL 20/02/2023
#
# ShinobiVMU (.svmu) is a custom VMU animation / gfx data format I've made for RAH, compatible with original VMU gfx data.
# Use this script to convert animated gifs to ShinobiVMU animation format/script.
#
# Full credit to skewbmaster for Build VMU GFX code part which were repurposed for this script.
# https://github.com/Refragg/VMU-Bad-Apple/blob/master/converter.py
# ------------------------

import struct
import tkinter as tk
import glob
import os
from collections import defaultdict
from PIL import Image
from tkinter import filedialog

debug = False

# -----------------------
# (1) Read .GIF animation
# -----------------------

# Open a file dialog to select the input GIF file
root = tk.Tk()
root.withdraw()

# Open the GIF and get the number of frames
filename = filedialog.askopenfilename(filetypes=[("GIF Files", "*.gif")])
gif = Image.open(filename)
num_frames = gif.n_frames

# Check if animation loops or not
if "loop" in gif.info:
    loop = 1
else:
    loop = 0

# Create a list of the hash values of each frame
hashes = [hash(gif.seek(i) or gif.tobytes()) for i in range(num_frames)]

# Find duplicate frames and if debug:print which frames they match
duplicates = defaultdict(list)
list_of_frames = list(range(num_frames))
for i, hash_val in enumerate(hashes):
    for j in range(i + 1, num_frames):
        if hash_val == hashes[j]:
            duplicates[i].append(j)

# Find duplicate frames, store them in "dup" list
if duplicates:
    if debug:print("Duplicates:")
    for i, dup_list in duplicates.items():
        if debug:print("Frame {} is a duplicate of frame(s) {}".format(i, dup_list))
        for dup in dup_list:
            list_of_frames[dup] = i

    tot_dupes = len(duplicates)
    if debug:print(tot_dupes)
else:
    if debug:print("No duplicates found.")
if debug:print(list_of_frames)


# -------------------------------------
# (2) Prepare folders for output files
# -------------------------------------

# Create folders to store binary data and .png frames
basename = glob.os.path.basename(filename)
basepath = os.path.dirname(filename)
folder_path = f'{basepath}/animations/{basename[:-4]}'
data_path = f'{basepath}/animations/{basename[:-4]}/data'
if debug:print(folder_path)
if debug:print(data_path)

# Check if data_path exist:
if not os.path.exists(data_path):
    os.makedirs(data_path)
    if debug:print(f"Folder '{data_path}' created.")
else:
    if debug:print(f"Folder '{data_path}' already exists.")

# Check if folder_path exist:
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    if debug:print(f"Folder '{folder_path}' created.")
else:
    if debug:print(f"Folder '{folder_path}' already exists.")


# --------------------------
# (3) Write animation script
# --------------------------

# Check frames duration

frame_delays = []
arr = []  # new array of frames

# Loop through each frame in the GIF image
for i in range(0, gif.n_frames):
    # Select the current frame
    gif.seek(i)
    # Get the duration of the current frame (in milliseconds)
    frame_delay = gif.info["duration"]
    # Add the delay time of the current frame to the list
    frame_delays.append(frame_delay)

    # Repeat the current frame based on its delay time (in increments of 300ms)
    times = round(frame_delay / 300)
    if times < 1:
        times = 1
    for y in range(times):
        arr.append(list_of_frames[i])

    if debug: print(f"Frame {i}, Delay: {frame_delay}, Repeated {times} times")


# Rearrange frame numbers as they will be written in GFX data

unique_vals = list(set(arr))
unique_vals.sort()

rankings = {}
for i, val in enumerate(unique_vals):
    rankings[val] = i

arr = [rankings[x] for x in arr]

if debug:print('array after:',arr)

# Open binary file in write mode
with open(data_path+"/"+basename[:-4]+"_anim_script"+".bin", "wb") as f:
    # Iterate over each value in the list
    for value in arr:
        # Pack the value as an unsigned char (uint8) using the struct.pack() function
        packed_value = struct.pack("B", value)
        # Write the packed value to the file
        f.write(packed_value)

    # Write control code for animation loop
    if loop == 0:
        f.write(struct.pack("B", 254))
    else:
        f.write(struct.pack("B", 255))

# -------------------------------------
# (4) Write unique frames to 1bpp .PNGs
# -------------------------------------

# Rearrange uniques:
unique_list = list(set(list_of_frames))

# Sort the list in ascending order
unique_list.sort()
if debug:print(unique_list)

# Extract each frame and convert to a PNG image
for i in range(len(unique_list)):
    # Set the current frame
    gif.seek(unique_list[i])

    # Convert the current frame to an 1bpp PNG image
    png = gif.convert('1')

    # Save the PNG image to a file with a name based on the frame index
    png.save(f"{folder_path}/frame_{str(unique_list[i]).zfill(3)}.png")

# -----------------
# (5) Build VMU GFX
# -----------------

path = f'{folder_path}/*.png'
if debug:print('path of pngs:',path)
num_files = len(glob.glob(path))
if debug:print('number of files:',num_files)
totalbytes = bytearray()
for i in range(num_files): # Iterate through all frames
    currentPath = f"{folder_path}/frame_{str(unique_list[i]).zfill(3)}.png" # Set Path to current frame (change filepath and extension accordingly)

    image = Image.open(currentPath) # Open Image at path

    curbyte = 0 # Initialise byte builder

    for i in range(31,-1,-1): # Iterate from the bottom right pixel (VMU format)
        for j in range(47,-1,-1):
            # Build the current byte (6 for each horizontal line)
            # Take the value at the current pixel and flip it by abusing python types
            # The value is shifted to it's relative position
            curbyte += (not image.getpixel((j,i))) << (j % 8)

            if 7 - (j % 8) == 7: # If the byte is finished, we add it to the bytearray
                totalbytes.append(curbyte)
                curbyte = 0

    image.close()

# Create a byte file and store everything in order for the dreamcast program to read
finalfile = open(f'{data_path}/vmu_gfx.bin', 'wb')
finalfile.write(totalbytes)
finalfile.close()
