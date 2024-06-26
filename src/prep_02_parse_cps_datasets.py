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
    # Check the existency of the output data file
    output_file = output_dir / data_fx_file.with_suffix(".csv").name
    if output_file.exists():
        print(f"The file {output_file.stem} already exists, skipping...")
        return
    
    # Load the dictionary
    dict_df = pd.read_csv(dict_csv_file)
    
    # Extract the var_name, start_pos, and end_pos columns
    dict_df = dict_df[["var_name", "start_pos", "end_pos"]]
    dict_df = dict_df.sort_values("start_pos")
    colspecs = [(row["start_pos"] - 1, row["end_pos"]) for _, row in dict_df.iterrows()]
    
    # Load the fixed-width data file
    data_df = pd.read_fwf(data_fx_file, colspecs=colspecs, header=None)
    
    # Assign the column names
    data_df.columns = dict_df["var_name"]
    needed_columns = [col for col in data_df.columns.to_list() if col not in ["FILLER", "FILLER.2"]]
    data_df = data_df[needed_columns]
    
    # Save the data as a CSV file
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
    dict_csv_files = sorted(dict_csv_files, key=lambda x: x.stem.split("_")[-1], reverse=True)
    for dict_file in dict_csv_files:
        dict_time = dict_file.stem.split("_")[-1]
        if dict_time <= start_time:
            return dict_file
        
    raise ValueError(f"No corresponding dictionary CSV file found for {data_file}")

def validate_founded_dict_files(data_files: List[Path], dict_csv_files: List[Path]) -> None:
    """
    Validate the founded dictionary files for the data files.
    
    Parameters:
        data_files (List[Path]): A list of data files.
        dict_csv_files (List[Path]): A list of dictionary CSV files.
    
    Returns:
        None
    """
    data_files.sort()
    for data_file in data_files:
        dict_csv_file = find_corresponding_dict_file(data_file, dict_csv_files)
        print(f"Matched variable dictionary for {data_file.stem}: {dict_csv_file.stem}")

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
    
    # Find all the fixed-width data files (exclude "subset" files)
    data_files = list(data_dir.glob("*"))
    data_files = [file for file in data_files if "subset" not in file.stem]
    data_files.sort()
    
    # Parse each data file
    for data_file in tqdm(data_files):
        dict_csv_file = find_corresponding_dict_file(data_file, dict_csv_files)
        convert_fixed_width_data_to_csv(data_file, dict_csv_file, output_dir)
   
def validate_parsed_csv_files(csv_dir: Path) -> None:
    """
    Validate the parsed CSV files, make sure no unexpected string values are present.
    
    Parameters:
        csv_dir (Path): The directory containing the parsed CSV files.
    """
    csv_files = list(csv_dir.glob("*.csv"))
    csv_files.sort()
    
    for csv_file in csv_files:
        allowed_str_columns = ["HRSAMPLE", "HRSERSUF"]
        df = pd.read_csv(csv_file, dtype={var : str for var in allowed_str_columns})
        num_columns = len(df.columns)
        num_entries = len(df)
        str_columns = df.select_dtypes(include="object").columns
        unexpected_str_columns = [col for col in str_columns if col not in allowed_str_columns]
        
        # Check for number of columns
        if num_columns <= 300:
            raise ValueError(f"Number of columns is too low in {csv_file.stem}")
        # Check for number of entries
        if num_entries <= 100000:
            raise ValueError(f"Number of entries is too low in {csv_file.stem}")
        # Check for string columns
        if len(unexpected_str_columns) > 0:
            print(f"Unexpected string columns in {csv_file.stem}: {unexpected_str_columns}")
            for col in unexpected_str_columns:
                print(f"Unique Values for {col}:\n{df[col].value_counts()}")
            continue
        
        print(f"Validated {csv_file.stem}")


if __name__ == "__main__":
    # Validate the founded dictionary files for the data files
    data_files = [file for file in list(CPS_DATA_FW_DIR.glob("*")) if "subset" not in file.stem]
    dict_csv_files = CPS_DICT_CSV_LIST
    validate_founded_dict_files(data_files, dict_csv_files)
    
    # Parse and validate the CPS data files
    parse_cps_data_files(CPS_DATA_FW_DIR, CPS_DICT_CSV_LIST, CPS_DATA_CSV_DIR)
    # validate_parsed_csv_files(CPS_DATA_CSV_DIR)
    