* you need a standalone version of python, >= 3.10
* you need to install sgeop (ie also need all the sgeop dependencies)
* solve this with conda
    * if it is a muni where data is NOT publicly available: manual download
    * if it is a muni where data IS publicly available: geofa download (recent-data-download.py)
* in case of geofa download: you need to provide GeoFA access data in `config/config.yml`
* you need to run the simplfication script (recent-data-simplify.py)s BEFORE running the run.sh script 