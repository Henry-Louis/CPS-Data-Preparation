from config import CPS_DATA_FW_DIR

def subset_cps_datasets():
    """
    Subset the CPS datasets.
    """
    # Load the unparsed CPS datasets
    cps_data_unparsed_files = [file for file in CPS_DATA_FW_DIR.glob("*") if "subsets" not in file.parts]
    for file in cps_data_unparsed_files:
        # Load the first 5 lines and save with a new name (via line method)
        with open(file, "r") as f:
            new_file = file.parent / "subsets" / f"{file.stem}_subset{file.suffix}"
            new_file.parent.mkdir(parents=True, exist_ok=True)
            with open(new_file, "w") as f_new:
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
                    f_new.write(line)
    
    print("Subsetting is done.")
                
if __name__ == "__main__":
    subset_cps_datasets()