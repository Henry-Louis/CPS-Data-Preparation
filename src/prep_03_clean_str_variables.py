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
    # Replace the "-" with NA in PTAGE variable
    data_df["PTAGE"] = data_df["PTAGE"].replace("-", pd.NA).astype("Int64")
    
    return data_df

def get_invalid_str_columns(cleaned_df: pd.DataFrame, allowed_str_vars: List[str]) -> List[str]:
    """
    Get the unexpected string variables in a DataFrame.
    
    Parameters:
        cleaned_df (pd.DataFrame): The cleaned DataFrame.
        allowed_str_vars (List[str]): A list of allowed string variables.
        
    Returns:
        List[str]: A list of string variables that are not allowed.
    """
    str_columns = cleaned_df.select_dtypes(include="object").columns.to_list()
    str_columns = [col for col in str_columns if col not in allowed_str_vars]
    return str_columns

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
        
        # Define dtype
        dtype = {"HRSAMPLE": str, "HRSERSUF": str}
        
        # Check if the cleaned data exists
        if not output_file.exists():
            data_df = pd.read_csv(data_file, dtype=dtype)
            data_df = clean_str_variables(data_df)
            data_df.to_csv(output_file, index=False)
        else:
            data_df = pd.read_csv(output_file, dtype=dtype)
            str_columns = get_invalid_str_columns(data_df, dtype.keys())
            if str_columns:
                data_df = clean_str_variables(data_df)
                data_df.to_csv(output_file, index=False)
        
        # Validate the cleaned dataset
        str_columns = get_invalid_str_columns(data_df, dtype.keys())
        if str_columns:
            print(f"String columns found in {data_file}: {str_columns}")

if __name__ == "__main__":
    main()