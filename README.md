# timeforge_airflow

This project is done as a task to be submitted for the internship opportunity for Summer 2023 at Timeforge.

Import the provided sales data csv from three retail stores into a SQL database of your choice such as MySQL, PostgreSQL, or SQLite. The sales data contains the store id, date and daily sales.

## Create a sales forecasting pipeline using Apache Airflow that automates the following steps:

* Configuration: Use a configuration file (e.g., .ini, .yaml, or .json) to store database connection details, file paths, and other necessary configurations.
*  Data ingestion: Connect to the SQL database using a Python library such as SQLAlchemy, Pandas, following Python idiomatic practices. Read the sales dataset from the database. Low-level sql modules such as psycopg2 are perfectly acceptable.
* Model selection:: Use the auto_arima function from the pmdarima library to automatically find the best SARIMA model parameters (p, d, q) and seasonal parameters (P, D, Q, m) for the given data. Log the selected model parameters using Python's logging module.
* Model training and forecasting: Train the SARIMA model using the best parameters (or predefined default parameters if model selection is not performed) and forecast sales for the next thirty days. Store the forecasts in the SQL database.

## Expected Deliverables:
* A Python script with the necessary Airflow DAG (Directed Acyclic Graph) definition that automates the described steps, utilizing Python idioms where appropriate. 
* A configuration file (e.g., .ini, .yaml, or .json) to store necessary configurations.
* Python logging setup to log relevant information, including model selection and evaluation results
* A README file describing setup and running the DAG in a Python virtual environment. Code committed to a repo such as Github.

## Installation and Set-up of Airflow in local system.
* To verify the existence of latest version of python and pip,
``` python3 -V ```
``` pip --version ```
* To create a python virtual environment,
``` python3 -m venv venv1 ```
* To activate the virtual environment,
``` source venv1/bin/activate ```
* To install the apache-airflow latest version with the constraints,
``` pip3 install 'apache-airflow==2.5.3' --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.3/constraints-3.7.txt" ```
* To create a user to access the web UI of apache-airflow,
``` airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin ```
* To set the path at airflow.cfg file,
``` export AIRFLOW_HOME=~/airflow ```
* To initiate the airflow database,
``` airflow db init ```
* To activate the webserver at 'http://localhost:8080'
``` airflow webserver -p 8080 ```
* To run the airflow scheduler,
``` airflow scheduler ```
* To find and kill the processes already running,
``` ps -ef | grep 8080 ```
```kill -9 <pid> ```
## Database activation to access the dataset
* To install the postgreSQL database,
``` sudo apt install postgresql ```
* To start the porstgreSQL service,
``` sudo su - postgres ```
``` sudo service postgresql start ```
``` psql ```
* To know your database details,
``` \conninfo ```
* To create a database with similar columns and their datatypes,
``` CREATE TABLE store_sales(location_id integer,belongs_to date,totala float); ```
* To copy the data from our local csv file to database,
``` COPY store_sales(location_id,belongs_to,totala) FROM '/tmp/project/store_sales.csv' DELIMITER ',' CSV HEADER; ```

* Similar steps in Azure and also, make sure to add the inbound port rule to the database, airflow web ui and allow the action in networking tab of virtual machine of Azure.

Here, uploading the only required files projectcode.py is the code used to generate the appropriate model parameters after training the model. The code is stored at '/Users/ayeshashaik/Desktop/InternProject/venv_project/lib/python3.9/site-packages/airflow/example_dags/projectcode.py' and the related logs are '/Users/ayeshashaik/Desktop/InternProject/airflow/logs/scheduler/2023-04-27/native_dags/example_dags/attempt=1.log' and '/Users/ayeshashaik/Desktop/InternProject/airflow/logs/scheduler/2023-04-27/native_dags/example_dags/attempt=2.log'
