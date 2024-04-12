from pathlib import Path
from typing import List
import re
import pandas as pd
from config import CPS_DICT_FILE_LIST, PARSED_DICT_DIR, PARSED_DICT_FILE_LIST

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
        
    return lines

def extract_dict_text_to_df(lines: List[str], dict_type: str="normal") -> pd.DataFrame:
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
    
    # Extract var_name, var_len, desc, start_pos, and end_pos
    if dict_type == "normal":
        for line in lines:
            pattern = r"(\w+\d?)\s+(\d+)\s+(.+?)\s+\(?(\d+)\s*-\s*(\d+)\)?\s*$"
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
    elif dict_type == "1998":
        for line in lines:
            # D HETELAVL    2     35
            pattern = r"D\s+(\w+\d?)\s+(\d+)\s+(\d+)"
            match = re.match(pattern, line)
            if match:
                var_name, var_len, start_pos = match.groups()
                df = df._append({
                    "var_name": var_name,
                    "var_len": int(var_len),
                    "desc": "",
                    "start_pos": int(start_pos),
                    "end_pos": int(start_pos) + int(var_len) - 1
                }, ignore_index=True)
            else:
                Warning(f"Pattern not matched: {line}")
    else:
        raise ValueError(f"Invalid dict_type: {dict_type}, should be 'normal' or '1998'.")
            
    return df

def parse_dict_file_normal(dict_file: Path) -> None:
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

    # Save the parsed dictionary file
    PARSED_DICT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PARSED_DICT_DIR / f"{dict_file.stem}.csv", index=False)

def parse_dict_file_1998(dict_file: Path) -> None:
    """
    Parse the 1998 CPS dictionary file and save the parsed CSV file.
    
    Returns
    -------
    None
    """
    # Load the file as text
    text = dict_file.read_text()
    
    # Filter lines that match the pattern (lines start with "D ")
    filtered_lines = [line for line in text.split("\n") if line.startswith("D ")]
    print(f"In {dict_file.stem}, {len(filtered_lines)} variables are found.")
    
    # Extract the variable name, start position, and length
    df = extract_dict_text_to_df(filtered_lines, dict_type="1998")
    
    # Save the parsed dictionary file
    PARSED_DICT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PARSED_DICT_DIR / f"{dict_file.stem}.csv", index=False)

def main() -> None:
    """
    Parse the CPS dictionary files and save the parsed CSV files.
    """
    for file in CPS_DICT_FILE_LIST:
        if "199801" in file.stem:
            parse_dict_file_1998(file)
        else:
            parse_dict_file_normal(file)

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
            else:
                assert(row["start_pos"] == 1, f"{file.stem} does not start from 1.")
        
        print(f"{file.stem} is validated.")

def csv_to_dct(csv_file_path: str, output_file_path: str, str_vars: List[str] = []):
    """
    Reads a CSV file with variable specifications and writes a .dct file.
    
    Parameters:
        csv_file_path (str): Path to the CSV file containing the variable definitions.
        output_file_path (str): Path where the .dct file will be saved.
        str_vars (List[str]): List of variable names that should be treated as strings.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Open the output .dct file and begin writing
    with open(output_file_path, 'w') as file:
        file.write('infix dictionary {\n')
        
        # Iterate over rows in DataFrame
        for index, row in df.iterrows():
            var_name = row['var_name']
            var_len = row['var_len']
            start_pos = row['start_pos']
            end_pos = row['end_pos']
            
            # Determine if the variable should be treated as a string
            if var_name in str_vars:
                text = f'    str {var_name} {start_pos}-{end_pos}\n'
            else:
                text = f'    {var_name} {start_pos}-{end_pos}\n'
            
            file.write(text)
        
        file.write('}\n')

def convert_all_csv_to_dct() -> None:
    """
    Convert all parsed dictionary files to .dct files.
    """
    for file in PARSED_DICT_FILE_LIST:
        output_file = file.with_suffix(".dct")
        csv_to_dct(file, output_file, str_vars=[])
        print(f"{output_file.stem} is converted to dct file.")

if __name__ == "__main__":
    main()
    validate_parsed_dict()
    convert_all_csv_to_dct()
    