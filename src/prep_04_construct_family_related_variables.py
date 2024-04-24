from typing import List
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm
from config import CPS_DATA_CLEANED_DIR, CPS_DATA_CHILD_DIR
from variable_typing import *

# Data-loading function
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

# Variable-adding functions
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

def add_child_related_variables_for_household(family_group: pd.DataFrame) -> pd.DataFrame:
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

    # Calculate the number of children in the family
    is_ref_or_spouse = family_group[RELATIONSHIP].isin([1, 2]) # Series of booleans
    is_child = family_group[RELATIONSHIP] == 3 # Series of booleans
    num_children_in_family = is_child.sum() # Scalar
    has_child = (int(num_children_in_family > 0) * is_ref_or_spouse).astype(int) # Series of 0 or 1
    age_of_oldest_child = family_group.loc[is_child, AGE].max() if num_children_in_family > 0 else -1 # Scalar
    year_of_first_birth_giving = family_group[DATA_YEAR] - age_of_oldest_child if num_children_in_family > 0 else -1 # Series of years
    
    # Assign the family-based variables to the family group
    family_group[HAS_CHILD] = has_child
    family_group[AGE_OF_OLDEST_CHILD] = age_of_oldest_child
    family_group[YEAR_OF_FIRST_BIRTH_GIVING] = year_of_first_birth_giving

    return family_group[is_ref_or_spouse]

def add_child_related_variables(data_df: pd.DataFrame) -> pd.DataFrame:
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
    family_groups = [add_child_related_variables_for_household(family_group) for family_group in family_groups]
    data_df = pd.concat(family_groups)
    
    return data_df

def add_marriage_related_variables(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add marriage-related variables to the CPS data.
    
    Parameters:
        data_df (pd.DataFrame): The CPS data.
        
    Returns:
        pd.DataFrame: The CPS data with the marriage-related variables.
    """
    return data_df

def add_cohort_id(df: pd.DataFrame, var_list: List[str]=MATCHING_VARS) -> pd.DataFrame:
    """
    Construct a demographic identifier (COHORT_ID) for each individual based on the specified variables.

    Parameters:
    - df: DataFrame containing the specified variables
    - var_list: list of variable names to be used in constructing the demographic identifier

    Returns:
    - df: DataFrame with the demographic identifier added
    """
    # Construct the demographic identifier "COHORT_ID"
    df[COHORT_ID] = df[var_list].apply(lambda x: "_".join(x.astype(str)), axis=1)
    return df

# Container functions
def add_variables(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add several sets of variables to the cleaned CPS data.
    
    Parameters:
        data_df (pd.DataFrame): The cleaned CPS data.
        
    Returns:
        pd.DataFrame: The cleaned CPS data with the child-related variables.
    """
    data_df = add_birth_year(data_df)
    data_df = add_is_married(data_df)
    data_df = add_child_related_variables(data_df)
    data_df = add_marriage_related_variables(data_df)
    data_df = add_cohort_id(data_df, var_list=MATCHING_VARS)
    
    return data_df

def filter_data(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the DataFrame to keep only the relevant observations.
    
    Parameters:
        data_df (pd.DataFrame): The DataFrame to filter.
        
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    age_cond = (data_df[AGE] >= 20) & (data_df[AGE] <= 55)
    child_age_cond = (data_df[AGE_OF_OLDEST_CHILD] <= 18)
    reasonable_age_cond = data_df[AGE] > (data_df[AGE_OF_OLDEST_CHILD] + 15)
    married_or_never_cond = (data_df[IS_MARRIED] == 1) | (data_df[IS_MARRIED] == 0)
    
    return data_df[age_cond & child_age_cond & reasonable_age_cond & married_or_never_cond]

def prepare_dataframe(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add variables and filter the DataFrame.
    
    Parameters:
        data_df (pd.DataFrame): The DataFrame to prepare.
        
    Returns:
        pd.DataFrame: The prepared DataFrame.
    """    
    return filter_data(add_variables(data_df))

# Main function
def main() -> None:
    # Create the directory for the child-related CPS data
    CPS_DATA_CHILD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all cleaned CPS data files
    cleaned_data_files = list(CPS_DATA_CLEANED_DIR.glob("*.csv"))
    cleaned_data_files.sort()
    
    # Loop over all cleaned CPS data files
    for cleaned_data_file in tqdm(cleaned_data_files, desc="Adding child-related variables"):
        child_data_file = CPS_DATA_CHILD_DIR / cleaned_data_file.name
        child_data_df = prepare_dataframe(load_data(cleaned_data_file))
        child_data_df.to_csv(child_data_file, index=False)

        if "199403" in cleaned_data_file.name:
            break # for testing purposes
    
    print("Child-related variables added to the CPS data.")
    
if __name__ == "__main__":
    main()