import sys
import pandas as pd
sys.path.append('/opt/airflow/project')
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator 
from datetime import datetime
from etl import extract_data, transform_data, load_data
from airflow.decorators import dag, task

@dag(
    dag_id='etl_pipeline',
    start_date=datetime(2025, 1, 1),

    catchup=False
)
def etl_pipeline_taskflow():

    @task
    def extract(multiple_outputs=True):
        users_df, posts_df, comments_df = extract_data()
        return {"users_df": users_df.to_json(),  # ← DataFrame'leri JSON'a çevir
                "posts_df": posts_df.to_json(),
                "comments_df": comments_df.to_json()}



    @task (multiple_outputs=True)
    def transform(data: dict):
        users_df = pd.read_json(data["users_df"])      # ← JSON'dan DataFrame'e çevir
        posts_df = pd.read_json(data["posts_df"])
        comments_df = pd.read_json(data["comments_df"])

        users_t, posts_t, comments_t = transform_data(users_df, posts_df, comments_df)
        return {
            "users_df": users_t.to_json(),      
            "posts_df": posts_t.to_json(),
            "comments_df": comments_t.to_json()
        }

        
        

    @task()
    def load(data: dict):
        users_df = pd.read_json(data["users_df"])
        posts_df = pd.read_json(data["posts_df"])
        comments_df = pd.read_json(data["comments_df"])

        load_data(users_df, posts_df, comments_df)
        

    extracted = extract()
    transformed = transform(extracted)
    load(transformed)

etl_pipeline_taskflow()