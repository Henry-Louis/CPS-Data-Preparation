from typing import List
import pandas as pd
from config import CPS_DATA_MERGED_FILE, CPS_DATA_PSEUDO_DIR
from variable_typing import *

def drop_non_matched_observations(df: pd.DataFrame, cohort_id: str, treatment_var: str) -> pd.DataFrame:
    """
    Group the dataset into 2 by the treatment variable, and drop the unmatched observations.
    
    Parameters:
        df (pd.DataFrame): The dataset.
        cohort_id (str): The cohort ID variable.
        treatment_var (str): The treatment variable.
        
    Returns:
        pd.DataFrame: The dataset with the unmatched observations dropped.
    """
    treatment_group = df[df[treatment_var] == 1]
    control_group = df[df[treatment_var] == 0]
    intersect_cohort_ids = set(treatment_group[cohort_id]).intersection(set(control_group[cohort_id]))
    
    return df[df[cohort_id].isin(intersect_cohort_ids)]

def get_pseudo_control_group(df: pd.DataFrame, cohort_id: str, treatment_var: str) -> pd.DataFrame:
    """
    Get the pseudo control group by matching the new parent observations with the original dataset.
    
    Parameters:
        df (pd.DataFrame): The dataset.
        cohort_id (str): The cohort ID variable.
        treatment_var (str): The treatment variable, should be HAS_CHILD.
        
    Returns:
        pd.DataFrame: The pseudo control group.
    """
    # Keep only control group
    df = df[df[treatment_var] == 0]
    
    # Sort data for consistency
    df.sort_values(by=[cohort_id, DATA_YEAR], inplace=True)

    # Function to generate IDs
    def generate_ids(group):
        occupation = group[cohort_id].iloc[0]
        year = group[DATA_YEAR].iloc[0]
        count = group.shape[0]
        group[PSEUDO_ID] = [f"{occupation}_{str(i+1).zfill(4)}" for i in range(count)]
        return group
    
    data = data.groupby([cohort_id, DATA_YEAR]).apply(generate_ids)
    
    return data

def get_new_parent_observations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the new parent observations, who have oldest child aged 0. These observations
    serve as the baseline, whose left and right will be matched and filled.
    
    Parameters:
        df (pd.DataFrame): The dataset.
        
    Returns:
        pd.DataFrame: The new parent observations.
    """
    return df[df[AGE_OF_OLDEST_CHILD] == 0]

def get_pseudo_treatment_group(new_parent_df: pd.DataFrame, complete_df: pd.DataFrame, cohort_id: str, treatment_var: str) -> pd.DataFrame:
    """
    Get the pseudo treatment group by matching the new parent observations with the original dataset.
    
    Parameters:
        new_parent_df (pd.DataFrame): The new parent observations.
        df (pd.DataFrame): The dataset.
        cohort_id (str): The cohort ID variable.
        treatment_var (str): The treatment variable.
        
    Returns:
        pd.DataFrame: The pseudo treatment group.
    """
    df = add_matched_observations_to_right(new_parent_df, complete_df, cohort_id, treatment_var)
    df = add_matched_observations_to_left(df, complete_df, cohort_id, treatment_var)
    
    return df

def add_matched_observations_to_right(new_parent_df: pd.DataFrame, complete_df: pd.DataFrame, cohort_id: str, treatment_var: str) -> pd.DataFrame:
    """
    Add the matched observations to the right of the new parent observations.
    
    Parameters:
        new_parent_df (pd.DataFrame): The new parent observations.
        complete_df (pd.DataFrame): The complete dataset.
        cohort_id (str): The cohort ID variable.
        treatment_var (str): The treatment variable.
        
    Returns:
        pd.DataFrame: The dataset with the matched observations added to the right.
    """
    # Keep only treatment group
    complete_df = complete_df[complete_df[treatment_var] == 1]
    
    # Sort data for consistency
    complete_df.sort_values(by=[cohort_id, DATA_YEAR], inplace=True)
    
    # Function to generate IDs
    def generate_ids(group):
        occupation = group[cohort_id].iloc[0]
        year = group[DATA_YEAR].iloc[0]
        count = group.shape[0]
        group[PSEUDO_ID] = [f"{occupation}_{str(i+1).zfill(4)}" for i in range(count)]
        return group
    
    complete_df = complete_df.groupby([cohort_id, DATA_YEAR]).apply(generate_ids)
    
    # Merge the new parent observations with the complete dataset
    new_parent_df = new_parent_df.merge(complete_df, on=[cohort_id, DATA_YEAR], how="left")
    
    return new_parent_df

def main() -> None:
    df = pd.read_csv(CPS_DATA_MERGED_FILE)
    df = drop_non_matched_observations(df, COHORT_ID, HAS_CHILD)
    
    # Get the pseudo control group
    pseudo_control_df = get_pseudo_control_group(df, COHORT_ID, HAS_CHILD)
    
    # Get the pseudo treatment group
    new_parent_df = get_new_parent_observations(df)
    pseudo_treatment_df = get_pseudo_treatment_group(new_parent_df, df, COHORT_ID, AGE_OF_OLDEST_CHILD)
    
    # Concatenate the pseudo control and treatment groups
    complete_pseudo_df = pd.concat([pseudo_control_df, pseudo_treatment_df])
    
    # Save the pseudo panel data
    CPS_DATA_PSEUDO_DIR.mkdir(parents=True, exist_ok=True)
    complete_pseudo_df.to_csv(CPS_DATA_PSEUDO_DIR / "cps_data_pseudo_panel.csv", index=False)


