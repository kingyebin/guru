import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Safari WebDriver 설정
driver = webdriver.Safari()

# itch.io 검색 URL
search_url = "https://itch.io/search?q="

# CSV 데이터 불러오기
file_path = '/Users/AIFFELthon/final/data/null/null_platform.csv'
df = pd.read_csv(file_path)
df = df[df['platforms'].isna()]

# 게임 검색 결과 리스트 초기화
search_results = []

# 게임을 itch.io에 검색하고 플랫폼 업데이트
for index, row in df.iterrows():
    original_game_name = row['name']
    query = f"{search_url}{original_game_name.replace(' ', '+')}"

    # itch.io에서 검색
    driver.get(query)
    time.sleep(2)  # 페이지 로딩 대기

    # 검색 결과 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', class_='game_title')

    # 검색 결과 중 정확한 이름 매칭 찾기
    matched = False
    for result in results:
        game_name = result.text.strip()
        if game_name.lower() == original_game_name.lower():
            matched = True
            break

    # 정확히 매칭된 경우에만 플랫폼을 업데이트
    if matched:
        search_results.append(1)
        df.at[index, 'platforms'] = 'Web'
    else:
        search_results.append(0)

# WebDriver 종료
driver.quit()

# 결과를 데이터프레임에 저장
df['itch_search'] = search_results

# 플랫폼이 'Web'이 아닌 게임만 필터링
missing_platforms = df[df['itch_search'] == 0]

# 결과를 CSV로 저장
missing_platforms.to_csv('/Users/AIFFELthon/final/data/null/missing_platforms.csv', index=False)
