from pathlib import Path
from typing import List
import gzip
import requests
import concurrent.futures
from config import (CPS_DATA_URL_TEMPLATE, CPS_DATA_DIR, 
                    CPS_DICT_URL_LIST, CPS_DICT_DIR, CPS_DICT_START_TIME_LIST)

# Download the CPS dictionary files
def download_file(url: str, file_path: Path) -> None:
    response = requests.get(url)
    response.raise_for_status()
    file_size = int(response.headers.get("Content-Length", 0))
    if file_size <= 1024:
        print(f"File size is {file_size} bytes, skipping download")
        return
    else:
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
    # Rename the downloaded files to match the start time of the data
    for dict_file, start_time in zip(dict_file_list, dict_start_time_list):
        new_dict_file = dict_dir / f"cps_dict_{start_time}.txt"
        if new_dict_file.exists():
            print(f"Already renamed {new_dict_file}")
        else:
            # save a new copy of the file with the new name
            with open(dict_file, "r") as f:
                with open(new_dict_file, "w") as f_new:
                    f_new.write(f.read())

# Download the CPS data files
def download_cps_data(years: List[int], months: List[str], data_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for year in years:
            for month in months:
                url = CPS_DATA_URL_TEMPLATE.format(year_int4=year, mon_str3=month, year_int2=str(year)[2:])
                month_num = str(months.index(month) + 1).zfill(2)
                data_file = data_dir / f"CPS_{year}_{month_num}.gz"
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

def extract_file(gz_file: Path, data_file: Path) -> None:
    with gzip.open(gz_file, "rb") as f_in:
        with open(data_file, "wb") as f_out:
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

# Parse the CPS data files
def parse_cps_data(data_file: Path, dict_file: Path) -> None:
    pass

def parse_cps_data_files(data_dir: Path, dict_dir: Path) -> None:
    pass

# Main function
def main() -> None:
    # Download the CPS dictionary files
    download_cps_dict(CPS_DICT_URL_LIST, CPS_DICT_DIR / "raw")
    raw_dict_file_list = [CPS_DICT_DIR / "raw" / url.split("/")[-1] for url in CPS_DICT_URL_LIST]
    rename_cps_dict_files(CPS_DICT_DIR, raw_dict_file_list, CPS_DICT_START_TIME_LIST)
    
    # Download the CPS data files
    years = range(1994, 2024+1)
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    download_cps_data(years, months, CPS_DATA_DIR / "gz")
    extract_gz_files(CPS_DATA_DIR / "gz", CPS_DATA_DIR / "unparsed")
    parse_cps_data_files(CPS_DATA_DIR / "unparsed", CPS_DICT_DIR)
    
if __name__ == "__main__":
    main()
    
