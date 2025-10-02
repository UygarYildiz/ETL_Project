from etl import extract_data, transform_data, load_data
import pandas as pd

if __name__ == "__main__":
    # 1. EXTRACT - Veri çekme
    users_df_selected, posts_df, comments_df = extract_data()

    # 2. TRANSFORM - Veri dönüştürme
    users_df_selected, posts_df, comments_df = transform_data(users_df_selected, posts_df, comments_df)

    # 3. LOAD - Veritabanına yükleme
    load_data(users_df_selected, posts_df, comments_df)