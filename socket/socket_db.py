import socket
import boto3

HOST = '000.000.000.000'
PORT = 8080
SOCKET_SIZE = 1024

temp_list_f = []
flag = True
data_str = ""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("set socket")
server_socket.bind((HOST, PORT))
print("binding")
server_socket.listen()
print("listening")
client_socket, addr = server_socket.accept()

print('Connect by', addr)

while True:
    data = ""
    if flag:
        data = client_socket.recv(SOCKET_SIZE)
        
    if not data:
        break
    
    print('Received from', addr)
    data_decode = str(data, 'cp949')
    data_decode = data_decode.replace('t', '')
    user_id = data_decode.replace(' ', '')
    
    if !user_id.isdigit():
        break
    
    
    dynamodb = boto3.resource('dynamodb', region_name='REGION_NAME', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')
    table = dynamodb.Table('ace_test')
    response = table.scan()
    items = response['Items']
    temp_item = {}
    for item in items:
        if item['id'] == user_id:
            temp_item = item
            break
        
    data_str = str(temp_item)
    
print("sending...")
#client_socket.send(data_str.encode())
print(client_socket.sendall(data_str.encode()))

client_socket.close()
server_socket.close()
