import pandas as pd

people=pd.read_csv('../data/LOCAL_PEOPLE_GU_2020.csv',encoding='euc-kr',index_col=False)
map_code=pd.read_csv('../data/법정동.csv',encoding='euc-kr',index_col=False)

people_data = people.drop(labels = ['기준일ID','시간대구분'], axis=1)
map_code_data=map_code.drop_duplicates('시군구코드')

df=pd.merge(people_data, map_code_data, left_on = '자치구코드', right_on = '시군구코드')
df_data=df.drop(['시군구코드'],axis=1)

data=pd.pivot_table(df_data, index = ['자치구코드','시군구명'], aggfunc = 'sum')
data.to_csv('2020.csv', encoding="cp949")