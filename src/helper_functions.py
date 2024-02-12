def remove_output_data(output_folders, remove_previous_output: bool = False):
    import os
    import shutil

    if remove_previous_output:
        for f in output_folders:
            if os.path.exists(f):
                shutil.rmtree(f)

                os.makedirs(f)

    print("Data folder cleaned!")
