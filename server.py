import socket 
import os
import sys
import subprocess
import json

#ヘッダーやbodyを読み込むところから


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001

# 選択したビデオを圧縮する
def compress_video(videos):
    for video in videos:
        subprocess.call('ffmpeg -i '+video+' -crf 18 '+video[:-4]+'_comp.mp4', shell=True)

# 選択したビデオの解像度を変更する
def change_video_resolution(videos):
    for video in videos:
        subprocess.call('ffmpeg -i '+video+' -vf scale=1280:720 '+video[:-4]+'_resized.mp4', shell=True)

# 選択したビデオのアスペクト比を変更する
def change_video_aspect_ratio(videos):
    for video in videos:
        subprocess.call('ffmpeg -i '+video+' -c "-aspect 16:9 '+video[:-4]+'_aspect.mp4', shell=True)

# 選択したビデオをMP3に変換する
def translate_to_mp3(videos):
    for video in videos:
        subprocess.call('ffmpeg -i '+video+' -q:a 0 -map a '+video[:-4]+'.mp3', shell=True)

# 選択した画像をGIFに変換する        
def pick_up_video_to_gif(videos, start, finish):
    for video in videos:
        subprocess.call('ffmpeg  -i' +video+' -ss'+ start +'-t'+ finish, shell=True)

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise Exception('short read from socket')
        data += more
    return data

def receive_video(save_path, server_port):
    sock.bind((server_address, server_port))
    sock.listen(1)
    connection, client_address = sock.accept()
    body_data = connection.recv(1024)
    body_data_decode = body_data.decode('utf-8')
    json_data = json.loads(body_data_decode)
    
    connection.sendall('1'.encode('utf-8'))
    
    is_ready_code = connection.recv(1024)
    is_ready_code_decode = is_ready_code.decode('utf-8')
    new_file_path = save_path + '_received.mp4'
    if is_ready_code_decode == '1':
        with open(new_file_path, 'wb') as f:
            while True:
                data = connection.recv(1400)
                if not data:
                    print('data is null')
                    break
                f.write(data)
        connection.sendall('1'.encode('utf-8'))
        print(json_data['operation_code'])
        if json_data['operation_code'] == '1':
            print('2')
            compress_video([new_file_path])
        elif json_data['operation_code'] == '2':
            change_video_resolution([new_file_path])
        elif json_data['operation_code'] == '3':
            change_video_aspect_ratio([new_file_path])
        elif json_data['operation_code'] == '4':
            translate_to_mp3([new_file_path])
        elif json_data['operation_code'] == '5':
            pick_up_video_to_gif([new_file_path], json_data['start'], json_data['finish'])
        connection.close()
    else:
        connection.close()
        sys.exit()


if __name__ == '__main__':
    save_path = './video.mp4'
    receive_video(save_path, server_port)