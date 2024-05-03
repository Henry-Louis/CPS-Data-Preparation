# Data Preparation for Current Population Survey Datasets

This repository houses the code and documentation for preparing and analyzing the U.S. Current Population Survey (CPS) Datasets. The project facilitates the downloading of datasets, parsing of fixed-width files, cleaning data, and constructing variables to enable comprehensive socio-economic analyses. A key objective is to construct a pseudo-panel based on the technique developed by Henrik Kleven, which allows for longitudinal studies of economic behaviors using repeated cross-sectional data.

---

## File Structure
This project is organized into several directories, each serving a specific purpose:

- **`data/`**
  - **`processed/`**: Contains cleaned and transformed data ready for analysis.
    - **`cps_data/`**
      - `cleaned/`: Cleaned data files.
      - `child/`: Data files with child-related information.
      - `merged/`: Merged data from various sources.
      - `pseudo_panel/`: Data files structured into a pseudo-panel format.
  - **`raw/`**: Original data downloaded from the source.
    - **`cps_data/`**
      - `gz/`: Compressed files downloaded directly.
      - `fixedwidth/`: Raw data in fixed-width format.
    - **`cps_dict/`**
      - `txt/`: Text files containing metadata and dictionaries.
      - `csv/`: CSV files converted from text metadata for easier processing.
- **`output/`**
  - **`plot/`**: Graphical outputs from analysis scripts.
- **`src/`**
  - `archive/`: Archive of deprecated or experimental scripts.
  - `config.py`: Configuration settings for scripts.
  - `variable_typing.py`: Definitions for variable names used in the project.
  - `download_01_cps_dictionaries_and_datasets.py`: Script for downloading CPS dictionaries and datasets.
  - `plot_01_age_distribution.py`: Generates plots for age distribution analysis.
  - `prep_01_parse_cps_dictionaries.py`: Parses CPS dictionaries to understand data formats and variable definitions.
  - `prep_02_parse_cps_datasets.py`: Parses raw CPS datasets from fixed-width format to structured data frames.
  - `prep_03_clean_str_variables.py`: Cleans string variables and handles missing or malformed data.
  - `prep_04_construct_family_related_variables.py`: Constructs variables related to family demographics.
  - `prep_05_clean_and_merge_datasets.py`: Cleans and merges datasets for comprehensive analysis.
  - `prep_06_construct_pseudo_panel.py`: Constructs a pseudo-panel using the methodology developed by Henrik Kleven for longitudinal data analysis.
  - `run_all_scripts.py`: Runs all scripts by their natural ordering.
- **`README.md`**: Provides an overview and documentation for the project.
- **`requirements.txt`**: Lists all Python libraries required to run the project scripts.


## Setup and Usage

### Prerequisites
Before you begin, ensure you have Python installed on your system. It is recommended to use Python 3.7 or newer. You can download Python from [python.org](https://www.python.org/downloads/).

### Installation
1. **Clone the repository**  
   Clone the project repository from GitHub to your local machine using the following command:
   ```bash
   git clone https://github.com/Henry-Louis/CPS-Data-Preparation.git
   cd CPS-Data-Preparation
   ```

2. **Install required packages**  
   Install the Python libraries required for this project by running:
   ```bash
   pip install -r requirements.txt
   ```

### Project Structure
The project is structured as follows:
- `output/plot/`: Contains graphical outputs from analysis scripts.
- `src/`: Includes all the Python scripts needed to run analyses.
  - `archive/`: Stores deprecated or experimental scripts.
  - Individual scripts in `src/` are used to download data, parse datasets, clean data, and generate visualizations and analyses.

### Running the Scripts
To run the scripts and perform the complete data preparation and analysis pipeline, follow these steps:
1. **Navigate to the source directory**:
   ```bash
   cd src
   ```

2. **Execute the main script**:
   ```bash
   python run_all_scripts.py
   ```

This `run_all_scripts.py` script is configured to execute all necessary scripts in their required sequence, from downloading datasets to data parsing, cleaning, and merging, followed by data analysis and visualization.

### Documentation
Each script in the `src` directory contains detailed comments explaining the functionality and usage of the script. For more detailed information about the processing steps and data handling, refer to the comments within each script.


## Contributions
### Henry Liu
Henry Liu is a Research Assistant at the ifo Institute and the University of Munich. As the main contributor to this repository, Henry brings a rich background in data science, with a specific focus on modeling human behavior using machine learning techniques. His work aims to bridge conceptual and methodological gaps between economics and machine learning communities.

### Elena Herold
Elena Herold is a Junior Economist specializing in Public and Gender Economics and a PhD Candidate at the ifo Institute within the Fiscal Policy and Taxation Research Group. As the initiator of this project, Elena's research focuses on the data preparation necessary for estimating the birth penalty in the United States, paralleling a similar investigation using German administrative data.

## Notes
1. **On the Measurement of "Number of Children"**
   It should be noted that the dataset lacks a direct variable for "number of children." Instead, we can only ascertain the number of children who reside together with their parents. This limitation explains the observed "camel-shaped" age distribution for individuals without resident children, where the prevalence is highest among those aged 30 to 45—typically when children still live at home—and declines as children reach adulthood and establish separate residences. Thus, the available data more accurately reflects "number of children living together" rather than the total number of children, serving as a proximate measure.

2. **Validity of the Pseudo Panel**
   The efficacy and validity of the pseudo panel constructed for this research are yet to be conclusively established. Researchers who prefer alternative methodologies may opt to disregard the pseudo panel approach in their analyses.


## License
```
MIT License

Copyright (c) 2023 Henry Liu, Elena Herold

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
