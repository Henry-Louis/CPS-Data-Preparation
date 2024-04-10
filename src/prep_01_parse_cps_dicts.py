from pathlib import Path
from typing import List
import re
import pandas as pd
from config import CPS_DICT_FILE_LIST, PARSED_DICT_DIR, PARSED_DICT_FILE_LIST

def parse_cps_dict(dict_file: Path, dict_type: str="normal") -> pd.DataFrame:
    """
    Parse the CPS dictionary file into a DataFrame, extracting the variable name, start position, and length.
    Parameters
    ----------
    dict_file : Path
        The path to the CPS dictionary file.
    dict_type : str, optional. Default is "normal".
        The type of file to parse. Options are "normal" or "1998". The format for the 1998 file is different.
    """
    pass

def get_main_content(text: str) -> str:
    """
    Get the main content of the CPS dictionary file.
    Parameters
    ----------
    text : str
        The text content of the CPS dictionary file.
    Returns
    -------
    str
        The main content of the CPS dictionary file.
    """
    end_tokens = "END OF BASIC PORTION OF THE RECORD"
    if end_tokens in text:
        return text.split(end_tokens)[0]
    return text

def get_relevant_lines(text: str) -> List[str]:
    """
    Get the relevant lines from the CPS dictionary file.
    Parameters
    ----------
    text : str
        The text content of the CPS dictionary file.
    Returns
    -------
    List[str]
        A list of relevant lines.
    """
    # line starts with at least 2 capital letters
    line_pattern = r"^[A-Z]{2,}.* \(?\d+ *-? ?\d+\)? *$"
    lines = [line for line in text.split("\n") if re.match(line_pattern, line)]
    
    # if len(lines) <= 10:
    #     line_pattern = r"^[A-Z]{2,}.* \d+ *-? ?*$"
    #     lines = [line for line in text.split("\n") if re.match(line_pattern, line)]
        
    return lines

def extract_dict_text_to_df(lines: List[str]) -> pd.DataFrame:
    """
    Extract the variable name, start position, and length from the relevant lines.
    Parameters
    ----------
    lines : List[str]
        A list of relevant lines.
    Returns
    -------
    pd.DataFrame
        A DataFrame containing var_name, var_len, desc, start_pos and end_pos.
    """
    # Initialize a df to store the results
    df = pd.DataFrame(columns=["var_name", "var_len", "desc", "start_pos", "end_pos"])
    
    # Define a new pattern to extract the variable name, length, and description
    for line in lines:
        pattern = r"(\w+)\s+(\d+)\s+(.+?)\s+\(?(\d+)\s*-\s*(\d+)\)?\s*$"
        match = re.match(pattern, line)
        if match:
            var_name, var_len, desc, start_pos, end_pos = match.groups()
            df = df._append({
                "var_name": var_name,
                "var_len": int(var_len),
                "desc": desc,
                "start_pos": int(start_pos),
                "end_pos": int(end_pos)
            }, ignore_index=True)
        else:
            Warning(f"Pattern not matched: {line}")
            
    return df

def parse_dict_text_to_df(dict_file: Path) -> pd.DataFrame:
    """
    Parse a normal CPS dictionary file, filtering lines that match a specific pattern
    of variable names and positions.
    
    Parameters
    ----------
    dict_file : Path
        The path to the CPS dictionary file, should be read as text.
    
    Returns
    -------
    pd.DataFrame
        A DataFrame containing var_name, var_len, desc, start_index.
    """
    # Load the file as text
    text = dict_file.read_text()
    text = get_main_content(text)
    
    # Filter lines that match the pattern
    filtered_lines = get_relevant_lines(text)
    print(f"In {dict_file.stem}, {len(filtered_lines)} variables are found.")
    
    # Extract the variable name, start position, and length
    df = extract_dict_text_to_df(filtered_lines)

    return df

def parse_cps_dict_normal():
    """
    Parse all normal CPS dictionary files.
    
    Returns
    -------
    None
    """
    for file in CPS_DICT_FILE_LIST:
        if file.stem == "cps_dict_199801": # Skip the 1998 file
            print(f"Skip {file.stem}, since it is not a normal file.")
            continue
        
        # Parse the dictionary file
        df = parse_dict_text_to_df(file)
        
        # Save the parsed dictionary file
        PARSED_DICT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(PARSED_DICT_DIR / f"{file.stem}.csv", index=False)

def parse_cps_dict_1998(dict_file: Path) -> pd.DataFrame:
    """
    Parse a CPS dictionary file from 1998.
    Parameters
    ----------
    dict_file : Path
        The path to the CPS dictionary file.
    """
    pass

def validate_parsed_dict() -> None:
    """
    Validate the parsed dictionary files.
    """
    # Load the parsed dictionary files
    for file in PARSED_DICT_FILE_LIST:
        if not file.exists():
            Warning(f"{file.stem} does not exist.")
            continue
        df = pd.read_csv(file)
        assert(df.shape[0] > 0, f"{file.stem} is empty.")
        assert(df["var_len"].sum() == 0, f"{file.stem} has empty variable.")
        for i, row in df.iterrows():
            if i != 0: # Check for if all variables are next to each other
                assert(row["start_pos"] == df.loc[i-1, "end_pos"] + 1, f"{file.stem} has overlapping variables.")
        
        print(f"{file.stem} is validated.")

if __name__ == "__main__":
    parse_cps_dict_normal()
    validate_parsed_dict()