from pathlib import Path
from typing import List
import shutil
import gzip
import requests
import concurrent.futures
from config import (CPS_DATA_URL_TEMPLATE, RAW_CPS_DATA_DIR, 
                    CPS_DICT_URL_LIST, CPS_DICT_TXT_DIR, CPS_DICT_STARTTIME_LIST)

# Download the CPS dictionary files
def download_file(url: str, file_path: Path) -> None:
    response = requests.get(url)
    response.raise_for_status()
    file_size = int(response.headers.get("Content-Length", 0))
    if file_size <= 1024:
        print(f"File size is {file_size} bytes, skipping download")
        return
    else:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(response.content)

def download_cps_dict(dict_url_list: List[str], dict_dir: Path):
    dict_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in dict_url_list:
            dict_file = dict_dir / url.split("/")[-1]
            if dict_file.exists():
                print(f"Already downloaded {dict_file}")
            else:
                print(f"Downloading {dict_file}")
                futures.append(executor.submit(download_file, url, dict_file))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

def rename_cps_dict_files(dict_dir: Path, dict_file_list: List[Path], dict_start_time_list: List[str]) -> None:
    """
    Renames the downloaded dictionary files to match the start time of the data.

    Args:
        dict_dir (Path): The directory where dictionary files are located.
        dict_file_list (List[Path]): A list of paths to the dictionary files.
        dict_start_time_list (List[str]): A list of start times corresponding to each dictionary file.
    """
    for dict_file, start_time in zip(dict_file_list, dict_start_time_list):
        new_dict_file = dict_dir / f"cps_dict_{start_time}.txt"
        if new_dict_file.exists():
            print(f"Already renamed {new_dict_file}")
        else:
            try:
                with open(dict_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Attempt to read with a different encoding if UTF-8 fails
                with open(dict_file, "r", encoding="ISO-8859-1") as f:
                    content = f.read()

            with open(new_dict_file, "w", encoding="utf-8") as f_new:
                f_new.write(content)
            
            # delete the original file
            dict_file.unlink()

# Download the CPS data files
def download_cps_data(years: List[int], months: List[str], data_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for year in years:
            for month in months:
                url = CPS_DATA_URL_TEMPLATE.format(year_int4=year, mon_str3=month, year_int2=str(year)[2:])
                month_num = str(months.index(month) + 1).zfill(2)
                data_file = data_dir / f"cps_{year}{month_num}.gz"
                if data_file.exists():
                    print(f"Already downloaded {data_file}")
                else:
                    print(f"Downloading {data_file}")
                    futures.append(executor.submit(download_file, url, data_file))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

def extract_file(gz_file: Path, output_file: Path) -> None:
    """
    Extracts the contents of a gzip-compressed file.

    Args:
        gz_file (Path): The path to the gzip file to be extracted.
        output_file (Path): The path where the extracted contents will be saved.
    """
    with gzip.open(gz_file, "rb") as f_in:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f_out:
            f_out.write(f_in.read())

def extract_gz_files(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for gz_file in input_dir.glob("*.gz"):
            data_file = output_dir / gz_file.stem
            if data_file.exists():
                print(f"Already extracted {data_file}")
            else:
                print(f"Extracting {data_file}")
                futures.append(executor.submit(extract_file, gz_file, data_file))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

# Main function
def main() -> None:
    # Download the CPS dictionary files
    download_cps_dict(CPS_DICT_URL_LIST, CPS_DICT_TXT_DIR)
    raw_dict_file_list = [CPS_DICT_TXT_DIR / url.split("/")[-1] for url in CPS_DICT_URL_LIST]
    rename_cps_dict_files(CPS_DICT_TXT_DIR, raw_dict_file_list, CPS_DICT_STARTTIME_LIST)
    
    # Download the CPS data files
    years = range(1994, 2024+1)
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    download_cps_data(years, months, RAW_CPS_DATA_DIR / "gz")
    extract_gz_files(RAW_CPS_DATA_DIR / "gz", RAW_CPS_DATA_DIR / "fixedwidth")

if __name__ == "__main__":
    main()
    
