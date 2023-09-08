#/bin/bash
#brew install postgresql@15
source .venv/bin/activate
brew services start postgresql@15
psql postgres < $(dirname $0)/setup_db.sql
airflow db migrate
airflow connections delete 'airflow_db'
airflow connections add 'airflow_db' --conn-uri 'postgres://airflow:airflow@127.0.0.1:5432/airflow'