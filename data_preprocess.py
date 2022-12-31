import pandas as pd

from utils import find_xy, get_api, trans_wtm2wgs84

# 결빙사고 데이터 다운로드 (freezing)
get_api().to_csv("./data/org/도로교통공단_결빙사고_다발지역_은평구.csv")

# 제설함 좌표변환
jaeseorham = pd.read_csv("./data/org/서울시_제설함_위치정보.csv", encoding="cp949")
trans_wtm2wgs84(jaeseorham).to_csv(
    "./data/seoul_jaeseorham.csv", index=False)

# 노인의료복지 시설 (grand_medical)
grand_medical = pd.read_csv(
    './data/org/서울특별시_은평구_노인의료복지시설_20220701.csv', encoding='cp949')
find_xy(grand_medical, '소재지 도로명주소', '시설명').to_csv("./data/grand_medical.csv", index=False)

# 어린이보호구역 (child)
child = pd.read_csv(
    './data/org/서울특별시_어린이_보호구역_지정현황_20201231.csv', encoding='cp949')
child = child[child['자치구명'] == '은평구']
find_xy(child, '도로명 주소(동명)', '시설명').to_csv("./data/child_safe_site.csv", index=False)

# 급경사지 (warnway)
warnway = pd.read_csv(
    './data/org/행정안전부_급경사지 현황_20211231.csv', encoding='cp949')
warnway[warnway['시군구'] == '은평구']#.to_csv("./data/warnway.csv", index=False) #수동

# 서울 전체 생활인구수 1년치 합치기 / 구 코드
people = pd.read_csv('./data/org/LOCAL_PEOPLE_GU_2021.csv', encoding='euc-kr')
people = people[['시간대구분', '자치구코드', '총생활인구수']]

g_value_data = list()
for gcode in dict.fromkeys(people['자치구코드']).keys():
    value = people[people['자치구코드'] == gcode]['총생활인구수'].sum()
    g_value_data.append([str(gcode), value])

code = pd.read_csv('./data/org/법정동코드_조회자료.csv', encoding='cp949')

dcode_name = list()
for dcode, name in zip(code['법정동코드'], code['법정동명']):
    key = name.split()
    if len(key) == 2:
        key = key[1]
        dcode = str(dcode)[:5]
        dcode_name.append([dcode, key])

g_value_df = pd.DataFrame(g_value_data, columns=['자치구코드', '총생활인구수'])
code_name_df = pd.DataFrame(dcode_name, columns=['자치구코드', '법정구명'])
pd.merge(g_value_df, code_name_df, on='자치구코드', how='inner').to_csv(
    "./data/seoul_people.csv", index=False)
