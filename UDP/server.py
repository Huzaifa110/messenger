import socket
import threading
import queue

messages = queue.Queue()
clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = '127.0.0.1'
port = 9999
server.bind((host, port))

def receive():
    while True:
        try:
            message, address = server.recvfrom(1024)
            messages.put((message, address))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, address = messages.get()
            message_str = message.decode()
            print(message_str)
            if address not in clients:
                clients[address] = message_str.split(":", 1)[1].strip()
            for client in clients:
                try:
                    if message_str.startswith("CLIENT:"):
                        name = message_str.split(":", 1)[1].strip()
                        if client != address:
                            server.sendto(f'{name} joined the chat..'.encode(), client)
                    elif message_str.lower() == f'{clients[address]} has left the chat':
                        del clients[address]  
                        server.sendto(message, client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)

print("Server is listening...")

thread1 = threading.Thread(target=receive)
thread1.start()

thread2 = threading.Thread(target=broadcast)
thread2.start()
