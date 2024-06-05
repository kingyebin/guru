import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_game_info(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 검색 결과 페이지에서 첫 번째 게임의 상세 페이지 링크를 찾음
    game_link_element = soup.find('a', class_='search_result_row')
    if not game_link_element:
        return "Information Not Found", "Information Not Found"  # 검색 결과가 없으면 예외 처리

    game_link = game_link_element['href']

    # 게임 상세 페이지로 요청 보내기
    game_response = requests.get(game_link)
    game_soup = BeautifulSoup(game_response.text, 'html.parser')

    # 개발자와 출판사 정보를 안전하게 추출
    developer_info = game_soup.find('div', id='developers_list')
    developer = developer_info.text.strip() if developer_info else "Unknown"

    publisher_info = game_soup.find_all('div', class_='dev_row')
    publisher = publisher_info[1].text.split(':')[1].strip() if len(publisher_info) > 1 else "Unknown"

    return developer, publisher



# CSV 파일 로드
df = pd.read_csv('/Users/AIFFELthon/final/data/null/developers/null_developers.csv')

# 결측치 업데이트
for index, row in df.iterrows():
    if pd.isna(row['developers']) or pd.isna(row['publishers']):
        game_name = row['name']
        search_url = f"https://store.steampowered.com/search/?term={'+'.join(game_name.split())}"
        developer, publisher = fetch_game_info(search_url)
        df.at[index, 'developers'] = developer
        df.at[index, 'publishers'] = publisher

# 업데이트된 데이터프레임 저장
df.to_csv('/Users/AIFFELthon/final/data/null/developers/updated_file.csv', index=False)
