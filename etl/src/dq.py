from pathlib import Path
import pandas as pd

_REPORT_PATH = Path("./data/processed/dq_report.csv")
_REQUIRED_COL = ['patient_id', 'visit_id', 'collected_at', 'test_name', 'value', 'unit']

def dq_check(path:str = './data/processed/labs_clean.csv') :

    p = Path(path)

    # 파일 경로 확인, 경로를 못 찾으면 FileNotFoundError 발생
    if not p.exists :
        raise FileNotFoundError(
            '파일을 찾을 수 없습니다. 경로를 다시 확인해주세요'
        )
    
    # 파일을 찾으면 DataFrame으로 만들기 
    df = pd.read_csv(p)        

    # 1) 필수 column확인 / 없으면 error_log에 저장
    if set(_REQUIRED_COL) - set(df.columns):
        save_issue('필수 Column이 부족합니다')
        raise ValueError('필수 Column이 부족합니다')

    # 2) 중복 행 체크 
    dup = df.duplicated()
    dup_cnt = int(dup.sum())
    if dup_cnt > 0 : 
        save_issue(f'중복된 행이 {dup_cnt} 존재합니다.', issue_type='duplicate_row')

    # 3) 날짜 파싱 실패 / 비정상 시간 체크
    # coolected_at을 파싱한 후 에러가 나서 Nan으로 변한 곳이 있으면 issue 저장
    df['collected_at'] = pd.to_datetime(df['collected_at'],errors='coerce')
    bad_parsing = df['collected_at'].isna().sum()
    if bad_parsing > 0 : 
        save_issue(f'날짜 파싱 실패 {bad_parsing}', 'datetime_parsing')

    # 4) 수치값 비정상 체크
    # value 에 NaN이 있거나 value의 값이 음수일 경우 save_issue로 저장
    bad_value = df['value'].isna() | (df['value'] < 0)
    bad_value_coutn = int(bad_value.sum())
    if bad_value_coutn> 0 : 
        # 
        bad_value_idx = df.index[bad_value].to_list()[:10]
        save_issue(f'value 결측치/음수값 {bad_value}: 예시 index{bad_value_idx}', 'bad_value')

    # 5) 범위 체크
    # TEMP: 30~45°C 밖이면 이슈
    # WBC: 0~100 밖이면 이슈
    # CRP: 0~500 밖이면 이슈
    test_range = df[['test_name', 'value']]

    temp_value = test_range.loc[test_range['test_name'] == 'TEMP', 'value']
    wbc_value = test_range.loc[test_range['test_name'] == 'WBC', 'value']
    crp_value = test_range.loc[test_range['test_name'] == 'CRP', 'value']

    # any() :: 앞의 값 중 하나라도 True 라면 True
    # all() :: 모두 True 면 True
    if (temp_value[(temp_value < 30) | (temp_value > 45)]).any(): 
        save_issue('TEMP의 값이 정상범위를 벗어났습니다', issue_type='out_of_range')
    if (wbc_value[(wbc_value < 0) | (wbc_value > 100)]).any(): 
        save_issue('WBC의 값이 정상범위를 벗어났습니다', issue_type='out_of_range')
    if (crp_value[(crp_value < 0) | (crp_value > 500)]).any(): 
        save_issue('CRP의 값이 정상범위를 벗어났습니다', issue_type='out_of_range')
        

# 이슈가 발생하면 해당 이슈를 dq_report에 저장함
def save_issue(msg:str, issue_type:str, ) :
    _REPORT_PATH.parent.mkdir(parents= True, exist_ok= True)

    error_log = pd.DataFrame([{
        'issue' : msg, 
        'timestamp' : pd.Timestamp.now(),
        'issue_type': issue_type,
        }])
    
    error_log.to_csv(_REPORT_PATH, mode='a', header=not _REPORT_PATH.exists(), encoding='utf-8', index=False)
    print(f'issue가 log에 저장되었습니다 : {msg}')


     
    '''
    (1) 필수 컬럼 결측 체크
    patient_id, visit_id, collected_at, test_name, value, unit
    하나라도 비면 “결측” 이슈로 기록


    (2) 중복 행 체크(완전 동일 행)
    전체 컬럼 기준 duplicated()로 중복 레코드 탐지

    (3) 날짜 파싱 실패 / 비정상 시간 체크
    collected_at이 NaT(파싱 실패)면 이슈

    (선택) 미래 날짜(오늘 이후)면 이슈
    (4) 수치값 비정상 체크

    value가 NaN이면 이슈
    value < 0이면 이슈(검사 값은 보통 음수 불가)

    (5) 범위 기반 “상식적” 이상치 체크(룰)
    AI가 아니라 상식 범위 룰이야.
    TEMP: 30~45°C 밖이면 이슈
    WBC: 0~100 밖이면 이슈
    CRP: 0~500 밖이면 이슈
    (이 범위는 “경고용”이라 정확한 임상 기준이 아니라, 데이터 오류 탐지 목적)
    '''
