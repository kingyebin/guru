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

# 장르별 평균 평점
def calculate_average_ratings_by_genre():
    genre_ratings_dict = {}
    split_pattern = r'[,]+'

    for _, row in games_df.iterrows():
        genres = re.split(split_pattern, row['genre'].strip())
        for genre in genres:
            if genre not in genre_ratings_dict:
                genre_ratings_dict[genre] = []
            genre_ratings_dict[genre].append(row['rating'])

    genre_avg_ratings = {genre: sum(ratings)/len(ratings) for genre, ratings in genre_ratings_dict.items() if len(ratings) >= 10}
    sorted_genre_avg_ratings = sorted(genre_avg_ratings.items(), key=lambda x: x[1], reverse=True)[:10]

    return sorted_genre_avg_ratings

# 플랫폼별 YouTube, Twitch, Reddit 인기 통계
def calculate_social_media_stats_by_platform():
    social_media_stats_dict = {}
    split_pattern = r'[,]+'

    for _, row in games_df.iterrows():
        platforms = re.split(split_pattern, row['platforms'].strip())
        for platform in platforms:
            if platform not in social_media_stats_dict:
                social_media_stats_dict[platform] = {'youtube_count': 0, 'twitch_count': 0, 'reddit_count': 0}
            social_media_stats_dict[platform]['youtube_count'] += row['youtube_count']
            social_media_stats_dict[platform]['twitch_count'] += row['twitch_count']
            social_media_stats_dict[platform]['reddit_count'] += row['reddit_count']

    sorted_social_media_stats = sorted(social_media_stats_dict.items(), key=lambda x: x[1]['youtube_count'], reverse=True)[:10]

    return sorted_social_media_stats

# 개발사별 총 평점
def split_and_count(column, count_column):
    split_pattern = r'[,]+'
    counts_dict = {}

    for _, row in games_df.iterrows():
        if pd.notna(row[column]):
            items = re.split(split_pattern, row[column].strip())
            for item in items:
                if item not in counts_dict:
                    counts_dict[item] = 0
                counts_dict[item] += row[count_column]

    counts_series = pd.Series(counts_dict).sort_values(ascending=False)
    return counts_series

# Stats
average_ratings_by_genre = calculate_average_ratings_by_genre()
social_media_stats_by_platform = calculate_social_media_stats_by_platform()

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

# Category routes
@app.route('/category/<category>', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_category_data(category):
    if category == 'platforms':
        unique_values = category_platforms.to_dict()
    elif category == 'genres':
        unique_values = category_genres.to_dict()
    elif category == 'themes':
        unique_values = category_themes.to_dict()
    elif category == 'modes':
        unique_values = category_modes.to_dict()
    elif category == 'developers':
        unique_values = category_developers.to_dict()
    elif category == 'publishers':
        unique_values = category_publishers.to_dict()
    elif category == 'tags':
        unique_values = category_tags.to_dict()
    else:
        unique_values = {}
    return jsonify(unique_values)

@app.route('/category/<category>/<value>', methods=['GET'])
def get_games_by_category_value(category, value):
    column_map = {
        'platforms': 'platforms',
        'genres': 'genre',
        'themes': 'theme',
        'modes': 'mode',
        'developers': 'developers',
        'publishers': 'publishers',
        'tags': 'tags'
    }
    
    if category in column_map:
        column = column_map[category]
        filtered_games = games_df[games_df[column].str.contains(value, case=False, na=False)]
        games_list = filtered_games.to_dict(orient='records')
    else:
        games_list = []
    return jsonify(games_list)

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

# stats
@app.route('/stats/social_media', methods=['GET']) # 플랫폼별 YouTube, Twitch, Reddit 인기 통계
def get_social_media_stats():
    labels = [item[0] for item in social_media_stats_by_platform]
    youtube = [item[1]['youtube_count'] for item in social_media_stats_by_platform]
    twitch = [item[1]['twitch_count'] for item in social_media_stats_by_platform]
    reddit = [item[1]['reddit_count'] for item in social_media_stats_by_platform]

    return jsonify({
        'labels': labels,
        'youtube': youtube,
        'twitch': twitch,
        'reddit': reddit
    })

@app.route('/stats/rating_reviews', methods=['GET']) # 평점별 리뷰 수
def get_rating_reviews_stats():
    rating_reviews_stats = games_df.groupby('rating')['reviews_text_count'].sum().sort_index()
    # 리뷰 수가 1 이하인 평점을 제외
    rating_reviews_stats = rating_reviews_stats[rating_reviews_stats > 1]
    filtered_ratings = rating_reviews_stats[rating_reviews_stats > 0]  # 다시 한 번 필터링

    # 라벨과 값 생성
    labels = filtered_ratings.index.tolist()
    values = filtered_ratings.values.tolist()

    return jsonify({
        'labels': labels,
        'values': values
    })


@app.route('/stats/yearly_additions', methods=['GET']) # 연도별 추가된 게임 수
def get_yearly_additions_stats():
    yearly_additions_stats = games_df.groupby(games_df['released'].str[:4])['additions_count'].sum().sort_index()
    return jsonify({
        'labels': yearly_additions_stats.index.tolist(),
        'values': yearly_additions_stats.values.tolist()
    })

@app.route('/stats/genre_ratings', methods=['GET']) # 장르별 평균 평점
def get_genre_ratings_stats():
    labels, values = zip(*average_ratings_by_genre)
    
    return jsonify({
        'labels': labels,
        'values': values
    })
    
@app.route('/stats/review_rating', methods=['GET']) # 리뷰 수 대비 평균 평점
def get_review_rating_stats():
    review_rating_stats = games_df.groupby('reviews_text_count')['rating'].mean().sort_index().head(10)
    return jsonify({
        'labels': review_rating_stats.index.tolist(),
        'values': review_rating_stats.values.tolist()
    })

@app.route('/stats/developer_ratings', methods=['GET'])
def get_developer_ratings_stats():
    developer_ratings_stats = games_df.groupby('developers')['rating'].sum().sort_values(ascending=False).head(10)
    return jsonify({
        'labels': developer_ratings_stats.index.tolist(),
        'values': developer_ratings_stats.values.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)
