from pathlib import Path

# Define the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Define the directories for the CPS data
RAW_CPS_DATA_DIR = RAW_DIR / "cps_data"
CPS_DATA_GZ_DIR = RAW_CPS_DATA_DIR / "gz"
CPS_DATA_FW_DIR = RAW_CPS_DATA_DIR / "fixedwidth"
CPS_DATA_CSV_DIR = RAW_CPS_DATA_DIR / "csv"

PROCESSED_CPS_DATA_DIR = PROCESSED_DIR / "cps_data"
CPS_DATA_CLEANED_DIR = PROCESSED_CPS_DATA_DIR / "cleaned"
CPS_DATA_CHILD_DIR = PROCESSED_CPS_DATA_DIR / "child"

# Define the directories for the CPS dictionary
RAW_CPS_DICT_DIR = RAW_DIR / "cps_dict"
CPS_DICT_TXT_DIR = RAW_CPS_DICT_DIR / "txt"
CPS_DICT_CSV_DIR = RAW_CPS_DICT_DIR / "csv"
CPS_DICT_DCT_DIR = RAW_CPS_DICT_DIR / "dct"

# Define the URLs for the CPS data and dictionary
CPS_DATA_URL_TEMPLATE = "https://www2.census.gov/programs-surveys/cps/datasets/{year_int4}/basic/{mon_str3}{year_int2}pub.dat.gz"
CPS_DICT_URL_LIST = [
    "https://www2.census.gov/programs-surveys/cps/datasets/2024/basic/2024_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2023/basic/2023_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2022/basic/2022_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2021/basic/2021_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2020/basic/2020_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt",
    
    "https://www2.census.gov/programs-surveys/cps/datasets/2017/basic/January_2017_Record_Layout.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2015/basic/January_2015_Record_Layout.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2014/basic/January_2014_Record_Layout.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2013/basic/January_2013_Record_Layout.txt",
    
    "https://www2.census.gov/programs-surveys/cps/datasets/2012/basic/may12dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2010/basic/jan10dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2009/basic/jan09dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2007/basic/jan07dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2005/basic/augnov05dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2004/basic/may04dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2003/basic/jan03dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/2002/basic/jan98dd.asc",
    
    "https://www2.census.gov/programs-surveys/cps/datasets/1997/basic/sep95_dec97_dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/1995/basic/jun95_aug95_dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/1995/basic/apr94_may95_dd.txt",
    "https://www2.census.gov/programs-surveys/cps/datasets/1994/basic/jan94_mar94_dd.txt",
]
CPS_DICT_STARTTIME_LIST = [
    "202401", "202301", "202201", "202101", "202001", 
    "201701", "201501", "201401", "201301",
    "201205", "201001", "200901", "200701", "200508", "200405", "200301", "199801",
    "199509", "199506", "199404", "199401"
]

# Define the file paths for the CPS dictionary
CPS_DICT_TXT_LIST = [CPS_DICT_TXT_DIR / f"cps_dict_{start_time}.txt" for start_time in CPS_DICT_STARTTIME_LIST]
CPS_DICT_CSV_LIST = [CPS_DICT_CSV_DIR / f"cps_dict_{start_time}.csv" for start_time in CPS_DICT_STARTTIME_LIST]
CPS_DICT_DCT_LIST = [CPS_DICT_DCT_DIR / f"cps_dict_{start_time}.dct" for start_time in CPS_DICT_STARTTIME_LIST]

# Define the file paths for the parsed CPS data
MANUAL_CLEAN_CPS_DICT_CSV_LIST = [
    CPS_DICT_CSV_DIR / "cps_dict_199509.csv",
    CPS_DICT_CSV_DIR / "cps_dict_199506.csv",
    CPS_DICT_CSV_DIR / "cps_dict_199404.csv",
    CPS_DICT_CSV_DIR / "cps_dict_199401.csv"
]




# Define variables in the datasets
HOUSEHOLD_ID = "HRHHID"
PERSON_NUM = "HUHHNUM"

DATA_YEAR = "DATA_YEAR"
BIRTH_YEAR = "BIRTH_YEAR"
AGE = "PEAGE"
RELATIONSHIP = "PRFAMREL"

HAS_CHILD = "HAS_CHILD"
IS_REF_OR_SPOUSE = "IS_REF_OR_SPOUSE"
IS_CHILD = "IS_CHILD"
IS_OLDEST_CHILD = "IS_OLDEST_CHILD"

AGE_OF_OLDEST_CHILD = "AGE_OF_OLDEST_CHILD"
MARRITAL_STATUS = "PEMARITL"
IS_MARRIED = "IS_MARRIED"
MARRIAGE_TIMES = "MARRIAGE_TIMES"