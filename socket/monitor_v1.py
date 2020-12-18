import os
import socket

def run_server(port=5001):
    host = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            msg = conn.recv(1024)
            os.system('rm qr')
            os.system('wget http://'+addr[0]+':3000/qr')
            os.system('fbi -T 2 qr')
            os.system('sleep(15)')
            os.system('fbi -T 2 white.jpg')
            conn.sendall(msg)
            conn.close()
if __name__ == '__main__':
    os.system('fbi -T 2 default.jpg')
    run_server()
