# 의료검사 결과 ETL + 대시보드

- ETL(Extract, Transform, Load)이란?

    데이터를 추출(Extract)하고, 분석에 맞게 정리 및 변환(Transform)하여, 데이터 웨어하우스나 데이터 레이크로 적재(Load)하는 데이터 엔지니어링 프로세스

## 🌡️ 소개

- CSV(검사결과) → DB 적재 → 전처리/품질검사 → API → 대시보드 → Docker로 배포를 연습하기 위한 토이 프로젝트입니다.

## 🌡️ 프로젝트를 진행한 이유

- 국비지원으로 의료ai 관련 수업을 듣게 되어 예습을 위해 진행해본 프로젝트
- 임의로 제작한 간단한 csv를 사용해 데이터 처리를 하는 연습을 해보기 위한 토이 프로젝트

## 🌡️ 기능 

- **ETL 파이프라인**
  - CSV 원천 데이터를 읽고(Extract) → 정리/정규화(Transform) → DB에 적재(Load)

- **데이터 품질관리(DQ)**
  - 결측/중복/이상값 등을 검사하고 결과 리포트를 남김

- **규칙 기반 이상치/알림 플래그**
  - 검사 항목별 기준치로 abnormal 여부를 계산해 저장(모델 없이 규칙 기반)

- **조회/집계 API**
  - 환자/검사 결과 조회, 이상치 통계/트렌드 같은 집계 결과를 REST API로 제공

- **대시보드**
  - 환자별 검사 이력/추세 확인, 이상 플래그 필터링 및 요약 통계 표시

- **컨테이너 기반 실행**
  - docker-compose로 DB + API + Dashboard를 한 번에 실행 가능

## 🌡️ 기술 스택

### 프론트엔드

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

### 백엔드

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)

### 데브옵스

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?logo=docker&logoColor=white)

### 도구 및 라이브러리

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

### 패키지 매니저

![pip](https://img.shields.io/badge/pip-3775A9?logo=pypi&logoColor=white)

### 배포

![Docker Compose](https://img.shields.io/badge/Deploy-Docker%20Compose-2496ED?logo=docker&logoColor=white)

## 🌡️ 구조

```shell
.
├── api
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── db.py
│       ├── main.py
│       ├── routes
│       │   ├── labs.py
│       │   ├── patients.py
│       │   └── stats.py
│       └── schemas.py
├── dashboard
│   ├── app.py
│   └── requirements.txt
├── data
│   ├── processed
│   └── raw
│       └── labs_sample.csv
├── docker
│   ├── Dockerfile.api
│   ├── Dockerfile.dashboard
│   └── Dockerfile.etl
├── docker-compose.yml
├── etl
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── config.py
│       ├── dq.py
│       ├── extract.py
│       ├── load.py
│       ├── run_etl.py
│       └── transform.py
├── mk_sample.ipynb
├── README.md
└── sql
    └── 001_init.sql
```

## 🌡️ 진행도
<details>
<summary>진행사항</summary>

- Day1 : 개발 환경 준비, 샘플 데이터 작성, 프로젝트 폴더 구성

- Day2 : 데이터 처리 (데이터 추출, 분석, 저장)

- Day3 : 
</details>