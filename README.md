# Selected_location_for_snow_removing_box
머신러닝을 활용한 은평구 제설함 추가 배치 개수, 위치를 설정하는 프로젝트

## Data update with refactoring date : 2022-12-27 ~ 2022-12-31

## How To use

- Run data_preprocess.py (Check warnway.csv > fixed manually)
- Run status.py (For check now status)
- Run mclp.ipynb (Need Jupyter notebook)

## Model

### LSCP - Del (코드에 사용된 데이터 확인 불가)
- 동국대학교 산업시스템공학과 심미경 개발

### MCLP

Gurobi Solver를 활용하여 Simple MIP(Mixed Integer Linear Programming)를 통해 Maximum Coverage Location Problem 해결


## Requirements

- `geopandas==0.9.0`
- `branca==0.5.0`
- `folium==0.13.0`
- `gurobipy==9.1.2`
- `mip==1.13.0`
- `numpy==1.19.5`
- `pandas==1.1.5`
- `scipy==1.5.4`
- `shapley==1.0.3`
- `selenium==3.141.0`
- `tqdm==4.64.1`

## Data

### Data list
- [행정안전부_급경사지 현황_20211231.csv](https://www.data.go.kr/data/15083292/fileData.do)
- [서울시 제설함 위치정보.csv](https://data.seoul.go.kr/dataList/OA-1253/S/1/datasetView.do)
- [서울특별시_어린이_보호구역_지정현황_20201231.csv](https://www.data.go.kr/data/15094988/fileData.do?recommendDataYn=Y)
- [서울특별시_은평구_노인의료복지시설_20220701.csv](http://stat.ep.go.kr/wt/wt50/wt501020.do?data_meta_id=240#contentSheet)
- [도로교통공단_결빙사고 다발지역 API](https://www.data.go.kr/data/15058135/openapi.do)
- [skorea_municipalities_geo_simple.json](https://pinkwink.kr/1003)
- [LOCAL_PEOPLE_GU_2021.csv](https://data.seoul.go.kr/dataList/OA-15439/S/1/datasetView.do)
- [법정동코드_조회자료.csv](https://www.code.go.kr/stdcode/regCodeL.do)

### Problem
- seoul_smoke_point > 강동구 데이터 존재하지 
