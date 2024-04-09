import socket
import sys
import os
import json

#ヘッダーを作成する
def create_protocol_header(json_data, medea_type, payload_size):
    print(json_data, medea_type, payload_size)
    return json_data.to_bytes(16, 'big') + medea_type.to_bytes(1, 'big') + payload_size.to_bytes(47, 'big')

# ボディを作成する
def create_body(json_data, media_type, payload):
    json_data_encoded = json.dumps(json_data).encode('utf-8')
    media_type_encoded = media_type.encode('utf-8')
    payload_encoded = json.dumps(payload).encode('utf-8')
    return json_data_encoded + media_type_encoded + payload_encoded

# JSONを作成する
def create_json(media_type, file_path, operation_code, start = None, end = None):
    return {
        "media_type": media_type,
        "file_path": file_path,
        "operation_code": operation_code,
        "start": start,
        "end": end
    }

# ペイロードを作成する
def create_payload(media_type, operation_code, url):
    return {
        "media_type": media_type,
        "operation_code": operation_code,
        "url": url
    }

# ペイロードをファイルとして保存する関数
def save_payload(payload, media_type):
    file_extension = get_file_extension(media_type)
    file_name = "payload" + file_extension
    
    with open(file_name, "wb") as file:
        for key, value in payload.items():
            file.write(f"{key}: {value}\n".encode('utf-8'))

# メディアタイプに対応する拡張子を取得する関数
def get_file_extension(media_type):
    if media_type == "mp4":
        return ".mp4"
    elif media_type == "mp3":
        return ".mp3"
    elif media_type == "json":
        return ".json"
    # 他のメディアタイプに対する拡張子の処理を追加することもできます
    else:
        return ".dat"

# ファイルサイズヘッダーを作成する関数
def create_file_size_header(file_size):
    return str(file_size).zfill(32)

# ファイルがmp4形式かどうかを判定する関数
def is_mp4_file(file_path):
    return file_path.endswith('.mp4')

def send_video(file_path, server_address, server_port):
    media_type = 'mp4'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    operation_code = input('Enter the operation code: ')
    if operation_code == 5:
        start = input('Enter the start time: ')
        end = input('Enter the end time: ')
        json_data = create_json('mp4', file_path, operation_code, start, end)
    else:
        json_data = create_json('mp4', file_path, operation_code)
    payload = create_payload('mp4', file_path, operation_code)
    save_payload(payload, 'mp4')
    
    # header = create_protocol_header(len(json.dumps(json_data)), len(media_type), len(payload))
    # body = create_body(json_data, 'mp4', payload)
    send_json_data = json.dumps(json_data)
    sock.sendall(send_json_data.encode('utf-8'))
    server_response_code = sock.recv(1024)
    
    if server_response_code.decode('utf-8') == '1':
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
        print('Video sent to', server_address)
        sock.close()
    else:
        print('Video not sent to', server_address)
        sock.close()

if __name__ == '__main__':
    file_path = input('Enter the file path: ')
    if(is_mp4_file(file_path) == False):
        print('Invalid file type. Please provide a .mp4 file.')
        sys.exit()
    server_address = '0.0.0.0'
    server_port = 9001
    send_video(file_path, server_address, server_port)