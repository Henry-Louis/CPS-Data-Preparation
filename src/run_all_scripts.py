import subprocess
import os
from config import ROOT_DIR

if __name__ == "__main__":
    # Change the working directory to the root directory
    os.chdir(ROOT_DIR)

    # Define the list of scripts to run
    script_list = [
        "download_01_cps_dictionaries_and_datasets.py", 
        "prep_01_parse_cps_dictionaries.py", "prep_02_parse_cps_datasets.py",
        "prep_03_clean_str_variables.py", "prep_04_construct_family_related_variables.py",
        "prep_05_clean_and_merge_datasets.py", "prep_06_construct_cohort_id.py",
        "plot_01_age_distribution.py"
    ]

    # Run all the scripts
    for script in script_list:
        subprocess.run(["python", f"src/{script}"])