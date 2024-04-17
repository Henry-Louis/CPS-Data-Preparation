from typing import List
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm
from config import CPS_DATA_CLEANED_DIR, CPS_DATA_CHILD_DIR

# step 1: group the entries by family
def get_family_groups(data_df: pd.DataFrame) -> List[pd.DataFrame]:
    """
    Group the entries in a DataFrame by family.
    
    Parameters:
        data_df (pd.DataFrame): The DataFrame to group.
        
    Returns:
        List[pd.DataFrame]: The groups of entries.
    """
    family_groups = data_df.groupby("HRHHID")
    return [group for _, group in family_groups]

# step 2: construct the first child variable
def construct_first_child_variable(family_df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct the first child variable in a family.
    
    Parameters:
        family_df (pd.DataFrame): The DataFrame for a family.
        
    Returns:
        pd.DataFrame: The DataFrame with the first child variable.
    """
    # Sort the entries by age
    family_df = family_df.sort_values("PRTAGE")
    
    # Construct the first child variable
    family_df["FIRSTCHILD"] = 0
    first_child_idx = family_df["PRTAGE"].idxmax()
    family_df.loc[first_child_idx, "FIRSTCHILD"] = 1
    
    return family_df