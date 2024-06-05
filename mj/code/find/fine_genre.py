from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
import pandas as pd
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 데이터 불러오기
df = pd.read_csv('/Users/AIFFELthon/final/data/null/null_genre.csv')

# Selenium 드라이버 설정
driver = webdriver.Safari()
wait = WebDriverWait(driver, 5)

# 결과를 저장할 빈 데이터프레임
results_df = pd.DataFrame(columns=['name', 'tags', 'genres'])

for index, row in df.iterrows():
    game_name = row['name'].strip()
    driver.get(f"https://itch.io/search?q={game_name.replace(' ', '+')}")
    logging.info(f"Searching for game: {game_name}")

    try:
        # 경고창 처리
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            logging.info("Alert accepted")
        except TimeoutException:
            logging.info("No alert was present")

        game_grid = wait.until(EC.presence_of_element_located((By.ID, 'game_grid_0')))
        first_game_title = game_grid.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.game_cell_data > div.game_title').text.strip()
        logging.info(f"First game title found: {first_game_title}")

        if first_game_title == game_name:
            first_game = game_grid.find_element(By.CSS_SELECTOR, 'div:nth-child(1)')
            first_game.click()
            logging.info("Clicked on the game matching the search query.")

            more_info_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.more_information_toggle a.toggle_info_btn')))
            if not 'open' in more_info_toggle.find_element(By.XPATH, "..").get_attribute('class'):
                more_info_toggle.click()

            time.sleep(2)  # Allow time for panel to open and load content

            game_info_panel = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.game_info_panel_widget')))
            tags_elements = game_info_panel.find_elements(By.XPATH, ".//tr[td='Tags']/td[2]/a")
            genres_elements = game_info_panel.find_elements(By.XPATH, ".//tr[td='Genre']/td[2]/a")

            tags = ', '.join([tag.text for tag in tags_elements]) if tags_elements else None
            genres = ', '.join([genre.text for genre in genres_elements]) if genres_elements else None

            new_row = pd.DataFrame({'name': [game_name], 'tags': [tags], 'genres': [genres]})
            results_df = pd.concat([results_df, new_row], ignore_index=True)
            logging.info(f"Data collected for {game_name}: Tags={tags}, Genres={genres}")
        else:
            logging.info(f"No match found for {game_name}")

    except (NoSuchElementException, TimeoutException, UnexpectedAlertPresentException) as e:
        logging.error(f"Error processing {game_name}: {str(e)}")

driver.quit()

# 결과 CSV 파일로 저장
results_df.to_csv('/Users/AIFFELthon/final/data/null/results_genre.csv', index=False)
logging.info("Results saved to CSV.")
