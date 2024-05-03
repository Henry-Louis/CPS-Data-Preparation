from glob import glob
from pathlib import Path
import shutil
from config import RAW_CPS_DATA_DIR

def lower_filename_and_remove_last_underscore(file_path: str) -> None:
    """
    Lower the filename and remove the last underscore in the filename.
    
    Parameters:
        file_path (str): The path to the file.
    
    Returns:
        None
    """
    file_path = Path(file_path)
    parent_dir = file_path.parent
    filename = file_path.stem.lower()
    
    if "cps" not in filename: # only rename CPS data files
        return
    
    filename_subcomponents = filename.split("_")
    if len(filename_subcomponents) not in [3,4]:
        print(f"Filename {filename} does not have 3 or 4 subcomponents, skipping")
        return
    if len(filename_subcomponents) == 3:
        new_filename = f"{filename_subcomponents[0]}_{filename_subcomponents[1]}{filename_subcomponents[2]}"
    else:
        new_filename = f"{filename_subcomponents[0]}_{filename_subcomponents[1]}{filename_subcomponents[2]}_{filename_subcomponents[3]}"
    
    shutil.move(file_path, parent_dir / f"{new_filename}{file_path.suffix}")
    
def rename_cps_datasets(data_dir: str) -> None:
    """
    Rename the CPS data files in the given directory.
    
    Parameters:
        data_dir (str): The path to the directory containing the CPS data files.
    
    Returns:
        None
    """
    for folder_name in ["gz", "fixedwidth", "fixedwidth/subsets"]:
        print(str(data_dir) + f"/{folder_name}/*")
        for data_file in glob(str(data_dir) + f"/{folder_name}/*"):
            lower_filename_and_remove_last_underscore(data_file)
        
if __name__ == "__main__":
    rename_cps_datasets(RAW_CPS_DATA_DIR)