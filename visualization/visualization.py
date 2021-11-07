import boto3
from boto3.dynamodb.conditions import Key, Attr
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

dynamodb = boto3.resource('dynamodb', region_name='REGION_NAME', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')
place_id = ['A area', 'B area', 'C area', 'D area', 'E area']
recycle_id = ['glass', 'metal', 'paper', 'plastic', 'plastic bag']
explode = [0.05, 0.05, 0.05, 0.05, 0.05]

table = dynamodb.Table('ace_test')
response = table.scan()
items = response['Items']

recycle_place = [0, 0, 0, 0, 0]
buy_place = [0, 0, 0, 0, 0]
notrecycle_object = [0, 0, 0, 0, 0]
recycle_object = [0, 0, 0, 0, 0]
recycle_element = [0, 0, 0, 0, 0]

for i in items:
    for l in i['list_object']:
        for r in l['recycle_place']:
            temp = recycle_place[int(r)-1]
            recycle_place[int(r)-1] = temp+1

        temp = buy_place[int(l['buy_place'])-1]
        buy_place[int(l['buy_place'])-1] = temp+1

        cnt = 0
        for o in l['recycle_element']:
            if o != "":
                if int(o) == 1:
                    notrecycle_object[cnt] = notrecycle_object[cnt]+1
                    recycle_element[cnt] = recycle_element[cnt]+1
                if int(o) == 2:
                    recycle_object[cnt] = notrecycle_object[cnt]+1
                    recycle_element[cnt] = recycle_element[cnt]+1
            cnt = cnt+1

plt.subplot(221)
plt.pie(recycle_place, labels=place_id, autopct='%.1f%%', startangle=260, counterclock=False, explode=explode, shadow=True)

plt.subplot(222)
wedgeprops = {'width':0.7, 'edgecolor':'w', 'linewidth':5}
plt.pie(buy_place, labels=place_id, autopct='%.1f%%', startangle=260, counterclock=False, wedgeprops=wedgeprops)

plt.subplot(223)
x = np.arange(len(recycle_object))
plt.bar(x, notrecycle_object)
plt.xticks(x, recycle_id)

plt.subplot(224)
plt.bar(x, recycle_element)
plt.xticks(x, recycle_id)
plt.show()

plt.savefig('recycle.png')
