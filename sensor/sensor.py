# 필요한 패키지를 import
from pyzbar import pyzbar
import argparse
import datetime
import time
from picamera import PiCamera
import cv2
import boto3
import pygame
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import imutils
import datetime

print(tf.__version__)

#audio
pygame.mixer.init()

#test db
dynamodb = boto3.resource('dynamodb', region_name='REGION_NAME', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')
table = dynamodb.Table('ace_test')
response = table.scan()
items = response['Items']
item = {}
item_index = 0
item_listob = []
 
cap = cv2.VideoCapture(-1)
flag = True
main_category = ['glass', 'metal', 'paper', 'plastic', 'plastic bag', 'trash']
recycle_arr = []
current_place = 5
point_score = 0

interpreter = tf.lite.Interpreter(model_path='model_unquant.tflite')
interpreter.allocate_tensors()
        
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']
sd = pygame.mixer.Sound('./voice/Ask_QR.wav')
sd.set_volume(0.5)
sd.play()
print("show your QR code")
while(cap.isOpened() and flag):
    ret, frame = cap.read()
    
    if(ret):
        frame = imutils.resize(frame,  height=300, width=500)
        cv2.imshow('barcode', frame)
        
        #프레임에서 QRcode(barcodes)를 찾고 각 바코드를 디코드
        barcodes = pyzbar.decode(frame)
        if len(barcodes) > 0:
        #decode
            barcode = barcodes[0]
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            #print(text)
            user_id = text.split(" ")[0]
            
            #print(user_id)
            for i in items:
                if i['id'] == user_id:
                    item = i
                    break
                item_index += 1
            flag=False
            
        k = cv2.waitKey(1) & 0xFF
        if (k==27):
            break
      
print("confirm your QR code")
item_listob = item['list_object']
sd = pygame.mixer.Sound('./voice/Confirm_QR.wav')
sd.set_volume(0.5)
sd.play()
cap.release()
cv2.destroyAllWindows()

answer = input("Do you want to start? Y/N: ")
if answer == 'Y' or answer == 'y':
    flag = True

cap = cv2.VideoCapture(-1)
sd = pygame.mixer.Sound('./voice/Ask_Show.wav')
sd.set_volume(0.5)
sd.play()
print("show your recycle object")
while(cap.isOpened() and flag):
    ret, frame = cap.read()
    
    if(ret):
        frame = imutils.resize(frame, height=300, width=500)
        cv2.imshow('object', frame)
        #input_shape:[1, 224, 224, 3]
        f_data = np.ndarray(shape=input_shape, dtype=np.float32)
        #image = frame.resize(224, 224)
        #cv2.imwrite('current.jpg', frame)
        #image = Image.open('current.jpg')
        #f = frame
        image = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_AREA)
        #image = ImageOps.fit(image, (224, 224), Image.ANTIALIAS)
        image_arr = np.asarray(image)
        normalized_img = (image_arr.astype(np.float32)/127.0)-1
        f_data[0] = normalized_img
        interpreter.set_tensor(input_details[0]['index'], f_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        temp_rcy = np.argmax(output_data[0])
        #print(output_data[0][2])
        #print(main_category[temp_rcy])
        #print(output_data[0][temp_rcy])
        if output_data[0][temp_rcy] > 0.997 and temp_rcy not in recycle_arr:
            print(main_category[temp_rcy], output_data[0][temp_rcy])
            recycle_arr.append(temp_rcy)
            #about db
            for i in item_listob:
                if i['recycle_element'][temp_rcy] == '1':
                    i['recycle_element'][temp_rcy] = ''
                    i['recycle_place'].append(current_place)
                    recycle_arr = []
                    sd = pygame.mixer.Sound('./voice/' +str(temp_rcy) + '.wav')
                    sd.set_volume(0.5)
                    sd.play()
                    #point
                    point_score += 1
                            
            cv2.imwrite('./image/' + str(main_category[temp_rcy]) + str(output_data[0][temp_rcy]) + '.jpg', frame)
            time.sleep(5)
            
        k = cv2.waitKey(1) & 0xFF
        if (k==27):
            break
        
        
temp_p = [str(datetime.datetime.now()), str(point_score)]
item['point'].append(temp_p)
item['list_object'] = item_listob
print("your db change")
print(item)
#print(item_index)
items[item_index] = item
#print(items)
table.put_item(Item=item)

cap.release()
cv2.destroyAllWindows()
