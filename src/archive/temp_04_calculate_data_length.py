import pandas as pd
from config import CPS_DATA_CLEANED_DIR

def calculate_data_length(data_df: pd.DataFrame) -> int:
    """
    Calculate the length of a DataFrame.
    
    Parameters:
        data_df (pd.DataFrame): The DataFrame to calculate the length of.
        
    Returns:
        int: The length of the DataFrame.
    """
    return len(data_df)

def main() -> None:
    total_obs = 0
    for file in CPS_DATA_CLEANED_DIR.glob("*.csv"):
        data_df = pd.read_csv(file)
        data_length = calculate_data_length(data_df)
        print(f"{file.name}: {data_length}")
        total_obs += data_length
        
    print(f"Total observations: {total_obs}")
    
if __name__ == "__main__":
    main()