import os

main_folder = "../input-for-bike-node-planner/"
os.makedirs(main_folder, exist_ok=True)

sub_folders = [
    "dem",
    "elevation",
    "linestring",
    "network",
    "point",
    "polygon",
    "studyarea"
]

for sub_folder in sub_folders:
    os.makedirs(main_folder + sub_folder, exist_ok=True)

print("Folders created!")