# guru


# 프로젝트 개요
이 프로젝트는 게임 데이터를 분석하고 모델링하는 다양한 코드와 웹 애플리케이션을 포함하고 있습니다.

## `mj` 폴더 구조
`mj` 폴더는 주요 코드와 데이터를 포함하고 있으며, 아래와 같은 구조로 되어 있습니다.

### 1. 코드 폴더 (`code`)

#### find 폴더
- `colums.py`: 컬럼 관련 작업을 수행하는 스크립트입니다.
- `find_developers_steam.py`: Steam에서 개발자를 찾는 스크립트입니다.
- `find_game_series.py`: 게임 시리즈를 찾는 스크립트입니다.
- `find_mode.py`: 게임 모드를 찾는 스크립트입니다.
- `find_name.py`: 게임 이름을 찾는 스크립트입니다.
- `find_platform.py`: 게임 플랫폼을 찾는 스크립트입니다.
- `find_similar_game_01.py`: 유사한 게임을 찾는 첫 번째 스크립트입니다.
- `find_similar_game_02.py`: 유사한 게임을 찾는 두 번째 스크립트입니다.
- `fine_genre.py`: 게임 장르를 찾는 스크립트입니다.
- `fine_genre_Nintento.py`: 닌텐도 게임 장르를 찾는 스크립트입니다.
- `fine_null_genre.py`: 장르가 없는 게임을 찾는 스크립트입니다.
- `fine_series.py`: 게임 시리즈를 찾는 스크립트입니다.

#### missing_value 폴더
- `missing_data_treatmen.ipynb`: 누락된 데이터를 처리하는 노트북입니다.
- `missing_value.ipynb`: 누락된 데이터를 처리하기 전 데이터 확인하는 노트북입니다.

#### modelling 폴더
- `Annoy.ipynb`: Annoy 알고리즘을 사용한 모델링 노트북입니다.
- `Content-based_Filtering.ipynb`: 콘텐츠 기반 필터링 모델링 노트북입니다.
- `NearestNeighbors.ipynb`: 최근접 이웃 알고리즘을 사용한 모델링 노트북입니다.
- `index.html`: 테스트 모델링 결과를 보여주는 HTML 파일입니다.
- `model_test.ipynb`: 모델 테스트를 위한 노트북입니다.
- `server.ipynb`: 테스트 서버 관련 작업을 수행하는 노트북입니다.
- `server.py`: 테스트 서버 관련 작업을 수행하는 파이썬 스크립트입니다.

### 2. 웹 폴더 (`web`)

#### data 폴더
- `.DS_Store`: 시스템 파일입니다.
- `cleansing_game_data.csv.zip`: 게임 데이터 정제 파일입니다.
- `data.csv.zip`: 데이터 파일입니다.
- `data.feather.zip`: 데이터 파일입니다.

#### static 폴더
- `css/styles.css`: 스타일 시트 파일입니다.
- `images/ : 이미지 파일입니다.
- `js/scripts.js`: 자바스크립트 파일입니다.

#### templates 폴더
- `index.html`: 웹 페이지 템플릿 파일입니다.
- `app.py`: 웹 애플리케이션 메인 파일입니다.
- `main.py`: 추천 시스템 알고리즘 파일입니다.

## `yebin` 폴더 구조
`yebin` 폴더는 주요 코드와 데이터를 포함하고 있으며, 아래와 같은 구조로 되어 있습니다.

### 1. 코드 폴더 (`code`)
- `igdb_processing.ipynb`: igdb 데이터를 전처리하는 노트북입니다.
- `test.ipynb`: 가공된 igdb 데이터를 이용해 실험 및 평가하는 노트북입니다.
- `rawg_processing.ipynb`: rawg 데이터를 전처리하는 노트북입니다.
- `web_recommend.ipynb`: rawg 데이터로 필터링 및 추천 과정을 확인하는 노트북입니다.
- `main.py`: 웹 구현에 사용되는 추천 시스템 알고리즘 파일입니다.

### 2. 데이터 폴더 (`data`)
- `igdb_pc_score.csv`: 실험 후 평가 지표를 통해 기록한 점수 파일입니다.
- `final_data.zip`: 정제된 게임 데이터 파일입니다.
  - `final_igdb_pc.csv`: 실험 및 평가를 위한 정제된 igdb(플랫폼:pc) 게임 정보 파일입니다.
  - 'final_rawg.csv': 실제 추천 시스템에 사용되는 정제된 rawg 게임 데이터입니다.

