"""這傢伙是用來sql的大象溝通師"""

import psycopg2
import pandas as pd
import sqlalchemy
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os

'''
接收user login資料之user_id，以sql由user_table取得user_id之觀看電影紀錄。
以(Type)傳給Main_exec.py中的data_process功能。
'''

# plz think how to manange the data structure to get the user watched genres
def get_watched(user_id):
    conn_params = {
    'host': os.environ['postgres_host'],
    'database': os.environ['postgres_db'],
    'user': os.environ['postgres_user'],
    'password': os.environ['postgres_password']
    }


    # SQL 查詢語句
    query = """
    SELECT DISTINCT movie_title 
    FROM public.user_movie_data  
    WHERE user_id = %s 
    ORDER BY movie_title;
    """

    try:
        # 建立資料庫連線
        conn = psycopg2.connect(**conn_params)
        user_id='hbrpoig8'
        # 執行查詢並轉換為 DataFrame
        watched_movies = pd.read_sql(query, conn, params=(user_id,))
        
        return watched_movies

    except (Exception, psycopg2.Error) as error:
        print("查詢時發生錯誤:", error)
        return pd.DataFrame()  # 返回空 DataFrame

    finally:
        # 關閉資料庫連線
        if conn:
            conn.close()



'''
依照model output genres(變數)，以SQL於movie_table中選取release date在30日內，具有model output genre的movie_id, movie_name, poster
'''
def get_user_genres(user_id):
    conn_params = {
    'host': os.environ['postgres_host'],
    'database': os.environ['postgres_db'],
    'user': os.environ['postgres_user'],
    'password': os.environ['postgres_password']
    }


    # SQL 查詢語句
    query = """
    SELECT DISTINCT movie_title 
    FROM public.user_movie_data  
    WHERE user_id = %s 
    ORDER BY movie_title;
    """

    try:
        # 建立資料庫連線
        conn = psycopg2.connect(**conn_params)
        user_id='hbrpoig8'
        # 執行查詢並轉換為 DataFrame
        watched_movies = pd.read_sql(query, conn, params=(user_id,))

        # convert dataframe to list
        watched_movies = watched_movies['movie_title'].tolist()
        
        return watched_movies

    except (Exception, psycopg2.Error) as error:
        print("查詢時發生錯誤:", error)
        return pd.DataFrame()  # 返回空 DataFrame

    finally:
        # 關閉資料庫連線
        if conn:
            conn.close()

'''取得15日內電影資訊'''
import pandas as pd
from datetime import datetime, timedelta


def get_movies():
    """
    取得最近 14 天內上映的電影
    
    Returns:
    pandas.DataFrame: 包含最近上映電影資訊的資料框
    """
    # initialize conn
    conn=None
    # 計算 14 天前的日期
    recent_date = datetime.now() - timedelta(days=14)
    
    # SQL 查詢語句
    query = """
    SELECT *
    FROM public.movie_table
    WHERE release_date >= %s
    ORDER BY release_date DESC;
    """
    conn_params = {
    'host': os.environ['postgres_host'],
    'database': os.environ['postgres_db'],
    'user': os.environ['postgres_user'],
    'password': os.environ['postgres_password']
    }

    try:
        # 使用 Pandas 執行查詢
        conn = psycopg2.connect(**conn_params)
        df = pd.read_sql(query, conn, params=[recent_date.strftime('%Y-%m-%d %H:%M:%S')])
        return df
    except Exception as e:
        print(f"查詢時發生錯誤: {e}")
        return pd.DataFrame()
    finally:
    # 關閉資料庫連線
        if conn:
            conn.close()

def convert_dataframe_to_movie_list(df):
    """
    将 DataFrame 转换为电影列表格式
    
    Args:
        df (pd.DataFrame): 包含电影信息的 DataFrame
    
    Returns:
        list: 电影列表，每个电影是 [movie_id, movie_title, genres, release_date, poster]
    """
    movies = []
    
    for _, row in df.iterrows():
        movie = [
            row['movie_id'],     # 假设有 movie_id 列
            row['movie_title'],  # 假设有 movie_title 列
            row['genres'],       # 假设有 genres 列
            row['release_date'], # 假设有 release_date 列
            row['movie_poster']        # 假设有 poster 列
        ]
        movies.append(movie)
    
    return movies
    

# # 使用方法
# df = get_movies()
# movies = convert_dataframe_to_movie_list(df)

# # 如果需要遍历
# for movie in movies:
#     movie_id, movie_title, genres, release_date, poster = movie
#     # 进行后续处理

'''取得movie genre餵進模型'''
import pandas as pd


def get_movie_genres():
    """
    取得電影類型分佈並將其轉換為指定格式
    
    Returns:
    pandas.DataFrame: 包含使用者電影類型偏好向量的資料表
    """
    # SQL 查詢
    query = """
    SELECT 
        m.movie_id,
        TRIM(BOTH ',' FROM
        REPLACE(m.genres, ' ', '')) AS genres
    FROM public.movie_table m;
    """

    conn_params = {
    'host': os.environ['postgres_host'],
    'database': os.environ['postgres_db'],
    'user': os.environ['postgres_user'],
    'password': os.environ['postgres_password']
    }
    
    try:
        # 使用 Pandas 執行查詢
        conn = psycopg2.connect(**conn_params)
        df = pd.read_sql(query, conn)
        
        # 轉換 genres 欄位
        genre_mapping = {
            'adventure': 1,
            'affection': 2,
            'comedy': 3,
            'horror': 4,
            'history': 5
        }
        
        # 展開 genres 欄位並計算出現次數
        df['genre_vector'] = df['genres'].str.split(',').apply(lambda x: [genre_mapping.get(g, 0) for g in x])
        df['genre_1'] = df['genre_vector'].apply(lambda x: x.count(1))
        df['genre_2'] = df['genre_vector'].apply(lambda x: x.count(2))
        df['genre_3'] = df['genre_vector'].apply(lambda x: x.count(3))
        df['genre_4'] = df['genre_vector'].apply(lambda x: x.count(4))
        df['genre_5'] = df['genre_vector'].apply(lambda x: x.count(5))
        
        # 選取所需欄位
        return df[['movie_id', 'genre_1', 'genre_2', 'genre_3', 'genre_4', 'genre_5', 'genre_vector']]
    
    except Exception as e:
        print(f"查詢時發生錯誤: {e}")
        return pd.DataFrame()
    finally:
    # 關閉資料庫連線
        if conn:
            conn.close()



