import socket
import threading
import random
import sys  

client =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('127.0.0.1', random.randint(8000, 9000)))

name = input("Name: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

thread = threading.Thread(target=receive)
thread.start()

client.sendto(f'CLIENT:{name}'.encode(), ('127.0.0.1', 9999))

while True:
    message = input("")
    if message.lower() == 'exit':  
        client.sendto(f'{name} has left the chat'.encode(), ('127.0.0.1', 9999))
        client.close()  
        sys.exit()  
    client.sendto(f'{name}: {message}'.encode(), ('127.0.0.1', 9999))
