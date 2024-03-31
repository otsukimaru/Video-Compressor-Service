import socket

def send_video(file_path, server_address, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.sendall(data)
    sock.close()
    print('Video sent to', server_address)

if __name__ == '__main__':
    file_path = 'video.mp4'
    server_address = '0.0.0.0'
    server_port = 9001
    send_video(file_path, server_address, server_port)