# Make necessary folders for output data
# %%
import os

folders = [
    "input-for-bike-node-planner",
    "data/polygon",
    "data/point",
    "data/dem",
    "input-for-bike-node-planner/dem",
    "input-for-bike-node-planner/studyarea",
    "input-for-bike-node-planner/point/",
    "input-for-bike-node-planner/linestring/",
    "input-for-bike-node-planner/polygon/",
]

# If paths do not exist

for f in folders:
    if not os.path.exists(f):
        os.mkdir(f)

print("Folders created successfully!")
# %%
