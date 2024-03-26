# BikeNodePlanner: Data for Denmark

This repository contains all data and scripts necessary to _automatically_ create the input data needed for the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner) for one or several Danish municipalities.

## Step 1: Install the software

**TODO** installation instructions: shortened version of already existing installation instructions from bike-node-planner

## Step 2: Provide information on your study area and evaluation interests

**Fill out the info** (currently in config files, later in a GUI):
* Which municipalities? (`config-municipalities.yml`)
* Which point layers? (`config-layers-point.yml`)
* Which linestring layers? (`config-layers-linestring.yml`)
* Which polygon layers? (`config-layers-polygon.yml`)

## Step 3: Generate the data

**Run the notebook `make_input`** (`scripts/make_input.ipynb`) to generate the data.

## Step 4: Use the data

After completing the steps 1-3 described above, the **data is ready** in subfolders of `/input-for-bike-node-planner/`. Follow the steps in the [bike-node-planner repo](https://github.com/anastassiavybornova/bike-node-planner) to run a complete analysis; to provide data, simply copy-paste all subfolders of `/input-for-bike-node-planner/` (this repo) into `/data/input/` subfolder (other repo).