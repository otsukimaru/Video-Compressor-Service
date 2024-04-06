import socket
import sys
import os

#ヘッダーを作成する
def create_protocol_header(json, medea_type, payload_size):
    return json.to_bytes(16, 'big') + medea_type.to_bytes(1, 'big') + payload_size.to_bytes(47, 'big')

# ボディを作成する
def create_body(json, media_type, payload):
    return json + media_type.encode('utf-8') + payload

# JSONを作成する
def create_json(media_type, file_path, operation_code):
    return {
        'media_type': media_type,
        'file_path': file_path,
        'op_code': operation_code,
    }

# ペイロードを作成する
def create_payload(media_type, operation_code, url):
    return {
        'media_type': media_type,
        'operation_code': operation_code,
        'url': url,
    }

# ペイロードをファイルとして保存する関数
def save_payload(payload, media_type):
    file_extension = get_file_extension(media_type)
    file_name = "payload" + file_extension
    
    with open(file_name, "wb") as file:
        file.write(payload)

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    operation_code = input('Enter the operation code: ')
    json_data = create_json('mp4', file_path, operation_code)
    payload = create_payload('mp4', file_path, operation_code)
    save_payload(payload, 'mp4')
    
    header = create_protocol_header(len(json_data), len('mp4'), len(payload))
    body = create_body(json_data, 'mp4', payload)
    sock.sendall(header + body)
    
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
    file_path = input('Enter the file path: ')
    if(is_mp4_file(file_path) == False):
        print('Invalid file type. Please provide a .mp4 file.')
        sys.exit()
    server_address = '0.0.0.0'
    server_port = 9001
    send_video(file_path, server_address, server_port)