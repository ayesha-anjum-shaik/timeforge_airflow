import yaml
import psycopg2
import pandas as pd
import numpy as np
from pmdarima.arima import auto_arima
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'ayeshashaik',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 25),
    'email': ['ayeshashaik0727@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_parameters',
    default_args=default_args,
    description='A DAG to Print the Parameters',
    schedule='@daily',
)

def ml_parameters():
    # Load the configuration file
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Access the database connection details
    db_host = config['database']['host']
    db_port = config['database']['port']
    db_name = config['database']['name']
    db_user = config['database']['user']
    db_password = config['database']['password']

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="ayeshashaik1",
        password="jw8s0F4"
    )



    # Execute the query and store the result in a pandas dataframe
    query = "SELECT * FROM store_sales"
    df = pd.read_sql(query, conn)

    #df = df.fillna(df.mean())
    df['totala'].fillna((df['totala'].mean()), inplace=True)
    df1 = df.head(100)
    # Display the first 5 rows of the dataframe
    print(df.head())

    # Convert 'belongs_to' column to datetime type
    df1['belongs_to'] = pd.to_datetime(df1['belongs_to'])

    # Set 'belongs_to' as the index and extract the 'totala' column
    ts = df1.set_index('belongs_to')['totala'].values.astype(np.float64)

    # Find the best SARIMA model parameters
    model = auto_arima(ts, seasonal=True, m=12, suppress_warnings=True, error_action='ignore')
    # Print the selected model parameters
    print(f"Selected model parameters: p={model.order[0]}, d={model.order[1]}, q={model.order[2]}, P={model.seasonal_order[0]}, D={model.seasonal_order[1]}, Q={model.seasonal_order[2]}, m={model.seasonal_order[3]}")
    conn.commit()
    conn.close()

start_task = DummyOperator(
    task_id='start_task',
    dag=dag
)

t1 = PythonOperator(
    task_id='ml_parameters',
    python_callable=ml_parameters,
    dag=dag
)

end_task = DummyOperator(
    task_id='end_task',
    dag=dag
)


start_task >> t1 >> end_task