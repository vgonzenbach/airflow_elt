from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator



default_args = {
    'owner': 'vgonzenb',
    'start_date': datetime(2018,11,1),
    'catchup': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5), 
    'depends_on_past': False,
    'email_on_retry': False
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def redshift_elt(*args, **kwargs):
    """Load data from S3 onto a staging table in Redshift"""
    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table='staging_events',
        redshift_conn_id='redshift',
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-vgonzenb",
        s3_key="log_data/{{ execution_date.year }}/{{ execution_date.month}}"
    )
    
    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table='staging_songs',
        redshift_conn_id='redshift',
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-vgonzenb",
        s3_key="song_data/"
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
    )

    start_operator >> stage_events_to_redshift 
    start_operator >> stage_songs_to_redshift 

redshift_elt_dag = redshift_elt()

