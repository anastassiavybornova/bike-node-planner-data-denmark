# BikeNodePlanner: Data for Denmark

This repository contains all data and scripts necessary to _automatically_ create the input data needed for the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner) for one or several Danish municipalities. The network data is fetched from [GeoFA](https://geofa-kort.geodanmark.dk/app/fkg/?config=/api/v2/configuration/fkg/configuration_fkg_udgivet_5f465f5d3181f687353260.json#Basis_kort/8/9.8328/55.9892/fkg.t_5609_cykelknudepunktsstraekninger,fkg.t_5608_cykelknudepunkter).

## Step 1: Download this repository

[Download](https://github.com/anastassiavybornova/bike-node-planner-data-denmark/archive/refs/heads/main.zip) or `git clone` the contents of this repository to your local machine.

## Step 2: Install required software

To set up the BikeNodePlanner environment on your machine, you need to install the latest long-term release of QGIS, as well as some additional Python packages *within* QGIS. Detailed instructions depend on your operating system:

* [macOS/linux: step02_install_software_macos](https://github.com/anastassiavybornova/bike-node-planner/blob/main/docs/step02_install_software_macos.md)
* [Windows: step02_install_software_windows](https://github.com/anastassiavybornova/bike-node-planner/blob/main/docs/step02_install_software_windows.md)

> Note: This step is identical to Step 2 in the [BikeNodePlanner](https://github.com/anastassiavybornova/bike-node-planner?tab=readme-ov-file#step-2-software-installations) instructions.

## Step 3: Define your study area and your evaluation layers

In the [`config`](config/) folder, fill out the required information:

<!-- * Data download ([`config.yml`](config/config.yml)) -->
* Which municipalities to include? ([`config-municipalities.yml`](config/config-municipalities.yml))
* Which point layers to include? ([`config-layers-point.yml`](config/config-layers-point.yml))
<!-- * Which linestring layers? (`config-layers-linestring.yml`) -->
* Which polygon layers to include? ([`config-layers-polygon.yml`](config/config-layers-polygon.yml))

Go to [./docs/define-layers.md](./docs/define-layers.md) for detailed instructions on how to define the study area and the (point and polygon) evaluation layers.

## Step 4: Generate the data

Run the bash script **`scripts/run.sh`** to generate the data. For detailed instructions on how to run the script, go to [./docs/run-bashscript.md](./docs/run-bashscript.md).

## Step 5: Use the data

After completing the steps 1-4, the **data is ready** in subfolders of `/input-for-bike-node-planner/`. Follow the steps in the [bike-node-planner repository](https://github.com/anastassiavybornova/bike-node-planner) to run a complete BikeNodePlanner analysis; to provide data, simply copy-paste all subfolders of `/input-for-bike-node-planner/` (from this repository) into `/data/input/` subfolder (to the other repository).

***

## Want to use more recent data?

> **Note:** Following the instructions above, you will make use of data that we downloaded from GeoFA on October 11, 2024, for all municipalities where data was publicly available at that moment (see [docs/list-municipalities.md](./docs/list-municipalities.md)). If you want to make use of more recent GeoFA data, and/or if data for your municipality of interest is not publicly available yet, see [`docs/download-recent-data.md`](./docs/download-recent-data.md) for instructions.

***

# Getting in touch

Questions, comments, feedback? You can reach out to us by email: [anvy@itu.dk](mailto:anvy@itu.dk)