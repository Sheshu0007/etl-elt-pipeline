# Automated ETL and ELT Pipeline with Apache Airflow

## 1. Project Overview

This project demonstrates an automated data pipeline using Python, Pandas, CSV files, and Apache Airflow. It extracts order data, validates records, separates valid and rejected data, calculates sales amounts, performs a basic incremental load, and records execution details in an audit log.

The workflow is orchestrated using an Apache Airflow DAG running through Docker Compose.

## 2. Objectives

- Build an ETL pipeline to process order data.
- Validate required columns and data quality.
- Identify missing values, duplicate order IDs, and invalid records.
- Separate clean records from rejected records.
- Calculate total sales for valid orders.
- Demonstrate incremental loading of new order IDs.
- Maintain an audit log of successful ETL executions.
- Orchestrate the ETL script using Apache Airflow.

## 3. Technology Stack

- **Language:** Python
- **Data processing:** Pandas
- **Data format:** CSV
- **Workflow orchestration:** Apache Airflow
- **Containerization:** Docker and Docker Compose
- **Environment:** Ubuntu on WSL2, VS Code
- **Version control:** Git (optional)

## 4. Project Architecture

```text
Source CSV
   |
   v
Extract order data
   |
   v
Validate required columns and records
   |
   +----------------------+
   |                      |
   v                      v
Clean records       Rejected records
   |
   v
Calculate total sales
   |
   v
Write processed CSV files
   |
   v
Append execution details to audit log

Apache Airflow DAG
   |
   v
Runs the Python ETL script
```

## 5. Project Structure

```text
ETLELT usecase/
├── airflow/
│   ├── dags/
│   │   └── etl_pipeline_dag.py
│   ├── config/
│   ├── logs/
│   ├── plugins/
│   ├── .env
│   └── docker-compose.yaml
├── config/
├── data/
│   ├── orders_raw.csv
│   ├── orders_test.csv
│   └── processed/
│       ├── orders_clean.csv
│       ├── orders_rejected.csv
│       ├── orders_incremental.csv
│       └── audit_log.csv
├── logs/
├── src/
│   ├── etl_pipeline.py
│   └── incremental_load.py
├── tests/
├── README.md
└── .gitignore
```

## 6. Pipeline Components

### Extract

Reads the source order data from `data/orders_raw.csv` using Pandas.

### Transform

- Checks that required columns exist.
- Cleans whitespace from selected text fields.
- Converts quantity and unit price to numeric values.
- Identifies records with missing values, duplicate order IDs, invalid email values, or invalid numeric values.
- Calculates `total_amount` for valid records.

### Load

Writes the clean records to `orders_clean.csv` and rejected records to `orders_rejected.csv` under `data/processed/`.

### Incremental Loading

The separate `src/incremental_load.py` script demonstrates identifying valid new orders that are not already present in the existing clean dataset.

This is a CSV-based incremental-loading demonstration, not a production database checkpointing system.

### Audit Logging

The ETL script appends successful execution details to `data/processed/audit_log.csv`, including the execution timestamp, extracted row count, valid row count, rejected row count, total sales, and status.

### Workflow Orchestration

The Airflow DAG `etl_pipeline_workflow` runs `src/etl_pipeline.py` through a BashOperator. The Airflow services run using Docker Compose.

## 7. Setup and Execution

Run commands in the Ubuntu/WSL terminal from the project root unless otherwise specified.

### Run the ETL pipeline

```bash
.venv-wsl/bin/python src/etl_pipeline.py
```

### Run the incremental-loading demonstration

```bash
.venv-wsl/bin/python src/incremental_load.py
```

### Start Apache Airflow

```bash
cd airflow
docker compose up -d
```

Open the Airflow interface:

http://localhost:8080

Sign in using the local credentials configured for your development environment. Do not publish credentials or secret keys.

### Run the DAG

1. Find `etl_pipeline_workflow` in the Airflow interface.
2. Unpause the DAG if necessary.
3. Trigger a manual DAG run.
4. Open the run and inspect the `run_orders_etl` task and its logs.

To stop the Airflow services when they are no longer needed:

```bash
docker compose down
```

This command stops and removes the Compose containers and network; it does not remove named volumes unless you explicitly request volume removal.

## 8. Output Files

| File | Purpose |
|---|---|
| `orders_clean.csv` | Validated and transformed orders |
| `orders_rejected.csv` | Records that failed validation |
| `orders_incremental.csv` | Output from the incremental-loading demonstration |
| `audit_log.csv` | Successful ETL execution history |

## 9. Verified Results

For the current six-row source dataset, a successful ETL execution produced:

- Rows extracted: 6
- Valid rows: 6
- Rejected rows: 0
- Total sales: 77,500
- ETL status: SUCCESS

The incremental-loading demonstration was also executed successfully. It reported six existing records, one valid new record, and seven records in its resulting dataset.

The Airflow DAG was manually triggered and completed successfully.

These results describe the current sample data and verified executions; they are not a benchmark of production-scale performance.

## 10. Current Scope and Limitations

- The source and processed datasets are CSV files.
- Incremental loading is demonstrated with CSV files rather than a persistent database checkpoint.
- The current Airflow DAG runs the ETL script; the incremental-loading script is executed separately.
- An AWS-based ELT pipeline, production-grade retry strategy, failure audit logging, and automated test suite are not claimed as completed components.

## 11. Future Enhancements

- Load data into PostgreSQL or another relational database.
- Add persistent incremental checkpoints and upsert logic.
- Add automated data-quality tests.
- Add failure logging, retries, and alerting in Airflow.
- Implement a cloud-based ELT workflow using AWS services.
- Add CI/CD and GitHub Actions.

## 12. Conclusion

This project demonstrates core data engineering concepts, including ETL, data validation, rejected-record handling, basic incremental loading, audit logging, and workflow orchestration with Apache Airflow. It provides a foundation for extending the pipeline toward a database-backed and cloud-based data platform.
