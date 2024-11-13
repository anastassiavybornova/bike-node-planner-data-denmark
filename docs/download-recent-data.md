# Downloading recent data from GeoFA

> **Note:** For the minimal instructions below we assume that the user has worked in Python before. 

## Check requirements

To download and preprocess recent knudepunktnetsværk data from GeoFA yourself, make sure that you have:

✔️ A standalone version of [Python](https://www.python.org/downloads/)

✔️ An updated version of [`conda`](https://docs.conda.io/en/latest/)

## Run Steps 1-3 from [README.md](../README.md)

Run steps 1-3 from the README:
1. [Download the repository](../README.md#step-1-download-this-repository)
2. [Install required software](../README.md#step-2-install-required-software)
3. [Define study area and evaluation layers](../README.md#step-3-define-your-study-area-and-your-evaluation-layers)

## Fill out configuration file

In `./config/config.yml`, set `geofa` to `True`:

```python
geofa: True
```

## Install `knupu` environment

In your terminal, navigate to the main folder of this repository (`./bike-node-planner-data-denmark/`) and install the `knupu` environment with `conda` by running:

```
conda env create -f environment.yml
conda activate knupu
```

## Download data

### Automated download

In your terminal, and with the `knupu` environment activated, run the script:
```
python scripts/recent-data-download.py
```

> **Note:** This only works for municipalities for which data is currently publicly availabe on GeoFA. If your municipality of interest does not have publicly available data yet, or if the script fails to run for another reason, follow the instructions below for manual download.

### Manual download

Log in with your credentials at GeoFA. If you have the necessary access rights, you will be able to now see the data displayed on the [interactive map](https://geofa-kort.geodanmark.dk/app/fkg/?config=/api/v2/configuration/fkg/configuration_fkg_udgivet_5f465f5d3181f687353260.json#Basis_kort/8/9.8328/55.9892/fkg.t_5609_cykelknudepunktsstraekninger,fkg.t_5608_cykelknudepunkter). 

1. To download the file `cykelknudepunkter.gpkg`, go to: `Menu > Cykelknudepunktsnetværk > `**`Cykelknudepunkter`**` > ... > Download button > Download > GeoPackage > Click to download` 
1. To download the file `cykelknudepunktsstraekninger.gpkg`, go to: `Menu > Cykelknudepunktsnetværk > `**`Cykelknudepunktsstraekninger`**` > ... > Download button > Download > GeoPackage > Click to download` 

Place both downloaded files in the folder `bike-node-planner-data-denmark/data/network-technical/geofa`.

## Preprocess data

Verify that automated or manual data download to `data/network-technical/geofa/` has been successful. There should be the following files in the folder:
* `cykelknudepunkter.gpkg`
* `cykelknudepunktsstraekninger.gpkg`

If so, you can now run the preprocessing script that will generate simplified network data and save it to `data/network-communication/geofa/`. 

To run the preprocessing script, in your terminal and with the `knupu` environment activated, run:

```
python scripts/recent-data-simplify.py
```

## Continue with Steps 4-5 from [README.md](../README.md)

Verify that data generation in `data/network-communication/geofa/` has been successful. There now should be the following file in the folder:
* `edges.gpkg`

If so, you can now continue with steps 4-5 from the [README](../README.md#step-4-generate-the-data).