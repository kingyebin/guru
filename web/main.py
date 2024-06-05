import datetime
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 기존 데이터 프레임 불러오기
csv_path = "/Users/test/data/cleansing_game_data.csv"
games_df = pd.read_csv(csv_path, index_col=0)

def preprocess_user_data(user_data):
    user_data["rating"] = user_data["rating"].fillna(3.5)
    user_data["year"] = user_data["year"].fillna(datetime.datetime.now().year)
    user_data = user_data.fillna(" ")
    return user_data

def get_user_preferences(user_data):
    return {
        "platforms": user_data["platforms"][0],
        "birth_year": user_data["year"][0],
        "rating": user_data["rating"][0],
        "mode": user_data["mode"][0],
        "genres": user_data["genre"][0],
        "themes": user_data["theme"][0],
        "tags": user_data["tags"][0],
    }

def filter_by_platforms(df, platform_filter):
    if platform_filter == "":
        return df
    platforms_filter_list = platform_filter.split(",")
    return df[df["platforms"].apply(lambda x: all(platform in x.split(",") for platform in platforms_filter_list))]

def filter_by_age(birth_year, df):
    current_year = datetime.datetime.now().year
    age = current_year - birth_year

    if age < 10:
        df = df[df["esrb_rating"] == "Everyone"]
    elif age < 13:
        df = df[df["esrb_rating"].isin(["Everyone 10+", "Everyone"])]
    elif age < 17:
        df = df[df["esrb_rating"].isin(["Teen", "Everyone 10+", "Everyone"])]
    elif age < 18:
        df = df[df["esrb_rating"].isin(["Mature", "Teen", "Everyone 10+", "Everyone"])]
    return df

def filter_by_rating(rating, df):
    return df[df["rating"] >= rating]

def filter_by_mode(mode, df):
    if mode == " ":
        return df
    return df[df["mode"].apply(lambda x: mode in x)]

def create_user_taste_vector(user_genres, user_themes, user_tags, g_weight=3, t_weight=3):
    temp_str = ""
    for j in range(len(user_genres.split(","))):
        for k in range(g_weight - j):
            temp_str += user_genres.split(",")[j] + ","
    for j in range(len(user_themes.split(","))):
        for k in range(t_weight - j):
            temp_str += user_themes.split(",")[j] + ","
    for j in range(len(user_tags.split(","))):
        temp_str += user_tags.split(",")[j] + ","
    return [temp_str]

def get_recommendations(df, user_taste_vector, recommend_num):
    cv = CountVectorizer()
    cv_matrix = cv.fit_transform(df["merge"])
    user_vector = cv.transform(user_taste_vector)
    cos_sim = cosine_similarity(user_vector, cv_matrix)

    pred_sim_games = list(enumerate(cos_sim[0]))
    sorted_pred_sim_games = sorted(pred_sim_games, key=lambda x: x[1], reverse=True)[1:]

    recommendation_list = []
    max_recommendations = min(recommend_num, len(df) - 1)

    for i, item in enumerate(sorted_pred_sim_games):
        if i >= max_recommendations:
            break
        recommendation_game = df[df.index == item[0]]["id"].values[0]
        recommendation_list.append(recommendation_game)

    return recommendation_list

def recommend_games(user_data, recommend_num=10):
    user_data = preprocess_user_data(user_data)
    user_prefs = get_user_preferences(user_data)

    filter_p_df = filter_by_platforms(games_df, user_prefs["platforms"])
    filter_pa_df = filter_by_age(user_prefs["birth_year"], filter_p_df)
    filter_par_df = filter_by_rating(user_prefs["rating"], filter_pa_df)
    filter_parm_df = filter_by_mode(user_prefs["mode"], filter_par_df)

    final_df = filter_parm_df.reset_index(drop=True)
    user_taste_vector = create_user_taste_vector(user_prefs["genres"], user_prefs["themes"], user_prefs["tags"])

    recommendations = get_recommendations(final_df, user_taste_vector, recommend_num)
    return recommendations

# 실행 예시 (테스트용)
if __name__ == "__main__":
    user_csv_path = "/Users/test/selected_values.csv"
    user_data = pd.read_csv(user_csv_path)
    recommendations = recommend_games(user_data, recommend_num=15)
    print(recommendations)
