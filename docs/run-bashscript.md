# Run the bash script `scripts/run.sh`

1. Open your command line interface (on Windows: Command Prompt; on MacOS/Linux: Terminal). In the command line interface, navigate to the subfolder `scripts`, located in main folder of this repository, which you downloaded in [Step 01](../README.md#step-1-download-the-contents-of-this-repository) (`bike-node-planner-data-denmark-main/scripts/`)
2. Run the following command, replacing `<qgispythonpath>` and `<qgisprojpath>` as described below: 
```
bash run.sh <qgispythonpath> <qgisprojpath>
```
`<qgispythonpath>` is the path to your Python installation for the QGIS app on your local machine (which you already used in [Step 02](../README.md#step-2-software-installations)). `<qgisprojpath>` is the path to the folder of your  QGIS installation files in which the file `proj.db` is located (to determine the location of `proj.db`, navigate to your QGIS installation files in your file explorer, then search for `proj.db`). See an example (for MacOS) in the screenshot below.

> **Note** that depending on the size and number of municipalities in your study area, running the bash script can take several minutes. Status messages will be printed out as the script runs (see screenshot below).

3. Once the script has successfully finished, you will see the following printout in your command line interface:

<p align="center"><img alt="running the bash script" src="/docs/screenshots/bash.png" width=80%></p>