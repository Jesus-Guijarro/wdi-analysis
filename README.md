# World Development Indicators Analysis

A Jupyter-based project for exploring the World Development Indicators (WDI) dataset using PySpark. This repository provides scripts and notebooks to load, filter, and perform basic exploratory analysis on WDI data for selected countries and indicators.


## ⚙️Installation and Configuration

**Prerequisites**
- JDK 17
- Spark 4.X
- Python 3.12.X


1. Clone the repository
```sh
git clone https://github.com/Jesus-Guijarro/wdi-analysis.git
cd wdi-analysis
```
2. Create and activate a virtual environment

```sh
python3 -m venv wdi-venv

source wdi-venv/bin/activate        # on Linux/macOS
wdi-venv\Scripts\activate.bat       # on Windows
```

3. Install dependencies

```sh
pip3 install -r requirements.txt
```
4. Download and transform WDI data

```sh
python3 get_WDI_data.py
```
A `data` folder should appear with the CSV files: `Countries.csv`, `Data.csv` ,and `Indicators.csv`.


- Final Project Structure
```
📂 wdi-analysis
├── 📂 data
│   ├── 📄 Countries.csv
│   ├── 📄 Data.csv
│   └── 📄 Indicators.csv
├── 📂 wdi-env
├── 📒 data_analysis.ipynb
├── 📒 data_exploration.ipynb
├── 🚫 .gitignore
├── 📜 LICENSE
├── 📄 README.md
└── 📄 requirements.txt
```


## 🚀Running the Project

Open each notebook and click on `Run All`.

## 🛠Technologies Used

- Language: Python
- Data Processing: Apache Spark (PySpark)
- Data Visualization: matplotlib

## 🔜Future improvements

- Improve data visualization quality and interactivity.

## 📜License
This project is open source under the MIT License. See the LICENSE file for details.