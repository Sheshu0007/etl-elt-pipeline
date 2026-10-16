
from datetime import datetime
from pathlib import Path

from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_DIR = Path("/opt/airflow/project")


@dag(
    dag_id="etl_pipeline_workflow",
    description="Run the existing orders ETL pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "portfolio"],
)
def etl_pipeline_workflow():

    run_etl = BashOperator(
        task_id="run_orders_etl",
        bash_command=(
            f"cd '{PROJECT_DIR}' && "
            "python src/etl_pipeline.py"
        ),
    )


etl_pipeline_workflow()
