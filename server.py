import socket 
import os
import sys
import subprocess


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

def receive_video(save_path, server_port):
    sock.bind((server_address, server_port))
    sock.listen(1)
    connection, client_address = sock.accept()
    file_size = int(connection.recv(32).decode('utf-8'))
    with open(save_path, 'wb') as f:
        while True:
            data = connection.recv(1400)
            if not data:
                break
            f.write(data)
        connection.sendall('1'.encode('utf-8'))
    connection.close()
    print('Video received from', client_address)

if __name__ == '__main__':
    save_path = 'received_video.mp4'
    receive_video(save_path, server_port)