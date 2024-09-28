# Run the bash script `scripts/run.sh`

1. Open your command line interface (on Windows: Command Prompt; on MacOS/Linux: Terminal). 
2. In the command line interface, navigate to the subfolder `scripts`, located in main folder of this repository, which you downloaded in [Step 01](../README.md#step-1-download-the-contents-of-this-repository) (`bike-node-planner-data-denmark-main/scripts/`)
3. Run the bash script `run.sh` with flags described below, for example:

```bash
bash run.sh --download_elevation 0 --python_path /Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.9 --projdb_path /Applications/QGIS-LTR.app/Contents/Resources/python/site-packages/fiona/proj_data/
```

* `download_elevation`: 1 for Yes, 0 for No (should elevation data be downloaded?)
* `python_path`: the path to your Python installation for the QGIS app on your local machine (which you already used in [Step 02](../README.md#step-2-software-installations)).
* `projdb_path`: the path to the folder of your fiona installation (Python package within QGIS) in which the file `proj.db` is located. 


<details>
<summary>To determine the location of `proj.db`:</details>

* Navigate to your QGIS installation in your file explorer.
* On a Mac, go to Applications > Find QGIS > Right click and choose *'Show package contents'*.
* In the QGIS installation folder, search for `proj.db` and copy the file path. On a MacOS, you can do this selecting the proj.db file, right clicking on the file in the bottom of the window, and choosing *'Copy "proj.db" as Path name'* (see an example for MacOS in the screenshot below).

<p align="center"><img alt="identifying the proj path" src="/docs/screenshots/find_proj.png" width=100%></p>

</details>



> **Note** that depending on the size and number of municipalities in your study area, running the bash script can take several minutes. Status messages will be printed out as the script runs (see screenshot below).

3. Once the script has successfully finished, you will see the following printout in your command line interface:

<p align="center"><img alt="running the bash script" src="/docs/screenshots/bash.png" width=100%></p>