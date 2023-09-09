from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 fact_table,
                 redshift_conn_id,
                 sql,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params
        self.fact_table = fact_table
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        

    def execute(self, context):
        # init hook
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        # format interst slq statemtn
        insert_sql_stmt = """
            INSERT INTO public.{}
        	{}
        """.format(self.fact_table, self.sql)
        # run sql
        self.log.info(f"Inserting values into {self.fact_table}")
        redshift.run(insert_sql_stmt)

