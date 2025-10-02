import requests
import pandas as pd

users=requests.get("https://jsonplaceholder.typicode.com/users").json()
posts=requests.get("https://jsonplaceholder.typicode.com/posts").json()
comments=requests.get("https://jsonplaceholder.typicode.com/comments").json()

users_df=pd.json_normalize(users)
posts_df=pd.DataFrame(posts)
comments_df=pd.DataFrame(comments)
print(comments_df.columns)