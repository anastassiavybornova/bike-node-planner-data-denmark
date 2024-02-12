# bike-node-planner-data-denmark

This repo contains all data and scripts necessary to _automatically_ create the input data needed for the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner) for one or several Danish municipalities.

## Instructions

**Fill out the info** (currently in config files, later in a GUI):

* Which municipalities? (`config-municipalities.yml`)
* Which point layers? (`config-layers-point.yml`)
* Which linestring layers? (`config-layers-linestring.yml`)
* Which polygon layers? (`config-layers-polygon.yml`)

**Set up the code environment** 

**Run the script** (`scripts/make_input.ipynb`)

**Data is ready** in subfolders of `/input-for-bike-node-planner/`