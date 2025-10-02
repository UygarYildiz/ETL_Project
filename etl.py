import pandas as pd
import requests
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import numpy as np
import logging
from sqlalchemy import Table, MetaData
# API'den veri çekme fonksiyonu
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

## Json placeholder API si ile gelen telfon numaraları çok çeşitli formatlarda geliyor.
## Bunları sadece rakamlardan oluşan bir formata çevirmek için aşağıdaki fonksiyonu yazdım.
def clean_usersdata(df):
    df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    df['email'] = df['email'].str.lower().str.strip()
    df['username'] = df['username'].str.lower().str.strip()
    df['phone'] = df['phone'].str.replace(r'[^0-9+]', '', regex=True)
    df['website'] = df['website'].str.lower().str.strip()
    df["email"]=np.where(df["email"].str.contains("@", na=False), df["email"], "invalid_email")
    
    return df

def clean_commentsdata(df):
    df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    df['email'] = df['email'].str.lower().str.strip()
    df["email"]=np.where(df["email"].str.contains("@", na=False), df["email"], "invalid_email")
    return df

def clean_postsdata(df):
    df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    return df


def add_timestamps(df):
    now = pd.Timestamp.now()
    df["created_at"] = now
    df["updated_at"] = now
    return df



def upsert_users(connection, df):
    df.to_sql("temp_users", con=connection, if_exists='replace', index=False)
    connection.execute(text("""
        INSERT INTO users(id, name, username, city, email, phone, website, company_name, created_at, updated_at)
        SELECT user_id, name, username, city, email, phone, website, company_name, created_at, updated_at FROM temp_users
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            username = EXCLUDED.username,
            city = EXCLUDED.city,
            email = EXCLUDED.email,
            phone = EXCLUDED.phone,
            website = EXCLUDED.website,
            company_name = EXCLUDED.company_name,
            updated_at = EXCLUDED.updated_at
    """))
    connection.execute(text("DROP TABLE IF EXISTS temp_users"))
    logging.info("Users tablosu güncellendi. (upserst)")



def upsert_posts(connection, df):
    df.to_sql("temp_posts", con=connection, if_exists='replace', index=False)
    connection.execute(text("""
        INSERT INTO posts(id, user_id, title, body, created_at, updated_at)
        SELECT id, user_id, title, body, created_at, updated_at FROM temp_posts
        ON CONFLICT (id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            title = EXCLUDED.title,
            body = EXCLUDED.body,
            updated_at = EXCLUDED.updated_at
    """))
    connection.execute(text("DROP TABLE IF EXISTS temp_posts"))
    logging.info("Posts tablosu güncellendi. (upsert)")



    
def upsert_comments(connection, df):
    df.to_sql("temp_comments", con=connection, if_exists='replace', index=False)
    connection.execute(text("""
        INSERT INTO comments(id, post_id, name, email, body, created_at, updated_at)
        SELECT id, post_id, name, email, body, created_at, updated_at FROM temp_comments
        ON CONFLICT (id) DO UPDATE SET
            post_id = EXCLUDED.post_id,
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            body = EXCLUDED.body,
            updated_at = EXCLUDED.updated_at
    """))
    connection.execute(text("DROP TABLE IF EXISTS temp_comments"))
    logging.info("Comments tablosu güncellendi. (upsert)")




# Extract, Transform, Load (ETL) işlemleri
def extract_data():
    users=fetch_data("https://jsonplaceholder.typicode.com/users")
    posts=fetch_data("https://jsonplaceholder.typicode.com/posts")
    comments=fetch_data("https://jsonplaceholder.typicode.com/comments")

    users_df=pd.json_normalize(users)
    posts_df=pd.DataFrame(posts)
    comments_df=pd.DataFrame(comments)

    return users_df, posts_df, comments_df



# Transform işlemleri
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

    
    
    
    users_df_selected=clean_usersdata(users_df_selected)
    comments_df=clean_commentsdata(comments_df)
    posts_df=clean_postsdata(posts_df)


    posts_df.rename(columns={"userId":"user_id"}, inplace=True)
    comments_df.rename(columns={"postId":"post_id"}, inplace=True)
    users_df_selected.rename(columns={"id":"user_id"}, inplace=True)


    users_df_selected=add_timestamps(users_df_selected)
    posts_df=add_timestamps(posts_df)
    comments_df=add_timestamps(comments_df)

    
    return users_df_selected, posts_df, comments_df





# Load işlemleri
def load_data(users_df, posts_df, comments_df):
    try:
        load_dotenv()
        db_url = os.getenv("DB_URL")
        db_engine = create_engine(db_url)
        with db_engine.begin() as connection:
            upsert_users(connection, users_df)
            upsert_posts(connection, posts_df)
            upsert_comments(connection, comments_df)
            
    except Exception as e:
        logging.error(f"Veritabanına yükleme sırasında hata oluştu: {e}")
        raise
            
           



logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



# ETL sürecini çalıştır
def run_etl():
    try:
        logging.info("ETL süreci başladı")
        users_df, posts_df, comments_df = extract_data()
        users_df_selected, posts_df, comments_df = transform_data(users_df, posts_df, comments_df)
        load_data(users_df_selected, posts_df, comments_df)
        logging.info("ETL süreci tamamlandı")
    except Exception as e:
        logging.error(f"ETL süreci sırasında hata oluştu: {e}")
        raise
