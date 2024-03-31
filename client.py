import socket
import sys
import os

def create_file_size_header(file_size):
    return str(file_size).zfill(32)

def is_mp4_file(file_path):
    return file_path.endswith('.mp4')

def send_video(file_path, server_address, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    with open(file_path, 'rb') as f:
        file_size = os.path.getsize(file_path)
        if(file_size == 0):
            print('file is empty')
            sys.exit()
        elif(file_size > 4 * 1024 * 1024 * 1024):
            print('file is too large')
            sys.exit()
            
        sock.sendall(str(file_size).encode('utf-8'))
        while True:
            data = f.read(1400)
            if not data:
                break
            sock.sendall(data)
        data = sock.recv(1024).decode('utf-8')
        if data == '1':
            print('success')
    sock.close()
    print('Video sent to', server_address)

if __name__ == '__main__':
    file_path = 'video.mp4'
    if(is_mp4_file(file_path) == False):
        print('Invalid file type. Please provide a .mp4 file.')
        sys.exit()
    server_address = '0.0.0.0'
    server_port = 9001
    send_video(file_path, server_address, server_port)