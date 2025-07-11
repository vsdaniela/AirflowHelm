from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
dag = DAG(
    'ejemplo_dag_configmap_v2',
    default_args=default_args,
    description='A simple example DAG from ConfigMap',
    schedule=timedelta(days=1),  # Use 'schedule' instead of 'schedule_interval'
    catchup=False,
)

# Define tasks
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    dag=dag,
)

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command='echo "{{ ds }}" && echo "{{ macros.ds_add(ds, 7) }}"',
    dag=dag,
)

# Set task dependencies
t1 >> [t2, t3]
