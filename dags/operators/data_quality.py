from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 tests,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tests = tests  # A list of dictionaries

    def execute(self, context):
        # Initialize hook
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Check if tests are provided
        if not self.tests:
            raise ValueError("No tests provided for DataQualityOperator")

        # Iterate over tests
        for test in self.tests:
            sql = test['sql']
            exp_result = test['expected_result']

            records = redshift.get_records(sql)

            # Check if records were returned
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {sql} returned no results")

            # Check if records match expected result
            if records[0][0] != exp_result:
                raise ValueError(f"Data quality check failed. {sql} returned {records[0][0]} which does not match expected result {exp_result}")

            self.log.info(f"Data quality on SQL {sql} check passed with {records[0][0]} records")


