from typing import List
from pathlib import Path
import pandas as pd
from config import CPS_DATA_CHILD_DIR, MERGED_CSV_FILE
from variable_typing import *

def get_child_data_files(child_csv_dir: Path) -> List[Path]:
    """
    Get the paths of the child data files.
    
    Parameters:
        child_csv_dir (Path): The directory containing the child data files.
        
    Returns:
        List[Path]: The paths of the child data files.
    """
    files = list(child_csv_dir.glob("*.csv"))
    return files

def load_child_data(data_file: Path, columns: List[str]) -> pd.DataFrame:
    """
    Load the child data.
    
    Parameters:
        data_file (Path): The path to the child data file.
        columns (List[str]): The columns to load.
        
    Returns:
        pd.DataFrame: The child data.
    """
    return pd.read_csv(data_file, usecols=columns)

def merge_datasets_and_save(data_files: List[Path], output_file: Path, needed_variables: List[str]) -> None:
    """
    Merge the child datasets and save the merged dataset.
    
    Parameters:
        data_files (List[Path]): The paths to the child datasets.
        output_file (Path): The path to save the merged dataset.
        needed_variables (List[str]): The variables needed in the merged dataset.
    """
    # Load the child datasets
    output_file.parent.mkdir(parents=True, exist_ok=True)
    data_df = pd.concat([load_child_data(data_file, needed_variables) for data_file in data_files])
    
    # Check for missing values
    len_before = data_df.shape[0]
    data_df.dropna(how="any", inplace=True)
    len_after = data_df.shape[0]
    if len_before != len_after:
        raise ValueError(f"Missing values found in the merged dataset: {len_before - len_after} rows dropped.")
    
    # Save the merged dataset
    data_df.to_csv(output_file, index=False)
    print(f"Merged dataset shape: {data_df.shape}, from {len(data_files)} files.")

def main() -> None:
    data_files = get_child_data_files(CPS_DATA_CHILD_DIR)
    merge_datasets_and_save(data_files, MERGED_CSV_FILE, NEEDED_VARS)
    print("Child datasets merged and saved.")
    
if __name__ == "__main__":
    main()