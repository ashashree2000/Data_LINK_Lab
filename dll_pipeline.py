# -*- coding: utf-8 -*-
"""DLL_pipeline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ED1a5ZI5xonBSeHekxhCg_vZ5X7jL2dW
"""

pip install prefect==1.0.0

import prefect
from prefect import task, Flow

import pandas as pd
import sqlite3

@task
def load_raw_data():
    pl_data = pd.read_excel('dll_records.xls')
    return pl_data

@task
def fill_blank_cells(cleaned_data):
    cleaned_data['DmdCd'].fillna(method='ffill', inplace=True)
    return cleaned_data

@task
def drop_total_rows(pl_data):
    cleaned_data = pl_data[~(pl_data['HOA'].str.contains('Total') | pl_data['DmdCd'].str.contains('Total'))]
    return cleaned_data

@task
def split_dmdcd(cleaned_data):
    cleaned_data[['DemandCode', 'Demand']] = cleaned_data['DmdCd'].str.split('-', 1, expand=True)
    return cleaned_data

@task
def split_hoa(cleaned_data):
    cleaned_data[['MajorHead', 'SubMajorHead', 'MinorHead', 'SubMinorHead', 'DetailHead',
                  'SubDetailHead', 'BudgetHead', 'PlanNonPlan', 'VotedCharged', 'StatementofExpenditure']] = cleaned_data['HOA'].str.split('-', 9, expand=True)

    cleaned_data.drop(['HOA', 'DmdCd'], axis=1, inplace=True)
    return cleaned_data

@task
def store_data_in_database(cleaned_data):
    conn = sqlite3.connect('mydatabase.db')
    cleaned_data.to_sql('cleaned_data', conn, if_exists='replace', index=False)
    conn.close()

with Flow("data_cleaning_pipeline") as flow:
    pl_data = load_raw_data()
    cleaned_data = fill_blank_cells(pl_data)
    cleaned_data = drop_total_rows(cleaned_data)
    cleaned_data = split_dmdcd(cleaned_data)
    cleaned_data = split_hoa(cleaned_data)
    store_data_in_database(cleaned_data)

flow.run()