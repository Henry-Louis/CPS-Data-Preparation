from pathlib import Path
from typing import List
import re
import pandas as pd
from config import (CPS_DICT_TXT_LIST, CPS_DICT_CSV_LIST, CPS_DICT_DCT_DIR, 
                    MANUAL_CLEAN_CPS_DICT_CSV_LIST, CPS_DICT_CSV_DIR)

# Parsing-related functions
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
    line_pattern = r"^[A-Z]{2,}.*\(?\d+ *-? ?\d+\)?\s*$"
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
    if dict_type == "normal": # normal CPS dictionary
        # Loop through the lines
        for line in lines:
            # Extract the variable name, start position, and length
            pattern = r"(\w+\d?)\s+(\d+)\s+(.+?)\s+\(?(\d+)\s*[-]{1}\s*(\d+)\)?\s*$"
            match = re.match(pattern, line)
                
            # If the pattern matches, append the results to the DataFrame
            if match:
                var_name, var_len, desc, start_pos, end_pos = match.groups()
                df = df._append({
                    "var_name": var_name,
                    "var_len": int(var_len),
                    "desc": desc,
                    "start_pos": int(start_pos),
                    "end_pos": int(end_pos)
                }, ignore_index=True)
                
            # If the pattern does not match, print a warning
            else:
                Warning(f"Pattern not matched: {line}")
                
    elif dict_type == "1998": # 1998 CPS dictionary
        # Loop through the lines
        for line in lines:
            # Extract the variable name, start position, and length
            pattern = r"D\s+(\w+\d?)\s+(\d+)\s+(\d+)"
            match = re.match(pattern, line)
            
            # If the pattern matches, append the results to the DataFrame
            if match:
                var_name, var_len, start_pos = match.groups()
                df = df._append({
                    "var_name": var_name,
                    "var_len": int(var_len),
                    "desc": "",
                    "start_pos": int(start_pos),
                    "end_pos": int(start_pos) + int(var_len) - 1
                }, ignore_index=True)
            
            # If the pattern does not match, print a warning
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
    CPS_DICT_CSV_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CPS_DICT_CSV_DIR / f"{dict_file.stem}.csv", index=False)

def parse_dict_file_1998(dict_file: Path) -> None:
    """
    Parse the 1998 CPS dictionary file and save the parsed CSV file.
    """
    # Load the file as text
    text = dict_file.read_text()
    
    # Filter lines that match the pattern (lines start with "D ")
    filtered_lines = [line for line in text.split("\n") if line.startswith("D ")]
    print(f"In {dict_file.stem}, {len(filtered_lines)} variables are found.")
    
    # Extract the variable name, start position, and length
    df = extract_dict_text_to_df(filtered_lines, dict_type="1998")
    
    # Save the parsed dictionary file
    CPS_DICT_CSV_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CPS_DICT_CSV_DIR / f"{dict_file.stem}.csv", index=False)

# Manually clean the parsed dictionary CSV files
def manually_clean_parsed_dict() -> None:
    """
    Manually clean the parsed dictionary files.
    """
    # Load the targeted parsed dictionary files
    for file in MANUAL_CLEAN_CPS_DICT_CSV_LIST:
        df = pd.read_csv(file)
        # Deal with variable "PXFNTVTY" (start_pos: 794 -> 679)
        if df.loc[df["var_name"] == "PXFNTVTY", "start_pos"].values[0] == 794:
            df.loc[df["var_name"] == "PXFNTVTY", "start_pos"] = 679
        
        # Deal with variable "PEAFNOW" (var_len: 2 -> 3)
        if not file.parts[-1] == "cps_dict_199509.csv": # 199509 is good for PEAFNOW
            if df.loc[df["var_name"] == "PEAFNOW", "var_len"].values[0] == 2:
                df.loc[df["var_name"] == "PEAFNOW", "var_len"] = 3
            
        # Save the cleaned parsed dictionary file
        df.to_csv(file, index=False) # overwrite the original file
        print(f"{file.stem} is manually cleaned.")
    
    print("---  All parsed dictionary CSV are manually cleaned.  ---\n")

# Validate the parsed dictionary CSV files
def validate_parsed_dict() -> None:
    """
    Validate the parsed dictionary files.
    """
    # Load the parsed dictionary files
    for file in CPS_DICT_CSV_LIST:
        if not file.exists():
            Warning(f"{file.stem} does not exist.")
            continue
        df = pd.read_csv(file)
        if df.shape[0] == 0:
            raise AssertionError(f"{file.stem} is empty.")
        # Check row by row
        for index, row in df.iterrows():
            var_name = row["var_name"]
            start_pos = row["start_pos"]
            end_pos = row["end_pos"]
            # Check var_len
            if row["end_pos"] - row["start_pos"] + 1 != row["var_len"]:
                # print(row["end_pos"], row["start_pos"], row["var_len"])
                if "FILLER" in var_name:
                    pass
                else:
                    print(f"{file.stem} has an invalid var_len at line {index} ({var_name}).")
            # Check start_pos and end_pos
            if start_pos > end_pos:
                if var_name == "PXFNTVTY":
                    print(f"{file.stem} has a PXFNTVTY variable with wrong position ({start_pos}, {end_pos}) at line {index}.")
                else:
                    raise AssertionError(f"{file.stem} has an invalid start_pos and end_pos at line {index} ({var_name}).")
            # Check the start_pos and end_pos between rows
            missing_var_list = []
            if index > 0:
                if row["start_pos"] != df.loc[index - 1, "end_pos"] + 1:
                    if "FILLER" in var_name:
                        pass
                    else:
                        missing_var_list.append(var_name)
            else:
                if row["start_pos"] != 1:
                    raise AssertionError(f"{file.stem} does not start from 1.")
                
        # Print the missing variable count
        if len(missing_var_list) > 0:
            print(f"{file.stem} has {len(missing_var_list)} missing variables.")
            print(missing_var_list)
        
        print(f"{file.stem} is validated.")
    
    print("---  All parsed dictionary CSV are validated.  ---\n")

# Convert the parsed dictionary CSV files to DCT files
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
    CPS_DICT_DCT_DIR.mkdir(parents=True, exist_ok=True)
    for file in CPS_DICT_CSV_LIST:
        output_file = CPS_DICT_DCT_DIR / f"{file.stem}.dct"
        csv_to_dct(file, output_file, str_vars=[])
        print(f"{output_file.stem} is converted to dct file.")
    
    print("---  All parsed dictionary CSV are converted to DCT.  ---\n")
    
# Main function
def main() -> None:
    """
    Parse the CPS dictionary files and save the parsed CSV files,
    manually clean the parsed dictionary files, validate the parsed dictionary files,
    and convert the parsed dictionary files to .dct files.
    """
    # Parse the dictionary files
    for file in CPS_DICT_TXT_LIST:
        if "199801" in file.stem:
            parse_dict_file_1998(file)
        else:
            parse_dict_file_normal(file)
    print("---  All CPS dictionary TXT are parsed into CSV.  ---\n")
    
    # Manually clean the parsed dictionary files
    manually_clean_parsed_dict()
    
    # Validate the parsed dictionary files     
    validate_parsed_dict()
    
    # Convert the parsed dictionary files to .dct files
    convert_all_csv_to_dct()

if __name__ == "__main__":
    main()
    
    