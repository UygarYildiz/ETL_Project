import requests
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv







load_dotenv()  # .env dosyasını yükle
db_url=os.getenv("DB_URL")

db_engine=create_engine(db_url)

print(users_df.columns)
users_df=users_df.rename(columns={"address.city":"city","company.name":"company_name"})


# Seçili sütunlar için yeni bir DataFrame oluşturma
users_selected=users_df[[
    "id",
    "name",
    "username",
    "city",
    "email",
    "phone",
    "website",
    "company_name"]].copy()


posts_df=posts_df.rename(columns={"userId":"user_id"})
comments_df=comments_df.rename(columns={"postId":"post_id"})


# company name normalize edildiği için sütun adını değiştirildi.


try:
    with db_engine.begin() as connection: 
        connection.execute(text("TRUNCATE TABLE comments, posts, users RESTART IDENTITY CASCADE;"))
        # child tablolar önce replace edilirse parent'ı drop ederken hata çıkmaz
        users_selected.to_sql('users', con=connection, if_exists='append', index=False)
        posts_df.to_sql('posts', con=connection, if_exists='append', index=False)
        comments_df.to_sql('comments', con=connection, if_exists='append', index=False)

except Exception as e:
    print(f"Veritabanı Hatası: {e}")

