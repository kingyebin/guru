# 라이브러리 호출
import ast
import datetime
import pandas as pd
from argparse import ArgumentParser

import warnings

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 1. 기존 데이터 프레임 불러오기
csv_path = "cleansing_game_data.csv"
games_df = pd.read_csv(csv_path, index_col=0)
recommend_num = 12

# 2. user_data
# 2-1) 입력값 데이터프레임으로 불러오기
user_data = pd.DataFrame([selected_values])

# 2-2) 결측치 처리
user_data["rating"] = user_data["rating"].fillna(3.5)
user_data["birth_year"] = user_data["birth_year"].fillna(datetime.datetime.now().year)
user_data = user_data.fillna("")

# 2-3) 변수 설정
user_platforms = user_data["platforms"][0]
user_birth_year = user_data["birth_year"][0]
user_rating = user_data["rating"][0]
user_mode = user_data["mode"][0]
user_genres = user_data["genre"][0]
user_themes = user_data["theme"][0]
user_tags = user_data["tags"][0]


# 3. 데이터 필터링
# 3-1) Platforms
def filter_by_platforms(df, platform_filter):
    """
    default = ""
    값을 입력하지 않으면 모든 게임을 반환하고,
    값을 입력하면 입력된 platform이 포함된 데이터를 필터링한다.
    """
    if platform_filter == "":
        df = df
    else:
        platforms_filter_list = platform_filter.split(",")
        df = df[
            df["platforms"].apply(
                lambda x: all(
                    platform in x.split(",") for platform in platforms_filter_list
                )
            )
        ]
    return df


filter_p_df = filter_by_platforms(games_df, user_platforms)


# 3-2) esrb_rating
def filter_by_age(birth_year, df):
    """
    default=current_year
    값을 입력하지 않으면 전연령 게임만 반환하고,
    값을 입력하면 입력된 나이에 맞는 esrb_rating에 따라 데이터를 필터링한다.
    """
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
    else:
        df = df
        age = "20+"
    return df


filter_pa_df = filter_by_age(user_birth_year, filter_p_df)


# 3-3) rating
def filter_by_rating(rating, df):
    """
    default = 3.5
    입력된 rating 이상의 데이터만 남도록 필터링한다.
    """
    df = df[df["rating"] >= rating]
    return df


filter_par_df = filter_by_rating(user_rating, filter_pa_df)


# 3-4) mode
def filter_by_mode(mode, df):
    """
    default = " "
    값을 입력하지 않으면 데이터 전부를 반환하고,
    값을 입력하면 입력된 mode에 맞게 데이터를 필터링한다.
    """
    if mode == " ":
        df = df
    else:
        df = df[df["mode"].apply(lambda x: mode in x)]
    return df


filter_parm_df = filter_by_mode(user_mode, filter_par_df)


# 4. 인덱스 리셋
final_df = filter_parm_df.reset_index(drop=True)


# 5. 벡터화
cv = CountVectorizer()
cv_matrix = cv.fit_transform(final_df["merge"])


# 6. 사용자 벡터
# 6-1) genres, themes 가중치를 주어 병합하기
def merge_column(g_weight, t_weight):
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


user_taste = merge_column(3, 3)

# 6-2) 사용자 취향 벡터화
user_vector = cv.transform(user_taste)

# 7. 게임 추천
# 7-1) 코사인 유사도 계산하기
cos_sim = cosine_similarity(user_vector, cv_matrix)


# 7-2) 게임 추천 리스트
def reommendation(recommend_num, df, cos_sim):
    """
    코사인 유사도가 높은 게임을 recommend_num 개수만큼 추천한다.
    final_df 데이터가 recommend_num보다 적으면 final_df를 모두 반환한다.
    """
    pred_sim_games = list(enumerate(cos_sim[0]))
    sorted_pred_sim_games = sorted(pred_sim_games, key=lambda x: x[1], reverse=True)[1:]

    reommendation_list = []
    similarity_list =  []
    max_recommendations = min(recommend_num, len(df) - 1)

    for i, item in enumerate(sorted_pred_sim_games):
        if i >= max_recommendations:
            break
        recommendation_game = df[df.index == item[0]]["id"].values[0]
        reommendation_list.append(recommendation_game)
        similarity = str(round(item[1] * 100, 3)) + "%"
        similarity_list.append(similarity)

    return reommendation_list


recommendation_list = reommendation(recommend_num, final_df, cos_sim)
