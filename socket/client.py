import socket

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 4001))
        line = input(':')
        s.sendall(line.encode())
        resp = s.recv(1024)
        print("received: {}".format(resp))

if __name__ == '__main__':
    run()
