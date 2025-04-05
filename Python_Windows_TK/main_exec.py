import numpy as np
import pandas as pd
from tkinter import messagebox
import datasource
from window import Window

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
        """
        Generate movie recommendations based on user ID and preferences
        
        Args:
            user_id: The ID of the current user
            gen_mov: Boolean to indicate if we should generate movie recommendations
            gen_mov_id: Boolean to indicate if we should return movie IDs
            
        Returns:
            movie_id: List of recommended movie IDs
        """
        self.user_id = user_id
        
        # Get user watch history
        watch_history = datasource.get_watched(user_id)
        
        # Get user preferences (genres)
        user_preferences = datasource.get_user_genres(user_id)
        
        # Process genres for recommendation
        processed_genres = datasource.genres_process(user_preferences)
        
        # Here, we would use the model to recommend movies
        # For now, we'll just simulate this with a simple algorithm
        
        # Get all available movies
        all_movies = datasource.get_movies()
        
        # Filter movies based on user preferences and watch history
        # This is a simplified version of what would actually happen with your model
        recommended_movies = []
        for movie in all_movies:
            # Don't recommend movies the user has already watched
            if movie['movie_id'] not in watch_history['movie_id'].tolist():
                # Check if it matches any of the user's preferred genres
                if any(genre in movie['genres'] for genre in processed_genres):
                    recommended_movies.append(movie)
                    
        # Sort by some criteria (e.g., release date, popularity)
        # For this example, we'll just take the first 5
        recommended_movies = recommended_movies[:5]
        
        # Return the movie IDs if requested
        if gen_mov_id:
            return [movie['movie_id'] for movie in recommended_movies]
        else:
            return recommended_movies
    
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
    # Create main executor
    executor = MainExec()
    
    # Load the model
    if not executor.load_model():
        messagebox.showerror("Error", "Failed to load recommendation model")
        return None, None
    
    if user_id is None:
        # Launch the GUI (this will handle login)
        window = Window(theme="breeze")
        window.mainloop()
    else:
        # Use the provided user ID to generate recommendations
        movie_ids = executor.model(user_id, True, True)
        image_paths, image_names = executor.movie_recommended(movie_ids)
        return image_names, image_paths


if __name__ == "__main__":
    main()
