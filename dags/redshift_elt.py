from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator
from helpers import sql_queries

default_args = {
    'owner': 'vgonzenb',
    'start_date': pendulum.now(),
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
        s3_key="log_data/",
        json_format="s3://udacity-vgonzenb/log_json_path.json"
    )
    
    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table='staging_songs',
        redshift_conn_id='redshift',
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-vgonzenb",
        s3_key="song_data/",
        json_format="auto"
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        fact_table='songplays',
        redshift_conn_id='redshift',
        sql=sql_queries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        dim_table='users',
        redshift_conn_id='redshift',
        sql=sql_queries.user_table_insert,
        append_only=False
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        dim_table='songs',
        redshift_conn_id='redshift',
        sql=sql_queries.song_table_insert,
        append_only=True
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        dim_table='artists',
        redshift_conn_id='redshift',
        sql=sql_queries.artist_table_insert,
        append_only=True
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        dim_table='times',
        redshift_conn_id='redshift',
        sql=sql_queries.time_table_insert,
        append_only=True
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
    )

    start_operator >> stage_events_to_redshift >> load_songplays_table
    start_operator >> stage_songs_to_redshift >> load_songplays_table
    load_songplays_table >> load_user_dimension_table
    load_songplays_table >> load_song_dimension_table
    load_songplays_table >> load_artist_dimension_table
    load_songplays_table >> load_time_dimension_table


redshift_elt_dag = redshift_elt()

