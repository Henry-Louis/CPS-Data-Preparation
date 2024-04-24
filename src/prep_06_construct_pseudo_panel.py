from typing import List
import pandas as pd
from config import CPS_DATA_MERGED_CSV, CPS_DATA_PSEUDO_CSV
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

def make_potential_observations_for_non_parents(df: pd.DataFrame, treatment_timing: str) -> pd.DataFrame:
    """
    Replicate the observations with AGE_OF_OLDEST_CHILD == -1 to [-1, -5] to make potential
    observations for non-parents. Essentially, we are assuming the non-parents could potentially
    have children in the future from 1 to 5 years.
    
    Parameters:
        df (pd.DataFrame): The dataset.
        treatment_timing (str): The treatment timing variable.
    
    Returns:
        pd.DataFrame: The dataset with potential observations for non-parents.
    """
    non_parent_df = df[df[treatment_timing] == -1]
    parent_df = df[df[treatment_timing] >= 0]
    
    # Replicate the observations
    non_parent_df_list = []
    for i in range(1, 6):
        non_parent_df_copy = non_parent_df.copy()
        non_parent_df_copy[treatment_timing] = -i
        non_parent_df_list.append(non_parent_df_copy)
        
    df = pd.concat([parent_df,] + non_parent_df_list)
    
    return df

def main() -> None:
    df = pd.read_csv(CPS_DATA_MERGED_CSV)
    df = drop_non_matched_observations(df, COHORT_ID, HAS_CHILD)
    df = make_potential_observations_for_non_parents(df, COHORT_ID, AGE_OF_OLDEST_CHILD)
    
    # Save the dataset
    CPS_DATA_PSEUDO_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CPS_DATA_PSEUDO_CSV, index=False)
    
if __name__ == "__main__":
    main()