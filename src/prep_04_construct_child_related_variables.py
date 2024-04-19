from typing import List
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm
from config import (
    CPS_DATA_CLEANED_DIR, CPS_DATA_CHILD_DIR,
    DATA_YEAR, BIRTH_YEAR, AGE,
    HOUSEHOLD_ID, RELATIONSHIP,
    IS_PARENT, IS_CHILD, IS_OLDEST_CHILD,
    AGE_OF_OLDEST_CHILD, 
    MARRITAL_STATUS, IS_MARRIED, MARRIAGE_TIMES
)


def load_data(data_file: Path) -> pd.DataFrame:
    """
    Load the cleaned CPS data, with DATA_YEAR added.
    
    Parameters:
        data_file (Path): The path to the cleaned CPS data.
        
    Returns:
        pd.DataFrame: The cleaned CPS data with DATA_YEAR added.
    """
    dtype = {"HRSAMPLE": str, "HRSERSUF": str}
    data_df = pd.read_csv(data_file, dtype=dtype)
    year = int(data_file.stem.split("_")[-1][:4])
    data_df[DATA_YEAR] = year
    
    return data_df

def add_birth_year(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add the birth year variable to the CPS data.
    
    Parameters:
        data_df (pd.DataFrame): The CPS data.
        
    Returns:
        pd.DataFrame: The CPS data with the birth year variable.
    """
    birth_year = data_df[DATA_YEAR] - data_df[AGE]
    data_df[BIRTH_YEAR] = birth_year
    return data_df

def add_is_married(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add the IS_MARRIED variable to the CPS data.
    
    Parameters:
        data_df (pd.DataFrame): The CPS data.
        
    Returns:
        pd.DataFrame: The CPS data with the IS_MARRIED variable.
    """
    data_df[IS_MARRIED] = None
    data_df.loc[data_df[MARRITAL_STATUS].isin([1, 2]), IS_MARRIED] = 1
    data_df.loc[data_df[MARRITAL_STATUS] == 6, IS_MARRIED] = 0
    data_df[IS_MARRIED].fillna(-1, inplace=True) # only consider married and never married
    
    return data_df

def get_family_groups(data_df: pd.DataFrame) -> List[pd.DataFrame]:
    """
    Group the entries in a DataFrame by family.
    
    Parameters:
        data_df (pd.DataFrame): The DataFrame to group.
        
    Returns:
        List[pd.DataFrame]: The groups of entries.
    """
    family_groups = data_df.groupby(HOUSEHOLD_ID)
    return [group for _, group in family_groups]

def add_family_based_variables_for_household(family_group: pd.DataFrame) -> pd.DataFrame:
    """
    Add family-based variables to a family group (IS_PARENT, IS_CHILD, IS_OLDEST_CHILD,
    AGE_OF_OLDEST_CHILD).
    
    Parameters:
        family_group (pd.DataFrame): The family group.
        
    Returns:
        pd.DataFrame: The family group with the child-related variables.
    """
    if family_group[HOUSEHOLD_ID].nunique() != 1:
        raise ValueError("The family group should contain only one household.")
    
    # TODO: CHECK THE ENTIRE LOGIC
    # family_group = family_group.copy()

    # # Initialize the variables
    # family_group[IS_PARENT] = 0

    # # Check if there are any parents in the family group
    # is_child = family_group[RELATIONSHIP] == 3

    # # Set IS_PARENT, IS_CHILD, IS_OLDEST_CHILD, and AGE_OF_OLDEST_CHILD using boolean conditions
    # family_group[IS_PARENT] = (is_child.any()) * (family_group[RELATIONSHIP].isin([1, 2])).astype(int)
    # family_group[IS_CHILD] = (is_child).astype(int)
    # family_group[IS_OLDEST_CHILD] = ((family_group[AGE] == family_group[AGE].max()) & is_child).astype(int)
    # family_group[AGE_OF_OLDEST_CHILD] = -1 if is_child.any() else family_group[AGE].max()
    
    # # Keep only the reference person and the spouse
    # family_group = family_group[family_group[RELATIONSHIP].isin([1, 2])]

    # return family_group
    

def add_family_based_variables(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add child-related variables to the CPS data.
    
    Parameters:
        data_df (pd.DataFrame): The CPS data.
        
    Returns:
        pd.DataFrame: The CPS data with the child-related variables.
    """
    if data_df[HOUSEHOLD_ID].nunique() <= 1:
        raise ValueError("The DataFrame should contain multiple households.")
    
    family_groups = get_family_groups(data_df)
    family_groups = [add_family_based_variables_for_household(family_group) for family_group in family_groups]
    data_df = pd.concat(family_groups)
    
    return data_df

def add_variables_to_csv_file(data_file: Path) -> pd.DataFrame:
    """
    Add child-related variables to the cleaned CPS data.
    
    Parameters:
        data_file (Path): The path to the cleaned CPS data.
        
    Returns:
        pd.DataFrame: The cleaned CPS data with the child-related variables.
    """
    data_df = load_data(data_file)
    data_df = add_birth_year(data_df)
    data_df = add_is_married(data_df)
    data_df = add_family_based_variables(data_df)
    
    return data_df

def main() -> None:
    # Create the directory for the child-related CPS data
    CPS_DATA_CHILD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all cleaned CPS data files
    cleaned_data_files = list(CPS_DATA_CLEANED_DIR.glob("*.csv"))
    
    # Loop over all cleaned CPS data files
    for cleaned_data_file in tqdm(cleaned_data_files, desc="Adding child-related variables"):
        child_data_file = CPS_DATA_CHILD_DIR / cleaned_data_file.name
        child_data_df = add_variables_to_csv_file(cleaned_data_file)
        child_data_df.to_csv(child_data_file, index=False)
        break
    
if __name__ == "__main__":
    main()