from typing import List
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm
from config import CPS_DATA_CSV_DIR, CPS_DATA_CLEANED_DIR

def clean_str_variables(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean string variables in a DataFrame.
    
    Parameters:
        data_df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Drop FILLER columns
    data_df = data_df.drop(columns=[col for col in data_df.columns if "FILLER" in col])
    
    # Replace invalid values with NaN
    data_df["HULENSEC"] = pd.to_numeric(data_df["HULENSEC"], errors="coerce")
    data_df["GEMSAST"] = data_df["GEMSAST"].replace("-", "NaN")
    data_df["HRSERSUF"] = data_df["HRSERSUF"].replace("-", "NaN")
    
    return data_df

def get_str_columns(cleaned_df: pd.DataFrame) -> List[str]:
    """
    Get the string variables in a DataFrame.
    
    Parameters:
        cleaned_df (pd.DataFrame): The cleaned DataFrame.
        
    Returns:
        List[str]: The string variables in the DataFrame.
    """
    str_variables = cleaned_df.select_dtypes(include="object").columns.tolist()
    return str_variables

def validate_str_columns(cleaned_df: pd.DataFrame) -> bool:
    """
    Validate the string variables in a DataFrame.
    
    Parameters:
        cleaned_df (pd.DataFrame): The cleaned DataFrame.
        
    Returns:
        bool: True if the DataFrame has no string variables, False otherwise.
    """
    str_columns = get_str_columns(cleaned_df)
    str_columns = [col for col in str_columns if col != "HRSAMPLE"]
    return len(str_columns) == 0

def main() -> None:
    """
    Main function.
    """
    # Create the output directory
    CPS_DATA_CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Loop through the data files
    data_files = list(CPS_DATA_CSV_DIR.glob("*.csv"))
    for data_file in tqdm(data_files):
        # Set the output file
        output_file = CPS_DATA_CLEANED_DIR / data_file.name
        
        # Check if the cleaned data exists
        if not output_file.exists():
            data_df = pd.read_csv(data_file, dtype={"HRSAMPLE": str})
            data_df = clean_str_variables(data_df)
            data_df.to_csv(output_file, index=False)
        else:
            data_df = pd.read_csv(output_file, dtype={"HRSAMPLE": str})
            if not validate_str_columns(data_df):
                data_df = clean_str_variables(data_df)
                data_df.to_csv(output_file, index=False)
        
        # Validate the cleaned dataset
        str_columns = [col for col in get_str_columns(data_df) if col != "HRSAMPLE"]
        if not validate_str_columns(data_df):
            print(f"String columns found in {data_file}: {str_columns}")
        
    
if __name__ == "__main__":
    main()