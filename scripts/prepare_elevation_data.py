# %%

print("Downloading and merging elevation data. This may take a while... ")

exec(open("download_dem.py").read())

print("Elevation data downloaded! Starting to merge...")

exec(open("merge_dem.py").read())

print("Elevation data ready!")

# %%
