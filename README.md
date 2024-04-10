# BikeNodePlanner: Data for Denmark

This repository contains all data and scripts necessary to _automatically_ create the input data needed for the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner) for one or several Danish municipalities.

## Step 1: Download the contents of this repository

Download the contents of this repository to your local machine. Click [here](./docs/download-repo.md) for more detailed instructions.

## Step 2: Software installations

First, set up the BikeNodePlanner environment on your machine. Detailed instructions depend on your operating system:
* [here for macOS/linux](https://github.com/anastassiavybornova/bike-node-planner/blob/main/docs/step02_install_software_macos.md)
* [here for Windows](https://github.com/anastassiavybornova/bike-node-planner/blob/main/docs/step02_install_software_windows.md)

> Note: This step is identical to Step 2 in the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner?tab=readme-ov-file#step-2-software-installations) instructions.

## Step 3: Provide information on your study area and user-defined evaluation layers

**Fill out the info**:
* Which municipalities? (`config-municipalities.yml`) 
* Which point layers? (`config-layers-point.yml`)
<!-- * Which linestring layers? (`config-layers-linestring.yml`) -->
* Which polygon layers? (`config-layers-polygon.yml`)

[Click here](./docs/define-layers.md) for detailed instructions on how to define the study area and the evaluation layers.

## Step 4: Generate the data

Run the bash script **`scripts/run.sh`** to generate the data. [Click here](./docs/run-bashscript.md) for detailed instructions.

## Step 5: Use the data

After completing the steps 1-4 described above, the **data is ready** in subfolders of `/input-for-bike-node-planner/`. Follow the steps in the [bike-node-planner repo](https://github.com/anastassiavybornova/bike-node-planner) to run a complete analysis; to provide data, simply copy-paste all subfolders of `/input-for-bike-node-planner/` (this repository) into `/data/input/` subfolder (other repository).