# %%
exec(open("../src/helper_functions.py").read())

remove_output_data(
    [
        "../data/dem", 
        "../input-for-bike-node-planner/dem"
    ], 
    remove_previous_output=True
)

# %%
print("Downloading and merging elevation data. This can take several minutes per municipality.")

exec(open("../src/download_dem.py").read())

print("Elevation data downloaded! Starting to merge...")

exec(open("../src/merge_dem.py").read())

print("Elevation data ready!")

# %%
