# 데이터 전처리(변환, 정렬 등)
import pandas as pd

REQUIRED_COL = ['patient_id', 'visit_id', 'collected_at', 'test_name', 'value', 'unit']

'''
(1) 컬럼명 정리
    공백 제거, 소문자 통일(이미 맞으면 스킵 가능)

    최종 컬럼명을 위 6개로 고정
(2) 타입 변환
    collected_at: datetime으로 변환
    value: 숫자(float)로 변환 (문자 섞이면 NaN 처리)
(3) 결측치 최소 처리(초보용)
    patient_id, visit_id, test_name이 비면 그 행 삭제
    value가 NaN이면 그 행 삭제(오늘은 단순하게)
(4) 정렬
    patient_id, visit_id, collected_at 기준 오름차순 정렬
(5) 룰 기반 이상 플래그 추가(아주 간단)
    flag_abnormal(bool) 컬럼 추가:
    CRP이고 value > 10이면 True
    WBC이고 value > 12이면 True
    TEMP이고 value >= 38.0이면 True
    그 외 False
'''

def clean_up(df: pd.DataFrame) :
    clear = df.copy()
    # 1) 컬럼명 정리 (공백 제거, 소문자 통일)
    clear.columns = [col.strip().lower() for col in clear.columns]

    # 2) 최종 컬럼명을 위 6개로 고정
    clear = clear[REQUIRED_COL]

    # 3) 타입 변환
    '''
        타입 변환 방식 2종류 + 다중 열 변환 
        pd.astype()    :: clear['collected_at'] = clear['collected_at'].astype(float)
        pd.to_numeric  :: clear['collected_at'] = pd.to_datetime(clear['collected_at'], errors='coerce')
        다중 열 변환 :: clear = clear.astype({'collected_at' : 'float', 'test_name': 'str'})

        errors = 'coerce' 를 작성하면 숫자로 변환이 불가능한 문자는 NaN으로 표시 해줌 
    '''

    clear['collected_at'] = pd.to_datetime(clear['collected_at'], errors='coerce')
    clear['value'] = pd.to_numeric(clear['value'], errors='coerce')

    # 4) 결측치 최소 처리 
    '''
        dropna :: NaN 값(결측)이 있는 행을 전부 제거 
        dropna(subset=[]) subset은 list에 레이블을 지정하면 지정된 레이블만 dropna를 실행
    '''
    clear = clear.dropna(subset=['patient_id', 'visit_id', 'test_name', 'value'])

    # 5) patient_id, visit_id, collected_at 기준 오름차순 정렬
    '''
        sort_values :: 값 기준으로 정렬
        by :: 레이블 지정 / 여러 레이블을 지정하면 list형식을 주고 단일 레이블은 str로 줌 
        by 에 리스트 값이 들어갈 경우 앞쪽 순서대로 정렬됨
        sort_values로 정렬한 이후 인덱스는 정렬이 안 되어있음 인덱스의 순서도 정렬에 맞춰주기 위해서 reset_index를 사용해줌
    '''
    clear = clear.sort_values(by=['patient_id', 'visit_id', 'collected_at']).reset_index(drop=True)

    # 6) 룰 기반 이상 플래그 추가
    '''
    flag_abnormal(bool) 컬럼 추가:
    CRP이고 value > 10이면 True
    WBC이고 value > 12이면 True
    TEMP이고 value >= 38.0이면 True
    그 외 False
    '''
    clear['flag_abnormal'] = False
    is_CRP = (clear['test_name'] == 'CRP') & (clear['value'] > 10)
    is_WBC = (clear['test_name'] == 'WBC') & (clear['value'] > 12)
    is_TEMP = (clear['test_name'] == 'TEMP') & (clear['value'] >= 38.0)

    # loc[행(row), 열(column)] = value :: 값 저장하기 
    # 조건을 만족하면 해당 행열 위치의 값을 True로 변경 
    clear.loc[is_CRP | is_WBC | is_TEMP, 'flag_abnormal'] = True

    return clear