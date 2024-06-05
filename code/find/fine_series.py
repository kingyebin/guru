import csv
import requests
import pandas as pd
import os
from multiprocessing import Pool

# API 키
API_KEY = 'e5512bfe469d462b97115a0d95b6f048'  # 여기에 실제 API 키를 입력하세요

input_filename = '/Users/AIFFELthon/final/data/modified_data_01.csv'  # 입력 파일 이름
output_directory = '/Users/AIFFELthon/final/data/series_1'  # 중간 결과 저장 디렉토리
batch_size = 1000  # 한 번에 처리할 슬러그 개수

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def get_game_pk(game_slug):
    url = f"https://api.rawg.io/api/games?search={game_slug}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]['id']
    return None

def get_game_series(game_pk):
    url = f"https://api.rawg.io/api/games/{game_pk}/game-series?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def save_series_to_csv(series_info, writer):
    for game in series_info['results']:
        esrb_rating = game.get('esrb_rating')
        row = {
            'id': game.get('id'),
            'slug': game.get('slug'),
            'name': game.get('name'),
            'released': game.get('released'),
            'tba': game.get('tba'),
            'background_image': game.get('background_image'),
            'rating': game.get('rating'),
            'rating_top': game.get('rating_top'),
            'ratings_count': game.get('ratings_count'),
            'reviews_text_count': game.get('reviews_text_count'),
            'added': game.get('added'),
            'metacritic': game.get('metacritic'),
            'playtime': game.get('playtime'),
            'suggestions_count': game.get('suggestions_count'),
            'updated': game.get('updated'),
            'esrb_rating': esrb_rating['name'] if esrb_rating else 'Not Rated',
            'platforms': ', '.join([platform['platform']['name'] for platform in game.get('platforms', [])])
        }
        writer.writerow(row)

def process_batch(batch):
    batch_number, slugs = batch
    output_filename = os.path.join(output_directory, f'output_batch_{batch_number}.csv')

    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'id', 'slug', 'name', 'released', 'tba', 'background_image',
            'rating', 'rating_top', 'ratings_count', 'reviews_text_count',
            'added', 'metacritic', 'playtime', 'suggestions_count',
            'updated', 'esrb_rating', 'platforms'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for slug in slugs:
            game_pk = get_game_pk(slug)
            if game_pk:
                series_info = get_game_series(game_pk)
                if series_info:
                    save_series_to_csv(series_info, writer)
                else:
                    print(f"Failed to retrieve series information for '{slug}'.")
            else:
                print(f"Failed to retrieve game_pk for '{slug}'.")

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# 입력 파일에서 게임 슬러그 읽기 (game_series_count가 0이 아닌 경우만 필터링)
df = pd.read_csv(input_filename)
filtered_df = df[df['game_series_count'] != 0]
slugs = filtered_df['slug'].tolist()

# 슬러그를 배치로 나누기
batches = list(enumerate(chunks(slugs, batch_size)))

# 병렬 처리
with Pool(processes=4) as pool:  # CPU 코어 수에 맞게 조절
    pool.map(process_batch, batches)

# 중간 결과 파일 합치기
with open('game_series_info.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = [
        'id', 'slug', 'name', 'released', 'tba', 'background_image',
        'rating', 'rating_top', 'ratings_count', 'reviews_text_count',
        'added', 'metacritic', 'playtime', 'suggestions_count',
        'updated', 'esrb_rating', 'platforms'
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(len(batches)):
        batch_filename = os.path.join(output_directory, f'output_batch_{i}.csv')
        with open(batch_filename, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                writer.writerow(row)

# 중간 결과 파일이 저장된 디렉토리
output_directory = '/Users/AIFFELthon/final/data/series_1'
output_filename = '/Users/AIFFELthon/final/data/game_series_info.csv'

# 최종 결과 파일 작성
with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = [
        'id', 'slug', 'name', 'released', 'tba', 'background_image',
        'rating', 'rating_top', 'ratings_count', 'reviews_text_count',
        'added', 'metacritic', 'playtime', 'suggestions_count',
        'updated', 'esrb_rating', 'platforms', 'developers', 'publishers'
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # 중간 결과 파일을 읽어서 최종 결과 파일에 추가
    for i in range(len(os.listdir(output_directory))):
        batch_filename = os.path.join(output_directory, f'output_batch_{i}.csv')
        if os.path.exists(batch_filename):
            with open(batch_filename, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    writer.writerow(row)

print("All game series information saved to game_series_info.csv.")