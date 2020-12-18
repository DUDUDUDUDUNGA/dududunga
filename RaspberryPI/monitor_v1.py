import os
import socket
import webbrowser
import time

def run_server(port=5001):
    host = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            msg = conn.recv(2048).decode()
            print(msg)
            print(type(msg))
            print(len(msg))

            import base64
            imgdata = base64.b64decode(msg)
            filename = 'qr.jpg'  # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                    f.write(imgdata)

            os.system("kill -15 `ps -aux | grep fbi | awk '{print $2}'`")
            os.system('sudo fbi -T 2 qr.jpg')
            print("SHOW QR")
            time.sleep(5)
            os.system('sudo fbi -T 2 white.jpg')
            conn.sendall(msg.encode())
            conn.close()

if __name__ == '__main__':
    os.system('sudo fbi -T 2 white.jpg')
    run_server()
