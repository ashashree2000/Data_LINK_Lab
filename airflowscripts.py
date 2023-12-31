# -*- coding: utf-8 -*-
"""airflowscripts.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DufX64aN6XNpu-YrRPd2vGa99sLYq5n0
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


dag = DAG(
    'data_cleaning_pipeline',
    start_date=datetime(2023, 9, 25),
    schedule_interval=None
)

def load_raw_data():
    pl_data = pd.read_excel('dll_records.xls')
    return pl_data

def fill_blank_cells(cleaned_data):
    cleaned_data['DmdCd'].fillna(method='ffill', inplace=True)
    return cleaned_data

def drop_total_rows(pl_data):
    #cleaned_data = pl_data[~(pl_data['HOA'].str.contains('Total') | pl_data['DmdCd'].str.contains('Total'))]
    cleaned_data = pl_data[ (pl_data['HOA'].str.contains('Total')) | (pl_data['DmdCd'].str.contains('Total')) ].index
    pl_data.drop(cleaned_data , inplace=True)
    return cleaned_data

def split_dmdcd(cleaned_data):
    cleaned_data[['DemandCode', 'Demand']] = cleaned_data['DmdCd'].str.split('-', 1, expand=True)
    return cleaned_data

def split_hoa(cleaned_data):
    cleaned_data[['MajorHead', 'SubMajorHead', 'MinorHead', 'SubMinorHead', 'DetailHead',
                   'SubDetailHead', 'BudgetHead', 'PlanNonPlan', 'VotedCharged', 'StatementofExpenditure']] = cleaned_data['HOA'].str.split('-', 9, expand=True)

    cleaned_data.drop(['HOA', 'DmdCd'], axis=1, inplace=True)
    return cleaned_data

#storing in sqlite database
def store_data_in_database(cleaned_data):
    conn = sqlite3.connect('cleaned_data.db')
    cleaned_data.to_sql('cleaned_data', conn, if_exists='replace', index=False)
    conn.close()

# tasks for each step
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_raw_data,
    dag=dag
)

fill_blank_cells_task = PythonOperator(
    task_id='fill_blank_cells',
    python_callable=fill_blank_cells,
    dag=dag
)

drop_total_rows_task = PythonOperator(
    task_id='drop_total_rows',
    python_callable=drop_total_rows,
    dag=dag
)

split_dmdcd_task = PythonOperator(
    task_id='split_dmdcd',
    python_callable=split_dmdcd,
    dag=dag
)

split_hoa_task = PythonOperator(
    task_id='split_hoa',
    python_callable=split_hoa,
    dag=dag
)

store_data_task = PythonOperator(
    task_id='store_data_in_database',
    python_callable=store_data_in_database,
    dag=dag

)


#execution order of tasks
load_data_task >> fill_blank_cells_task >> drop_total_rows_task >> split_dmdcd_task >> split_hoa_task >> store_data_task.