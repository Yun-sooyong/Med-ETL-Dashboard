# 데이터 프레임 반환, 데이터 읽기 

import pandas as pd
from pathlib import Path

# path 인자는 기본적으로 str을 받고 기본값을 가짐 
def read_raw_data(path:str = './data/raw/labs_sample.csv') :
    p = Path(path)
    # 필수적으로 있어야 하는 columns
    REQUIRED_COL = {'patient_id', 'visit_id', 'collected_at', 'test_name', 'value', 'unit'}
    
    # 파일을 찾을 수 없으면 에러를 발생 시킴
    if not p.exists :
        raise FileNotFoundError('파일을 찾을 수 없습니다. 경로를 다시 확인해주세요.')
    
    df = pd.read_csv(p)

    if REQUIRED_COL - set(df.columns) :
        raise ValueError(f'필수 칼럼이 부족합니다. 다시 확인해 주세요. {REQUIRED_COL - set(df.columns)}')

    return df
# __name__ 은 import 되었을 떄는 실행되지 않음
if __name__ == '__main__':
    df = read_raw_data()
    print(df.head())