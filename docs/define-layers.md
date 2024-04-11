# Step 3: Provide information on your study area and user-defined evaluation layers

In this step, you can customize the input data generation by selecting which municipalities to include in the analysis; which point/linestring/polygon data to include in the evaluation; and how to merge them into broader evaluation categories. You can edit `.yml` in any standard text editor on your machine; then save your changes for them to take effect, before you continue to the next step.

## Settings for data download

* Here you can provide the settings for data download and preprocessing (name of data layers in GeoFA, etc.)

The workflow includes a script that downloads elevation data from [Dataforsyningen](https://dataforsyningen.dk/).
To use this step, the setting `download_elevation_data` must be set to True (the default) *and* you must provide your username and password to Dataforsyningen.

**If** you already have an elevation raster (DEM) for the study area:
* Set the `download_elevation_data` to False. 
* After completing step 1-4 in the README.MD, place your DEM file in `/input-for-bike-node-planner/`dem/ and name the file `dem.tif`.

## Which municipalities? (`config-municipalities.yml`)

For each municipality that you want to be included in the analysis, delete the leading `#` in front of the corresponding 4-digit code; then save the file. Make sure not to change the indentation. In the example below, the file is edited so that the 3 municipalities of Gentofte, Gladsaxe, and Herlev will be included in the analysis, while the rest of the municipalities (Frederiksberg, Ballerup, etc.) will be ignored.

<p align="center"><img alt="modifying config-municipalities.yml" src="/docs/screenshots/config-muni.png" width=50%></p>

## Which point layers? (`config-layers-point.yml`)

In the file, you will find a list of categories and subcategories of point data. You can customize how these subcategories are merged into separate evaluation layers by typing the corresponding evaluation layer name next to each subcategory name. You can also choose subcategories to be excluded from the evaluation by typing `ignore` next to the subcategory name. Note that the evaluation layer names are case-sensitive. In the example below, the category is `facilit_indkoeb`; the subcategories are `supermarked`. `bager`, etc. The user-defined evaluation layers are `shop` and `tourism`. The evaluation layer `shop` will include the subcategories `supermarked, bager, kiosk, slagter, fisk`; the evaluation layer `tourism` will include the subcategory `lokale smagsoplevelser`; and finally, the subcategory `tank` will be ignored.

<p align="center"><img alt="modifying config-point.yml" src="/docs/screenshots/config-point.png" width=50%></p>

<!-- 
## Which linestring layers? (`config-layers-linestring.yml`)

In the file, you will find a list of categories and subcategories of linestring data. You can customize how these subcategories are merged into separate evaluation layers by typing the corresponding evaluation layer name next to each subcategory name. You can also choose subcategories to be excluded from the evaluation by typing `ignore` next to the subcategory name. Note that the evaluation layer names are case-sensitive. In the example below, ... [insert screentshot]
-->

## Which polygon layers? (`config-layers-polygon.yml`)

In the file, you will find a list of categories and subcategories of polygon data. You can customize how these subcategories are merged into separate evaluation layers by typing the corresponding evaluation layer name next to each subcategory name. You can also choose subcategories to be excluded from the evaluation by typing `ignore` next to the subcategory name. Note that the evaluation layer names are case-sensitive. In the example below, the categories are: `land_beskyttnatur_flade` (with 1 subcategory) and `land_frednatpark` (with 5 subcategories). The user-defined evaluation layers are: `protected-nature` (including the subcategories`Beskyttet natur, Bekendtgørelsesfredning`); `nature` (including the subcategories `Fredet område, Naturnationalpark, Nationalpark`); and `park` (including the subcategory `Naturpark`). In this example, no subcategories are ignored.

<p align="center"><img alt="modifying config-poly.yml" src="/docs/screenshots/config-poly.png" width=50%></p>
