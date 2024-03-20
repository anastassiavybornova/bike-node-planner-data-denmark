# bike-node-planner-data-denmark

This repo contains all data and scripts necessary to _automatically_ create the input data needed for the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner) for one or several Danish municipalities.

## Instructions

1. **Fill out the info** (currently in config files, later in a GUI):
* Which municipalities? (`config-municipalities.yml`)
* Which point layers? (`config-layers-point.yml`)
* Which linestring layers? (`config-layers-linestring.yml`)
* Which polygon layers? (`config-layers-polygon.yml`)

2. **Set up the code environment** (like knudepunkter)

3. **Run the notebook `make_input`** (`scripts/make_input.ipynb`)

4. **Data is ready** in subfolders of `/input-for-bike-node-planner/`

5. Follow the steps in the [bike-node-planner repo](https://github.com/anastassiavybornova/bike-node-planner); to provide data, simply copy-paste all subfoldersof `/input-for-bike-node-planner/` (this repo) into `/data/input/` subfolder (other repo)