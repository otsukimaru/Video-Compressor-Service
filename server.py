import socket 
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001

def receive_video(save_path, server_port):
    sock.bind((server_address, server_port))
    sock.listen(1)
    connection, client_address = sock.accept()
    print('Connection from', client_address)
    with open(save_path, 'wb') as f:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            f.write(data)
    connection.close()
    print('Video received from', client_address)

if __name__ == '__main__':
    save_path = 'received_video.mp4'
    receive_video(save_path, server_port)