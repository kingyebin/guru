import requests
import pandas as pd
import concurrent.futures
import time
import os

# API 키 설정
API_KEY = 'API_KEY'
BASE_URL = 'https://api.rawg.io/api'

# 특정 게임의 시리즈 목록을 가져오는 함수
def get_game_series(game_pk, page=1, page_size=40):
    url = f'{BASE_URL}/games/{game_pk}/game-series'
    params = {
        'key': API_KEY,
        'page': page,
        'page_size': page_size
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# 특정 게임의 ID를 가져오는 함수
def get_game_id(game_name):
    url = f'{BASE_URL}/games'
    params = {
        'key': API_KEY,
        'search': game_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['id']
    return None

# 게임 목록 CSV 파일 읽기
input_file_path = '/Users/AIFFELthon/final/data/modified_data.csv/modified_data.csv'
output_file_path = '/Users/AIFFELthon/final/data/modified_data.csv/modified_data_game_series.csv'
df = pd.read_csv(input_file_path)

# 결과를 저장할 리스트
results = []

# CSV 파일에 데이터를 저장하는 함수
def save_results_to_csv(results, output_file_path, mode='a', header=False):
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file_path, mode=mode, header=header, index=False, encoding='utf-8')

# 결과 파일이 없는 경우 헤더 포함하여 저장
if not os.path.exists(output_file_path):
    save_results_to_csv([{
        'Original Game': 'Original Game',
        'Series Game Name': 'Series Game Name',
        'Released': 'Released',
        'Rating': 'Rating'
    }], output_file_path, mode='w', header=True)

# 각 게임에 대해 시리즈 정보 가져오기
def process_game_series(game_name):
    game_id = get_game_id(game_name)
    temp_results = []
    if game_id:
        series_data = get_game_series(game_id)
        print(f"Processing game: {game_name} (ID: {game_id})")
        for game in series_data['results']:
            print(f"  Found series game: {game['name']} (Released: {game['released']})")
            temp_results.append({
                'Original Game': game_name,
                'Series Game Name': game['name'],
                'Released': game['released'],
                'Rating': game['rating']
            })
    else:
        print(f"Game ID not found for: {game_name}")
        temp_results.append({
            'Original Game': game_name,
            'Series Game Name': None,
            'Released': None,
            'Rating': None
        })
    save_results_to_csv(temp_results, output_file_path)
    return temp_results

# 병렬 처리를 사용하여 각 게임에 대해 시리즈 정보 가져오기
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_game_series, row['name']) for index, row in df.iterrows()]
    for future in concurrent.futures.as_completed(futures):
        future.result()

print(f"Series information saved to: {output_file_path}")