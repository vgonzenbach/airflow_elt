from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 dim_table,
                 redshift_conn_id,
                 sql,
                 append_only=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params 
        self.dim_table = dim_table
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.append_only = append_only

    def execute(self, context):
        # init hook
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if not self.append_only: # execute truncate-insert pattern
            self.log.info(f"{self.append_only} is set to False. Clearing data before insertion")
            truncate_sql_stmt = """
                DELETE FROM {};
            """.format(self.dim_table)
            redshift.run(truncate_sql_stmt)

        # format intert slq statement
        insert_sql_stmt = """
            INSERT INTO public.{}
        	{}
        """.format(self.dim_table, self.sql)
        # run sql
        self.log.info(f"Inserting values into {self.dim_table}")
        redshift.run(insert_sql_stmt)
