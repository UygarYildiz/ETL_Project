import pandas as pd
import requests
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def fetch_data(url,timeout=15):
    try:
        response = requests.get(url,timeout=timeout)
        response.raise_for_status()  # Hata varsa exception fırlatır
        return response.json()
    except requests.Timeout:
        print(f"Request timed out after {timeout} seconds")
        return {"error": "timeout"}
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": "http_error"}
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": "request_exception"}


def extract_data():
    users=fetch_data("https://jsonplaceholder.typicode.com/users")
    posts=fetch_data("https://jsonplaceholder.typicode.com/posts")
    comments=fetch_data("https://jsonplaceholder.typicode.com/comments")

    users_df=pd.json_normalize(users)
    posts_df=pd.DataFrame(posts)
    comments_df=pd.DataFrame(comments)

    return users_df, posts_df, comments_df


def transform_data(users_df, posts_df, comments_df):
    users_df.rename(columns={"address.city":"city","company.name":"company_name"}, inplace=True)
    users_df_selected=users_df[[
        "id",
        "name",
        "username",
        "city",
        "email",
        "phone",
        "website",
        "company_name"]].copy()
    
    posts_df.rename(columns={"userId":"user_id"}, inplace=True)
    comments_df.rename(columns={"postId":"post_id"}, inplace=True)
    return users_df_selected, posts_df, comments_df


def load_data(users_df, posts_df, comments_df):
    try:
        load_dotenv()
        db_url=os.getenv("DB_URL")
        db_engine=create_engine(db_url)
        with db_engine.begin() as connection:
            connection.execute(text("TRUNCATE TABLE comments, posts, users RESTART IDENTITY CASCADE;"))
            users_df.to_sql('users', con=connection, if_exists='append', index=False)
            posts_df.to_sql('posts', con=connection, if_exists='append', index=False)
            comments_df.to_sql('comments', con=connection, if_exists='append', index=False)
    except Exception as e:
        print(f"Veritabanı Hatası: {e}")


def run_etl():
    users_df, posts_df, comments_df = extract_data()
    users_df_selected, posts_df, comments_df = transform_data(users_df, posts_df, comments_df)
    load_data(users_df_selected, posts_df, comments_df)
