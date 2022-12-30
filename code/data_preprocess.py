import pandas as pd

from utils import find_xy, get_api, trans_wtm2wgs84

#결빙사고 데이터 다운로드
get_api().to_csv("../data/org/도로교통공단_결빙사고_다발지역_은평구.csv")

##
people=pd.read_csv('../data/LOCAL_PEOPLE_GU_2020.csv',encoding='euc-kr',index_col=False)
map_code=pd.read_csv('../data/법정동.csv',encoding='euc-kr',index_col=False)

people_data = people.drop(labels = ['기준일ID','시간대구분'], axis=1)
map_code_data=map_code.drop_duplicates('시군구코드')

df=pd.merge(people_data, map_code_data, left_on = '자치구코드', right_on = '시군구코드')
df_data=df.drop(['시군구코드'],axis=1)

data=pd.pivot_table(df_data, index = ['자치구코드','시군구명'], aggfunc = 'sum')
data.to_csv('../data/2020.csv', encoding="cp949")

#제설함 좌표변환
jaeseorham = pd.read_csv("../data/org/서울시_제설함_위치정보.csv", encoding="cp949")
trans_wtm2wgs84(jaeseorham).to_csv("../data/seoul_jaeseorham.csv", encoding = "cp949")

#노인의료복지 시설
grand_medical = pd.read_csv('../data/org/서울특별시_은평구_노인의료복지시설_20220701.csv', encoding='cp949')
find_xy(grand_medical, '소재지 도로명주소').to_csv("../data/grand_medical.csv")

#어린이보호구역
child = pd.read_csv('../data/org/서울특별시_어린이_보호구역_지정현황_20201231.csv', encoding='cp949')
child[child['자치구명'] == '은평구']
find_xy(child, '도로명 주소(동명)').to_csv("../data/child_safe_site.csv")

#급경사지
data = pd.read_csv('../data/org/행정안전부_급경사지 현황_20211231.csv', encoding='cp949')
data = data[data['시군구'] == '은평구']