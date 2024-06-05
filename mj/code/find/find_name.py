import glob
import os
import pandas as pd

# RAWG 데이터 읽기
rawg_df = pd.read_csv('/Users/AIFFELthon/final/data/RAWG/RAWG_game_info.csv')
rawg_name_id = rawg_df[['id', 'name']].astype(str)

# 파일별로 컬럼 이름을 지정한 매핑
file_column_mapping = {
    'gameDB_games_info.csv': 'Game Name',
    'genres.csv': 'name',
    'platforms.csv': 'name',
    'player_perspectives.csv': 'name',
    'Video_Games.csv': 'Name',
    'games-data.csv': 'name',
    'computer_games.csv': 'Name',
    'appstore_games_march_2021.csv': 'name_app',
    'Metacritic_games_of_all_time.csv': 'title',
    'game_statistics_feb_2023.csv': 'title',
    'minimap_game_info.csv': 'Game Name',
    'IGDB_game_info.csv': 'name'
}

# 데이터 파일이 들어 있는 폴더 경로 지정
folder_path = '/Users/AIFFELthon/final/data/'
# 하위 폴더를 포함한 모든 CSV 파일 찾기
csv_files = glob.glob(os.path.join(folder_path, '**', '*.csv'), recursive=True)

# 빈 리스트 생성하여 결과 수집
results = []

# 모든 다른 CSV 파일 순회 및 이름 비교
for csv_file in csv_files:
    # 매핑 정보로부터 파일 이름을 가져오기
    base_name = os.path.basename(csv_file)
    if base_name == 'RAWG_game_info.csv':
        continue
    
    try:
        # 지정된 파일 이름이 매핑에 있는 경우만 처리
        if base_name in file_column_mapping:
            # CSV 파일 읽기
            other_df = pd.read_csv(csv_file)
            # 지정된 컬럼 이름으로 매칭
            name_col = file_column_mapping[base_name]
            
            # 컬럼을 문자열로 변환하고 RAWG와 병합
            other_df[name_col] = other_df[name_col].astype(str)
            merged_df = pd.merge(rawg_name_id, other_df[[name_col]], left_on='name', right_on=name_col, how='inner')
            merged_df['csv_file'] = csv_file
            merged_df = merged_df.rename(columns={name_col: 'matching_name'})
            
            results.append(merged_df[['id', 'name', 'csv_file', 'matching_name']])
    except Exception as e:
        print(f"Error processing file {csv_file}: {e}")

# 결과를 DataFrame으로 결합
final_df = pd.concat(results, ignore_index=True)

# 결과 확인
print(final_df)

# 필요한 경우 결과를 CSV 파일로 저장
final_df.to_csv('/Users/AIFFELthon/final/data/matched_games_info.csv', index=False)
