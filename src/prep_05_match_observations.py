from typing import List
import pandas as pd
from config import CPS_DATA_CHILD_DIR
from variable_typing import *

# I have cohort_id now, and I still need to
# 1. separate 2 groups: has_child==1 and has_child==0
# 2. for has_child==1, we need to match the observations
#    based on cohort_id + year_of_first_giving_birth
# 3. for has_child==0, we need to match the observations
#    based on cohort_id

def match_observations_for_has_child(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Match the observations for the family groups with children.
    
    Parameters:
        data_df (pd.DataFrame): The CPS data.
        
    Returns:
        pd.DataFrame: The CPS data with the matched observations.
    """
    return data_df