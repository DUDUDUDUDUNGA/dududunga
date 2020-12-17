import socket
import time

def run():
	while True:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect(('127.0.0.1', 4001))
			line = ['aa', 'bb', 'cc', 'dd']
			line = str(line)
			s.send(line.encode())
			time.sleep(2)
			# resp = s.recv(1024)
			# print("received: {}".format(resp))

if __name__ == '__main__':
	run()
