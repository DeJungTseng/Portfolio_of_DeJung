# recommendation_engine.py
from model_exec import ModelExec

def get_recommendation(user_id):
    """
    根據使用者 ID 產出推薦的電影資訊

    Args:
        user_id (str): 使用者帳號名稱（登入後取得）

    Returns:
        tuple: (image_names, image_paths)
    """
    executor = ModelExec()
    if not executor.load_model():
        print("無法載入模型")
        return [], []

    movie_ids = executor.recommender_model(user_id=user_id, gen_mov=True, gen_mov_id=True)
    image_paths, image_names = executor.movie_recommended(movie_ids)
    return image_names, image_paths