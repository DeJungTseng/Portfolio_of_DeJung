import numpy as np
import pandas as pd
from tkinter import messagebox
import datasource
from auth_utils import verify_password
from window import Window
from dotenv import load_dotenv
import os

load_dotenv()

class MainExec:
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
            
            # Since we don't have the actual model implementation,
            # we'll just create a placeholder
            # print("Loading recommendation model...")
            # self.model = {
            #     "type": "random_forest",
            #     "regression": True,
            #     "feature_selection": True
            # }
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def model(self, user_id, gen_mov, gen_mov_id):
        self.user_id = user_id

        watch_history = datasource.get_watched(user_id)
        user_preferences = datasource.get_user_genres(user_id)

        # 組成 feature row
        genres = [user_preferences.get(f'genre={i}', 0) for i in range(1, 6)]
        genre_diversity = sum(1 for g in genres if g > 0)
        rating_complexity = np.mean(genres) * genre_diversity
        input_data = pd.DataFrame([{
            f'genre={i+1}': genres[i] for i in range(5)
        } | {
            'genre_diversity': genre_diversity,
            'rating_complexity': rating_complexity
        }])

        # 取得所有電影資料
        all_movies = datasource.get_movies()

        # 建立推薦清單
        scored_movies = []
        for movie in all_movies:
            if movie['movie_id'] not in watch_history['movie_id'].tolist():
                movie_genres = movie['genres']  # 假設是 list of genre ID
                movie_feature = input_data.copy()

                # 如果你想根據每部電影的 genre 重新組成 feature，也可以
                # 否則就用 user_preferences 預測每部電影的 rating (簡化方式)

                predicted_rating = self.model.predict(movie_feature)[0]
                scored_movies.append((predicted_rating, movie))

        # 排序並選出 top 5
        recommended_movies = sorted(scored_movies, reverse=True, key=lambda x: x[0])[:5]
        result = [movie for _, movie in recommended_movies]

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
    
    def movie_process(self):
        """Process movie data for recommendation"""
        # This could include data preprocessing, normalization, etc.
        print("Processing movie data...")
        # Placeholder for now
        return True
        
def main(user_id=None):
    """
    Main function to run the application
    
    Args:
        user_id: Optional user ID to bypass login
        
    Returns:
        image_names: List of recommended movie titles
        image_paths: List of paths to movie poster images
    """
    try:
        # Create main executor
        executor = MainExec()
        
        # Load the model
        if not executor.load_model():
            messagebox.showerror("Error", "Failed to load recommendation model")
            return None, None
        
        if user_id is None:
            # Launch the GUI (this will handle login)
            window = Window(theme="breeze")
            
            # The Window class now handles the login process in its __init__
            # If the window was created successfully, get the user_id
            if hasattr(window, 'login_dialog') and window.login_dialog.apply():
                user_id = window.login_dialog.username.get()
                window.mainloop()
            else:
                print("Login failed or window was closed")
                return None, None
        
        # Use the provided/logged-in user ID to generate recommendations
        movie_ids = executor.model(user_id, True, True)
        image_paths, image_names = executor.movie_recommended(movie_ids)
        return image_names, image_paths
        
    except Exception as e:
        print(f"Error in main: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    main()
