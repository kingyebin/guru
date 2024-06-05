from flask import Flask, request, jsonify
import threading
import pandas as pd
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# 데이터 로드 및 전처리
df = pd.read_csv('/Users/AIFFELthon/final/data/modified_data_03.csv')

df.loc[df['id'] == 119609, 'slug'] = 'nan'
df.loc[df['id'] == 119609, 'name'] = 'NaN'
df.loc[df['id'] == 100122, 'slug'] = 'null'
df.loc[df['id'] == 100122, 'name'] = 'NULL'
df.loc[df['id'] == 468408, 'slug'] = 'none'
df.loc[df['id'] == 468408, 'name'] = 'None'

game_data = df[['id', 'name', 'description', 'released', 'rating', 'genre', 'theme', 'developers', 'publishers', 'tags']]

columns_to_convert = ['genre', 'theme', 'developers', 'publishers', 'tags']
for column in columns_to_convert:
    game_data[column] = game_data[column].astype(str).str.lower()
    game_data[column] = game_data[column].apply(lambda x: unidecode(x))

for column in columns_to_convert:
    game_data[column] = game_data[column].str.replace(',', ' ', regex=False)

game_data['combined_features'] = (
    (game_data['genre'] + ' ') * 6 + 
    (game_data['theme'] + ' ') * 4 +  
    game_data['tags']
)

tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.8)
tfidf_matrix = tfidf.fit_transform(game_data['combined_features'])

nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(tfidf_matrix)

indices = pd.Series(game_data.index, index=game_data['name']).drop_duplicates()

def get_recommendations(title, nn_model, tfidf_matrix, indices, n_recommendations=10):
    if title not in indices:
        return "Game not found in dataset."
    
    idx = indices[title]
    query_vector = tfidf_matrix[idx]
    distances, indices = nn_model.kneighbors(query_vector, n_neighbors=n_recommendations + 1)
    
    sim_scores = list(zip(indices.flatten(), distances.flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1])
    game_indices = [i[0] for i in sim_scores[1:]]
    
    recommendations = game_data[['name', 'genre', 'theme', 'description']].iloc[game_indices]
    recommendations['distance'] = [score[1] for score in sim_scores[1:]]
    
    return recommendations

def filter_games(genre=None, theme=None, developers=None, publishers=None, tags=None):
    filtered_data = game_data
    
    if genre:
        genre = unidecode(genre.lower())
        filtered_data = filtered_data[filtered_data['genre'].str.contains(genre, case=False)]
    
    if theme:
        theme = unidecode(theme.lower())
        filtered_data = filtered_data[filtered_data['theme'].str.contains(theme, case=False)]
    
    if developers:
        developers = unidecode(developers.lower())
        filtered_data = filtered_data[filtered_data['developers'].str.contains(developers, case=False)]
    
    if publishers:
        publishers = unidecode(publishers.lower())
        filtered_data = filtered_data[filtered_data['publishers'].str.contains(publishers, case=False)]

    if tags:
        tags = unidecode(tags.lower())
        filtered_data = filtered_data[filtered_data['tags'].str.contains(tags, case=False)]
    
    return filtered_data

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Game Recommendation System!"

@app.route('/recommend', methods=['GET'])
def recommend():
    name = request.args.get('name').lower()
    recommendations = get_recommendations(name, nn, tfidf_matrix, indices)
    if isinstance(recommendations, str):
        return jsonify({"error": recommendations}), 400
    return recommendations.to_json(orient='records')

@app.route('/filter', methods=['GET'])
def filter():
    genre = request.args.get('genre')
    theme = request.args.get('theme')
    developers = request.args.get('developers')
    publishers = request.args.get('publishers')
    tags = request.args.get('tags')
    
    filtered_games = filter_games(genre, theme, developers, publishers, tags)
    return jsonify(filtered_games['name'].tolist())

def run_flask():
    app.run(debug=True, use_reloader=False)

# 백그라운드에서 Flask 앱 실행
threading.Thread(target=run_flask).start()
