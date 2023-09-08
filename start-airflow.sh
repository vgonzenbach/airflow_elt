#!/bin/bash

# Create user
# airflow users create --email student@example.com --firstname aStudent --lastname aStudent --password admin --role Admin --username admin

# Start airflow
export AIRFLOW_HOME=$(dirname $0)
airflow scheduler -D
airflow webserver -D -p 8080
airflow users create --email student@example.com --firstname aStudent --lastname aStudent --password admin --role Admin --username admin

# Wait till airflow web-server is ready
echo "Waiting for Airflow web server..."
while true; do
  _RUNNING=$(ps aux | grep airflow-webserver | grep ready | wc -l)
  if [ $_RUNNING -eq 0 ]; then
    sleep 1
  else
    echo "Airflow web server is ready"
    break;
  fi
done

# Set connections and variables
airflow connections add aws_credentials --conn-uri 'aws://AKIAYFBI7WX5XXUFLMBK:0hStWmAeKuvx1RNxmbdMBalsVXPm0x4wsSEfW8lb@'
airflow connections add redshift --conn-uri 'redshift://awsuser:Password123@default-workgroup.560579196411.us-east-1.redshift-serverless.amazonaws.com:5439/dev'
airflow variables set s3_bucket udacity-vgonzenb
airflow variables set s3_prefix data-pipelines

