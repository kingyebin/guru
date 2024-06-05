import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# 데이터 불러오기 (구분자 ',' 사용)
df = pd.read_csv('/Users/AIFFELthon/final/data/modified_data_03.csv', delimiter=',')

# 유사도 계산을 위한 텍스트 데이터 결합 (이름과 설명 제외)
df['combined'] = (
    (df['genre'].str.replace(',', ' ') + ' ') * 5 +
    (df['platforms'].str.replace(',', ' ') + ' ') * 4 +
    df['tags'].str.replace(',', ' ') + ' ' +
    (df['developers'].str.replace(',', ' ') + ' ') * 2 +
    (df['theme'].str.replace(',', ' ') + ' ') * 3 +
    df['esrb_rating'] + ' ' +
    (df['mode'].str.replace(',', ' ') + ' ') * 2 
)

# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['combined'])

# Nearest Neighbors 모델 설정
nn_model = NearestNeighbors(n_neighbors=6, algorithm='auto', metric='cosine')
nn_model.fit(tfidf_matrix)

# 유사한 게임 찾기
distances, indices = nn_model.kneighbors(tfidf_matrix)

# 유사한 게임 ID를 저장할 리스트 초기화
similar_games = []
for i in range(indices.shape[0]):
    similar_game_ids = df.iloc[indices[i][1:]]['id'].tolist()  # 첫 번째는 자기 자신이므로 제외
    similar_games.append(similar_game_ids)

# 새로운 칼럼 추가
df['similar_game'] = similar_games

# 결과 저장 (구분자 ',' 사용)
df.to_csv('/Users/AIFFELthon/final/data/modified_data_05.csv', index=False)