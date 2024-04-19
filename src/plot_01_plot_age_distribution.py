from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import CPS_DATA_CHILD_DIR, PLOT_DIR
from variable_typing import *

def plot_age_frequency(age_var: str, group_var: str, data: pd.DataFrame, plot_dir: Path) -> None:
    """
    Plot the frequency of age groups for each group of having children or not.

    Parameters:
    - x: list or array of x-axis values
    - y: list or array of y-axis values
    - labels: list of labels for each data series

    Returns:
    - None
    """
    fig, ax = plt.subplots()
    sns.histplot(data=data, x=age_var, hue=group_var, multiple="stack", ax=ax, bins=len(data[age_var].unique()))
    plt.title(f"Distribution of Age by Having Children or Not")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    
    plot_path = plot_dir / "age_distribution.png"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_path)

if __name__ == "__main__":
    df = pd.read_csv(list(CPS_DATA_CHILD_DIR.glob("*.csv"))[0])
    plot_age_frequency(AGE, HAS_CHILD, df, PLOT_DIR)
