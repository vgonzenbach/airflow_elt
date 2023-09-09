from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.secrets.metastore import MetastoreBackend

class StageToRedshiftOperator(BaseOperator):
    template_fields = ("s3_key",)
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 table,
                 redshift_conn_id,
                 aws_credentials_id,
                 s3_bucket,
                 s3_key,
                 json_format='auto',
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        
        # Map params
        self.table=table
        self.redshift_conn_id=redshift_conn_id
        self.aws_credentials_id=aws_credentials_id
        self.s3_bucket=s3_bucket
        self.s3_key=s3_key
        self.json_format=json_format

    def execute(self, context):
        # set up aws credentials
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection(self.aws_credentials_id)
        # set up a hook using the redshift connection and the 
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        # Clear data before copying
        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))
        # Populate s3_key with context variables if its a templated string
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(
            self.s3_bucket, 
            rendered_key
        )
        # format copy sql query
        copy_sql_stmt = """
            COPY {}
            FROM '{}'
            ACCESS_KEY_ID '{}'
            SECRET_ACCESS_KEY '{}'
            FORMAT AS JSON '{}'
        """.format(
            self.table,
            s3_path,
            aws_connection.login,
            aws_connection.password,
            self.json_format
        )
        # run sql
        self.log.info("Copying data from S3 into Redshift staging table")
        redshift.run(copy_sql_stmt)


