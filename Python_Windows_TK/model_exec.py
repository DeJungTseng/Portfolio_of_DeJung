import numpy as np
import pandas as pd
from tkinter import messagebox
import datasource
from auth_utils import verify_password
# from window import Window
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

class ModelExec:
    def __init__(self):
        self.type = "movie_recommendation"
        self.model = None
        self.user_id = None
        self.movie_id = None
    
    def load_model(self):
        """Load the trained recommendation model"""
        try:
            # Here you would load your pre-trained model
            # For example, using pickle to load a saved model
            import pickle
            with open('model/trained_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
                print(f"[model type]: {type(self.model)}")
            return True
        except Exception as e:
            print(f"[loading model]Error loading model: {e}")
            return False
    
    def recommender_model(self, user_id, gen_mov=None, gen_mov_id=False):
        self.user_id = user_id

        # 使用者歷史紀錄與偏好
        watch_history = datasource.get_watched(user_id)
        print(f"[all movies]{watch_history}")
        watched_titles = [m['movie_title'] for m in watch_history]
        
        user_preferences = datasource.get_user_genres(user_id)  # 假設格式為 {'genre=1': 1, ..., 'genre=5': 0}
        print(f"[user preferences]{user_preferences}")

        # 全部電影資料
        all_movies = datasource.get_movies().to_dict(orient="records")
        

        # 建立推薦清單
        scored_movies = []

        # 特徵索引（k=3）
        selected_feature_names = [f'genre={i}' for i in range(1, 6)] + ['genre_diversity', 'rating_complexity']

        for movie in all_movies:
            movie_title = movie['movie_title']
            movie_genres = movie['genres']  # 假設是 dict like {'genre=1': 1, ..., 'genre=5': 0}
            print(f"[movie_genres] {movie_genres} ({type(movie_genres)})")

            if movie_title in watched_titles:
                continue  # 跳過已看過的電影

            # # 有模型的版本:構建電影特徵 row
            # genres = [user_preferences.get(f'genre={i}', 0) for i in range(1, 6)]
            # genre_diversity = sum(1 for g in genres if g > 0)
            # rating_complexity = np.mean(genres) * genre_diversity if genre_diversity > 0 else 0

            # feature_row = {
            #     f'genre={i+1}': genres[i] for i in range(5)
            # }
            # feature_row['genre_diversity'] = genre_diversity
            # feature_row['rating_complexity'] = rating_complexity

            # input_df = pd.DataFrame([feature_row])
            # input_selected = input_df[selected_feature_names]

            # # 預測推薦分數
            # predicted_rating = self.model.predict(input_selected)[0]
            # scored_movies.append((predicted_rating, movie))
            ## ======End 有模型的版本======

            # ======沒有模型的版本:用genre向量來配對電影偏好=======
            # 使用者偏好向量
            user_vec = np.array([user_preferences.get(f'genre={i}', 0) for i in range(1, 6)])

            # 電影類型向量（假設是 one-hot dict）
            movie_vec = np.array([movie_genres.get(f'genre={i}', 0) for i in range(1, 6)])

            # 相似度分數：偏好與電影類型的匹配度
            match_score = np.dot(user_vec, movie_vec)

            scored_movies.append((match_score, movie))
            # ======End 沒有模型的版本=======




        # 根據預測分數排序並取前 5
        recommended_movies = sorted(scored_movies, reverse=True, key=lambda x: x[0])[:5]
        result = [movie for _, movie in recommended_movies]

        # 印出推薦結果（debug 用）
        print(f"\n[使用者 {user_id} 推薦結果]")
        for i, m in enumerate(result, 1):
            print(f"{i}. {m['movie_title']} ({m['movie_id']})")

        # 回傳 id 或完整資料
        if gen_mov_id:
            return [movie['movie_id'] for movie in result]
        else:
            return result



        
    def movie_recommended(self, movie_id):
        """
        Fetch details about recommended movies
        
        Args:
            movie_id: List of movie IDs to fetch details for
            
        Returns:
            image_paths: List of paths to movie poster images
            image_names: List of movie titles
        """
        image_paths = []
        image_names = []
        
        # Fetch details for each movie
        for mid in movie_id:
            movie_details = datasource.get_movie_by_id(mid)
            if movie_details is not None:
                image_paths.append(f"Images/{movie_details['movie_poster']}")
                image_names.append(movie_details['movie_title'])
        
        return image_paths, image_names
    

# def main(user_id=None):
#     """
#     Main function to run the application
    
#     Args:
#         user_id: Optional user ID to bypass login
        
#     Returns:
#         image_names: List of recommended movie titles
#         image_paths: List of paths to movie poster images
#     """
#     try:
#         # Create main executor
#         executor = ModelExec()
        
#         # Load the model
#         if not executor.load_model():
#             messagebox.showerror("Error", "Failed to load recommendation model")
#             return None, None
        
#         if user_id is None:
#             # Launch the GUI (this will handle login)
#             window = Window(theme="breeze")
            
#             # The Window class now handles the login process in its __init__
#             # If the window was created successfully, get the user_id
#             if hasattr(window, 'login_dialog') and window.login_dialog.apply():
#                 user_id = window.login_dialog.username.get()
#                 window.mainloop()
#             else:
#                 print("Login failed or window was closed")
#                 return None, None
        
#         # Use the provided/logged-in user ID to generate recommendations
#         movie_ids = executor.recommender_model(user_id, True, True)
#         image_paths, image_names = executor.movie_recommended(movie_ids)
#         # print(f"[image_names]: {image_names},[image_paths]:{image_paths}")
#         return image_names, image_paths
        
#     except Exception as e:
#         print(f"Error in main: {e}")
#         messagebox.showerror("Error", f"An error occurred: {e}")
#         return None, None

# if __name__ == "__main__":
#     main()
