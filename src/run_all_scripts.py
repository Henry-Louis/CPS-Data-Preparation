import subprocess
import os
from config import ROOT_DIR, SRC_DIR

if __name__ == "__main__":
    # Change the working directory to the root directory
    os.chdir(ROOT_DIR)

    # Find all scripts in the src directory
    script_list = list(SRC_DIR.glob("*.py"))
    script_list.sort()
    download_script_list = [script for script in script_list if script.name.startswith("download_")]
    prep_script_list = [script for script in script_list if script.name.startswith("prep_")]
    plot_script_list = [script for script in script_list if script.name.startswith("plot_")]
    scripts_to_run = download_script_list + prep_script_list + plot_script_list
    
    # Run all the scripts
    for script in scripts_to_run:
        print(f"Running {script.name}")
        subprocess.run(["python", script])