# Data_Processing_and_Pipelining_Project

This is a mini project, based on Automated data collection, cleaning, and storage pipeline for monitoring reports from the Himachal Pradesh Treasury portal.

## Table of Contents

- [Description](#description)
- [Folder Structure](#folder-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description
This repository hosts a data pipeline that automates the process of monitoring reports from the Himachal Pradesh Treasury portal. The pipeline collects data for a specified date range and report type, cleans the data, and stores it in an SQLite database. This README provides an overview of the project and instructions for its setup and usage.

## Folder Structure

The project's folder structure is organized as follows:

- `dll_data_cleaningand_aqlite.py`: This file contains python scripts for data cleaning and to store the processed data in a SQLite database.
- `dll_pipeline.py`: This file contains python script for defining the tasks within the data pipeline.
- `dll_records.xls`: Excel spreadsheet for the collected data in spreadsheet format.
- `data.db`: SQLite database file.
- `README.md` : This documentation file.
Snippets folder contains some screenshot of code execution

## Dependencies

- pandas
- sqlite3
- prefect


### Running Python Scripts on Google Colab

1. Open Google Colab.
2. Upload the Python scripts (`dll_data_cleaningand_aqlite.py` and `dll_pipeline.py`) to your Colab workspace.
3. Open each script in Colab and follow the instructions within the script comments.

### Using the Excel Spreadsheet

- Upload the dll_records.xls folder in google collab 


### Using the SQLite Database

A SQLite database file will automatically get formed once the 2 code blocks of sqlite connections are runned


