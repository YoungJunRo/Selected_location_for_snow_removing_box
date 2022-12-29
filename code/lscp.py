# Workers : 심미경
# Refactoring : 노영준

import pandas as pd
from haversine import haversine # 위경도 데이터 거리 계산시 최단거리 계산해주는 라이브러리

data = pd.read_csv('c:/result.csv', encoding='cp949')
data_dic = {}

for i in data.index:
    data_dic[data.loc[i, 'juso']] = (data.loc[i, 'lat'], data.loc[i, 'lon'])

data_list = []

for i in data_dic.values():
    data_list.append(i)

list_num = len(data_list)

x = 0
y = 0

cnt = 0
cnt_del = 0

R = 832 # 반지름 208인데..?

print(data_list[0])

while x != len(data_list)-1:
    y += 1
    try:
        distance = int(haversine(data_list[x], data_list[y], unit='m'))
    except:
        break
    if y >= len(data_list)-1:
        x += 1
        y = x+1
        continue

    if distance < R:
        print(x, y, distance)
        del data_list[y]
        y -= 1
        cnt_del += 1

    else:
        cnt += 1

print(cnt_del)

# validation
x = 0
y = 0
while x != len(data_list)-1:
    y += 1
    try:
        distance = int(haversine(data_list[x], data_list[y], unit='m'))
    except:
        break
    print(distance)
    if y >= len(data_list)-1:
        x += 1
        y = x+1

print("data 수", len(data_list))
print('-'*20)
print("후보군 선정 위치 : ", data_list)


df = pd.DataFrame(data_list)
df.to_csv('lscp.csv')