"""這傢伙是用來sql的大象溝通師"""

import psycopg2
import pandas as pd
import sqlalchemy
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
from collections import defaultdict
from datetime import datetime, timedelta

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

    query = """
    SELECT DISTINCT movie_title
    FROM public.user_movie_data
    WHERE user_id = %s 
    ORDER BY movie_title;
    """

    try:
        # 建立資料庫連線
        conn = psycopg2.connect(**conn_params)
        user_id = user_id.get() if hasattr(user_id, 'get') else user_id

        # 執行查詢並轉換為 DataFrame
        # print(f"查詢 user_id: {user_id}")
        watched_movies = pd.read_sql(query, conn, params=(user_id,))

        # print("watch_movies 型態：", type(watched_movies))
        # print(watched_movies)  # 顯示 DataFrame 內容

        if watched_movies.empty:
            print("查詢結果為空，無電影資料")

        # convert pd frame to list
        watched_movie_list = watched_movies.to_dict(orient='records')
        # print("轉換後的 watched_movie_list：", watched_movie_list)

        return watched_movie_list

    except (Exception, psycopg2.Error) as error:
        print("查詢時發生錯誤:", error)
        return []  # 返回空列表
        
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


   # genre 映射表
    genre_map = {
        'adventure': 'genre=1',
        'affection': 'genre=2',
        'comedy': 'genre=3',
        'horror': 'genre=4',
        'history': 'genre=5'
    }

    # SQL 查詢語句：取得使用者看過的所有 genre 欄位
    query = """
    SELECT genres
    FROM public.user_movie_data
    WHERE user_id = %s;
    """

    try:
        conn = psycopg2.connect(**conn_params)
        user_id = user_id.get() if hasattr(user_id, 'get') else user_id

        df = pd.read_sql(query, conn, params=(user_id,))

        # 統計 genre 數量
        genre_count = defaultdict(int)

        for genre_str in df['genres']:
            genres = genre_str.split(',')
            for g in genres:
                g = g.strip().lower()
                if g in genre_map:
                    genre_count[genre_map[g]] += 1

        # 確保所有 genre 都有輸出
        output = {v: genre_count.get(v, 0) for v in genre_map.values()}
        # print("output:", output)

        return output

    except (Exception, psycopg2.Error) as error:
        print("查詢時發生錯誤:", error)
        return {}

    finally:
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
    conn = None
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

        # 處理 genres 欄位：轉換為 one-hot dict
        def parse_genres(genres_str):
            # 初始化 genre=1 到 genre=5
            genre_dict = {f'genre={i}': 0 for i in range(1, 6)}
            if isinstance(genres_str, str):
                for g in genres_str.split(','):
                    g = g.strip()
                    if g in genre_dict:
                        genre_dict[g] = 1
            return genre_dict

        df['genres'] = df['genres'].apply(parse_genres)
        return df

    except Exception as e:
        print(f"查詢時發生錯誤: {e}")
        return pd.DataFrame()

    finally:
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


def get_user_id_pw(username):
    """
    Query user credentials from the user_id_table in PostgreSQL
    
    Args:
        username: The username to look up
        
    Returns:
        tuple: (user_id, password) if found, (None, None) if not found or error
    """
    # print(f"[get_user_id_pw] Looking up credentials for username: {username}")
    
    try:
        conn_params = {
            'host': os.environ['postgres_host'],
            'database': os.environ['postgres_db'],
            'user': os.environ['postgres_user'],
            'password': os.environ['postgres_password']
        }
        # print("[get_user_id_pw] Database connection parameters loaded from environment")

        # SQL query to get user credentials
        query = """
        SELECT movie_user_id, movie_user_pw
        FROM public.user_id_table
        WHERE movie_user_id = %s;
        """

        # Establish database connection
        # print("[get_user_id_pw] Connecting to database...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Execute query with username parameter
        # print(f"[get_user_id_pw] Executing query for username: {username}")
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result:
            # print(f"[get_user_id_pw] Found credentials for username: {username}")
            return result[0], result[1]  # Return user_id and password
            
        # print(f"[get_user_id_pw] No credentials found for username: {username}")
        return None, None  # User not found

    except (Exception, psycopg2.Error) as error:
        print(f"[get_user_id_pw] Database error: {error}")
        return None, None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
            print("[get_user_id_pw] Database connection closed")

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



