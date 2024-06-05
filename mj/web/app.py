from flask import Flask, render_template, jsonify, request
from flask_caching import Cache
import pandas as pd
import re
from main import recommend_games

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Feather로 저장
# df = pd.read_csv('/Users/test/data/data.csv')
# df.to_feather('/Users/test/data/data.csv')

# 데이터 로드 및 전처리
data_path = '/Users/guru/data/data.feather'
games_df = pd.read_feather(data_path)

# 데이터 전처리
games_df.loc[games_df['id'] == 119609, 'slug'] = 'nan'
games_df.loc[games_df['id'] == 119609, 'name'] = 'NaN'
games_df.loc[games_df['id'] == 100122, 'slug'] = 'null'
games_df.loc[games_df['id'] == 100122, 'name'] = 'NULL'
games_df.loc[games_df['id'] == 468408, 'slug'] = 'none'
games_df.loc[games_df['id'] == 468408, 'name'] = 'None'

# 평점이 3.8 이상인 게임 필터링
top_rated_games = games_df[games_df['rating'] >= 3.8].sort_values(by='rating', ascending=False)

# 카테고리별 유니크 값과 게임 수 계산
def get_unique_category_counts(column):
    category_list = []
    split_pattern = r'[,]+'
    for category in games_df[column].dropna():
        category_list.extend(re.split(split_pattern, category.strip()))
    unique_category = pd.Series(category_list).value_counts()
    unique_category = unique_category[unique_category.index != '']  # 빈 문자열 제거
    unique_category = unique_category[unique_category >= 10]  # 게임 수가 10개 이상인 경우만 포함
    return unique_category

# Recommend
platforms = get_unique_category_counts('platforms').index.tolist()
genres = get_unique_category_counts('genre').index.tolist()
themes = get_unique_category_counts('theme').index.tolist()
modes = get_unique_category_counts('mode').index.tolist()
tags = get_unique_category_counts('tags').head(100).index.tolist()

# Category
category_platforms = get_unique_category_counts('platforms')
category_genres = get_unique_category_counts('genre')
category_themes = get_unique_category_counts('theme')
category_modes = get_unique_category_counts('mode')
category_developers = get_unique_category_counts('developers').head(100)
category_publishers = get_unique_category_counts('publishers').head(100)
category_tags = get_unique_category_counts('tags').head(100)
category_esrb = get_unique_category_counts('esrb_rating')

@app.route('/')
def index():
    return render_template('index.html')

# Top Rating Games
@app.route('/games', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def get_games():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 6))
    start = (page - 1) * per_page
    end = start + per_page
    games = top_rated_games.iloc[start:end].to_dict(orient='records')
    return jsonify(games)

# Search
@app.route('/search', methods=['POST'])
def search():
    search_term = request.json['search_term'].lower()
    results = games_df[games_df['name'].str.contains(search_term, case=False)]
    return jsonify(results.to_dict(orient='records'))

# Upcoming
@app.route('/upcoming_2024', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def get_upcoming_2024():
    upcoming_2024_games = games_df[games_df['released'].str.contains(r'202[4-9]|20[3-9][0-9]')][:100].to_dict(orient='records')
    return jsonify(upcoming_2024_games)

@app.route('/upcoming_tba', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def get_upcoming_tba():
    tba_games = games_df[games_df['tba'] == True].to_dict(orient='records')
    return jsonify(tba_games)

# Popular
@app.route('/youtube_popularity', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def youtube_popularity():
    youtube_sorted_games = games_df.sort_values(by='youtube_count', ascending=False).head(100)
    return jsonify(youtube_sorted_games.to_dict(orient='records'))

@app.route('/twitch_popularity', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def twitch_popularity():
    twitch_sorted_games = games_df.sort_values(by='twitch_count', ascending=False).head(100)
    return jsonify(twitch_sorted_games.to_dict(orient='records'))

@app.route('/reddit_popularity', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def reddit_popularity():
    reddit_sorted_games = games_df.sort_values(by='reddit_count', ascending=False).head(100)
    return jsonify(reddit_sorted_games.to_dict(orient='records'))

@app.route('/user_suggestions', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def user_suggestions():
    suggestions_sorted_games = games_df.sort_values(by='suggestions_count', ascending=False).head(100)
    return jsonify(suggestions_sorted_games.to_dict(orient='records'))

@app.route('/text_reviews_count', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # 60초 동안 캐싱
def text_reviews_count():
    reviews_sorted_games = games_df.sort_values(by='reviews_text_count', ascending=False).head(100)
    return jsonify(reviews_sorted_games.to_dict(orient='records'))

# Recommend Unique Select
@app.route('/unique_values', methods=['GET'])
def unique_values():
    column = request.args.get('column')
    if column == 'platforms':
        unique_values = platforms
    elif column == 'genre':
        unique_values = genres
    elif column == 'theme':
        unique_values = themes
    elif column == 'mode':
        unique_values = modes
    elif column == 'tags':
        unique_values = tags
    else:
        unique_values = []
    return jsonify(unique_values)

# Recommned Game
@app.route('/recommend', methods=['POST'])
def recommend_games_api():
    selected_values = request.json
    user_data = pd.DataFrame([selected_values])
    recommendation_list = recommend_games(user_data, recommend_num=12)
    games_df['id'] = pd.Categorical(games_df['id'], categories=recommendation_list, ordered=True)
    recommended_games = games_df[games_df['id'].isin(recommendation_list)].sort_values('id').to_dict(orient='records')
    return jsonify(recommended_games)

if __name__ == '__main__':
    app.run(debug=True)
