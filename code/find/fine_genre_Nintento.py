import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 데이터 로드
df = pd.read_csv('/Users/AIFFELthon/final/data/null/null_genre.csv')

# 'Nintendo'가 포함된 플랫폼만 필터링
df = df[df['platforms'].str.contains('Nintendo', na=False)]

# WebDriver 설정
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

results = []

for index, row in df.iterrows():
    game_name = row['name']
    
    driver.get("https://www.fandom.com/")
    
    # 검색 아이콘 클릭
    search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.global-navigation__search')))
    search_icon.click()
    
    # 검색어 입력 및 검색 실행
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.search-input')))
    search_input.clear()
    search_input.send_keys(game_name + Keys.ENTER)
    
    # 결과 페이지 로딩 대기
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.unified-search__result__title')))
        results_links = driver.find_elements(By.CSS_SELECTOR, 'a.unified-search__result__title')
        
        for link in results_links:
            if game_name.lower() in link.text.lower():
                driver.execute_script("window.open(arguments[0]);", link.get_attribute('href'))
                driver.switch_to.window(driver.window_handles[1])
                
                try:
                    genre_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-source="genre"] .pi-data-value')))
                    genre = genre_element.text.strip()
                    results.append({'name': game_name, 'genre': genre})
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    break
                except (NoSuchElementException, TimeoutException):
                    results.append({'name': game_name, 'genre': 'Not found'})
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    break
        
    except (TimeoutException, NoSuchElementException):
        results.append({'name': game_name, 'genre': 'Not found'})

driver.quit()

# 결과 저장
results_df = pd.DataFrame(results)
results_df.to_csv('/Users/AIFFELthon/final/data/null/results_nintendo.csv', index=False)
