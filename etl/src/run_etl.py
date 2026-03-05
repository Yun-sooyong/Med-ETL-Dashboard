# 실행 위치

from pathlib import Path

from extract import read_raw_data
from transform import clean_up
from dq import dq_check

# csv를 저장하고 불러오는 위치 지정 
_RAW_PATH = './data/raw/labs_sample.csv'
_CLEAN_PATH = './data/processed/labs_clean.csv'

'''
extract.py의 함수 호출 → raw df 받기
transform.py의 함수 호출 → clean df 받기
data/processed/labs_clean.csv로 저장
로그 출력:
raw rows → clean rows
abnormal True 개수
저장 경로
'''


def main() :
    # extract 호출
    raw_df = read_raw_data(_RAW_PATH)

    # transform 호출
    clean_df = clean_up(raw_df)

    # labs_clean 저장
    save_folder = Path(_CLEAN_PATH)
    # exist_ok =True :: 이미 존재하는 폴더일 경우 에러를 내지 않고 넘어감 
    # parents = True :: 경로에 있는 부모 폴더가 존재하지 않는 경우 만듦
    # parent 부모 파일까지만 생성 
    save_folder.parent.mkdir(exist_ok=True, parents=True)
    # index = False :: csv로 저장할 때 index를 같이 저장하지 않음 
    clean_df.to_csv(_CLEAN_PATH, index=False, encoding='utf-8')

    dq_check(_CLEAN_PATH)

    # 로그 출력 
    print(f"raw rows {len(raw_df)} -> clean rows {len(clean_df)}")
    print(f"abnormal True : {int(clean_df['flag_abnormal'].sum())}") 
    print(f"saved : {_CLEAN_PATH}")


if __name__ == "__main__" :
    main()