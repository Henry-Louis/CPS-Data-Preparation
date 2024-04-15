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
    # Replace invalid values with NaN
    data_df["HULENSEC"] = pd.to_numeric(data_df["HULENSEC"], errors="coerce")
    data_df["GEMSAST"] = data_df["GEMSAST"].replace("-", "NaN")
    data_df["HRSERSUF"] = data_df["HRSERSUF"].replace("-", "NaN")
    
    return data_df

def main() -> None:
    """
    Main function.
    """
    # Create the output directory
    CPS_DATA_CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Loop through the data files
    data_files = list(CPS_DATA_CSV_DIR.glob("*.csv"))
    for data_file in tqdm(data_files):
        # Load the data
        data_df = pd.read_csv(data_file)
        
        # Clean the string variables
        data_df = clean_str_variables(data_df)
        
        # Save the cleaned data
        output_file = CPS_DATA_CLEANED_DIR / data_file.name
        data_df.to_csv(output_file, index=False)
        
    
if __name__ == "__main__":
    main()