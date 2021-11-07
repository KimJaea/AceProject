import cv2
import pyzbar.pyzbar as pyzbar
import boto3
from boto3.dynamodb.conditions import Key, Attr
from playsound import playsound
import datetime as dt
import csv

dynamodb = boto3.resource('dynamodb', region_name='REGION_NAME', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')
used_codes = []
object_cnt = []
user_id = ''
market_place = 1 #서울 구별 인코딩

"""
table = dynamodb.Table('UserData-a2xakivalvamflwr2cpfppaxva-staging')
response = table.scan()
items = response['Items']
print(items[0])
"""

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

non_exit = True
user_id = input("아이디(전화번호)를 입력하세요: ")

while non_exit:
    success, frame = cap.read()
    cv2.imshow("QRcode Barcode Scan", frame)

    for code in pyzbar.decode(frame):
        my_code = code.data.decode('utf-8')
        print("my: ", my_code)
        cv2.destroyAllWindows()
        playsound("./qrbarcode_beep.wav")
        if my_code not in used_codes:
            cnt = input("개수를 입력하세요: ") 
            object_cnt.append(cnt)
            print("결제 되었습니다: ", my_code)
            used_codes.append(my_code)

        elif my_code in used_codes:
            print("이미 결제된 상품입니다")

        else:
            pass

    ret = cv2.waitKey(5)
    if ret == 27: 
        non_exit = False

#물건 사면, name_1_y/m/d/h/m가 기본 형식 (1은 물건 구입 개수 의미)
table = dynamodb.Table('UserData-a2xakivalvamflwr2cpfppaxva-staging')#ace_user_database
x = dt.datetime.now()
now_time = str(x.year)+"/"+str(x.month)+"/"+str(x.day)+"/"+str(x.hour)+"/"+str(x.minute)
print(now_time)

f = open('./emart_recycle_list_5.csv', 'r', encoding='cp949')
rdr = csv.reader(f)

#db에 id가 있는지 확인, 없으면 새로 오브젝트를 만들고 있으면 추가
response = table.scan(
    FilterExpression = Attr('user_id').eq(user_id)
)
print(response['Items'])

if len(response['Items']) == 0:
    response['Items'].append({
            'id': user_id,
            'user_id': user_id,
            'user_pw': '',
            'list_object': [],
            'point': []
        })

print(response)


buy_object = {
    'name':'',
    'recycle_element':[],
    'buy_place': '',
    'recycle_place':[]}

print("user_codes: ", used_codes)
#csv에서 읽어와서 db 저장
for o in used_codes:
    print("o: ", o)
    for line in rdr:
        if line[6][0:-1] == o:
            o_name = line[0] + "_" + str(cnt) + "_" + now_time
            buy_object = {
                'name': o_name,
                'recycle_element': [line[1], line[2], line[3], line[4], line[5]],
                'buy_place': market_place,
                'recycle_place': []
            }
            print("========================")
            print(buy_object)
            print("========================")
            response['Items'][0]['list_object'].append(buy_object)
            break

print("--------------------------")
print(response["Items"])
print("----------------------------")
item= response['Items'][0]
table.put_item(Item=item)