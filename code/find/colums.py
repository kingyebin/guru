import glob
import os
import pandas as pd

# 경로를 지정하고 해당 디렉토리에서 모든 CSV 파일을 찾기
folder_path = '/Users/AIFFELthon/final/data/'
csv_files = glob.glob(os.path.join(folder_path, '**', '*.csv'), recursive=True)

# 각 CSV 파일의 컬럼을 확인하고 출력
for file in csv_files:
    try:
        df = pd.read_csv(file, nrows=0)  # 첫 줄만 읽어서 컬럼 확인
        print(f"File: {os.path.basename(file)}")
        print(f"Columns: {list(df.columns)}\n")
    except Exception as e:
        print(f"Error reading {file}: {e}")