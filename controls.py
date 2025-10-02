from datas import users_df, posts_df, comments_df

def uzunluk_kontrol(df,columns):
    for col in columns:
        max_len = df[col].str.len().max()
        print(f"{col} sütununun maksimum uzunluğu: {max_len}")

uzunluk_kontrol(users_df, ["name", "username", "city", "email", "phone", "website", "company_name"])
uzunluk_kontrol(posts_df, ["title", "body"])
uzunluk_kontrol(comments_df, ["name", "email", "body"])
