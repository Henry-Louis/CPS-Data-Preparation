from pathlib import Path
from typing import List, Dict
from tqdm.auto import tqdm
import pandas as pd
from config import CPS_DATA_FW_DIR, CPS_DICT_CSV_LIST, CPS_DATA_CSV_DIR

def convert_fixed_width_data_to_csv(data_fx_file: Path, dict_csv_file: Path, output_dir: Path) -> None:
    """
    Convert a fixed-width data file to a CSV file using a CPS dictionary file.
    
    Parameters:
        data_fx_file (Path): The path to the fixed-width data file.
        dict_csv_file (Path): The path to the dictionary CSV file.
        output_dir (Path): The directory to save the CSV file.
    
    Returns:
        None
    """
    # Load the dictionary
    dict_df = pd.read_csv(dict_csv_file)
    
    # Extract the var_name, start_pos, and end_pos columns
    dict_df = dict_df[["var_name", "start_pos", "end_pos"]]
    
    # Load the fixed-width data file
    data_df = pd.read_fwf(data_fx_file, colspecs=dict_df[["start_pos", "end_pos"]].values.tolist(), header=None)
    
    # Assign the column names
    data_df.columns = dict_df["var_name"]
    
    # Save the data as a CSV file
    output_file = output_dir / data_fx_file.with_suffix(".csv").name
    data_df.to_csv(output_file, index=False)

def find_corresponding_dict_file(data_file: Path, dict_csv_files: List[Path]) -> Path:
    """
    Search and return the corresponding dictionary file for a given data file.
    
    Parameters:
        data_file (Path): The path to the data file.
        dict_csv_files (List[Path]): A list of dictionary CSV files.
    
    Returns:
        Path: The path to the corresponding dictionary file.
    """
    
    # Extract the start time from the data file name
    start_time = data_file.stem.split("_")[-1]
    
    # Find the corresponding dictionary file
    dict_csv_files = sorted(dict_csv_files)
    for dict_file in dict_csv_files:
        dict_time = dict_file.stem.split("_")[-1]
        if dict_time <= start_time:
            return dict_file
        
    raise ValueError(f"No corresponding dictionary CSV file found for {data_file}")
        
def parse_cps_data_files(data_dir: Path, dict_csv_files: List[Path], output_dir: Path) -> None:
    """
    Parse all the CPS data files in a directory.
    
    Parameters:
        data_dir (Path): The directory containing the CPS data files.
        dict_csv_files (List[Path]): A list of dictionary CSV files.
        output_dir (Path): The directory to save the parsed data CSV files.
        
    Returns:
        None
    """
    # Create the output directory if it does not exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all the fixed-width data files
    data_files = list(data_dir.glob("*"))
    
    # Parse each data file
    for data_file in tqdm(data_files):
        dict_csv_file = find_corresponding_dict_file(data_file, dict_csv_files)
        convert_fixed_width_data_to_csv(data_file, dict_csv_file, output_dir)
        
if __name__ == "__main__":
    parse_cps_data_files(CPS_DATA_FW_DIR, CPS_DICT_CSV_LIST, CPS_DATA_CSV_DIR)