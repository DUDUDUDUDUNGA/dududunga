### check reservation
import requests
import time
import datetime
import getpass

def makeFormDataByIdAndPassword(token, id, password):
	login_info = {
		"utf8": "✓",
		"authenticity_token": token,
		"user[login]": id,
		"user[password]": password,
		"commit": "Sign in"
	}
	return login_info

def makeHeaders(url):
	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
		"Cache-Control": "max-age=0",
		"Content-Length": "207",
		"Connection": "keep-alive",
		"Content-Type": "application/x-www-form-urlencoded",
		"Host": "signin.intra.42.fr",
		"Referer": url,
		"Sec-Fetch-Dest": "document",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "same-site",
		"Sec-Fetch-User": "?1",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
	}
	return headers

def getIdAndPassword():
	id = input("User ID: ")
	password = getpass.getpass()
	return id, password

# TODO: 예약시간 외에 입려이 들어왔을 경우 처리하기

def getNow():
	return datetime.datetime.now()

def getNowHour():
	return int(getNow().strftime('%H'))

def getNowAndHour():
	return getNow(), getNowHour()

def getStartIndexOfEvent():
	hour = getNowHour()
	if 8 <= hour < 13:
		return 0
	elif 13 <= hour < 18:
		return 3
	else:
		return 6

def getLastIndexOfEvent():
	return (getStartIndexOfEvent() + 3)

def deleteUselessHeaders(headers):
	headers['Host'] = "{uri.netloc}".format(uri=urlparse(res.headers['Location']))
	del headers["Content-Length"]
	del headers["Content-Type"]
	return (headers)


def makeEventUrl():
	event_url = "https://reservation.42network.org/api/me/events?begin_at={begin:d}&end_at={end:d}"
	now = datetime.datetime.now()
	hour = int(now.strftime('%H'))
	begin = int(time.mktime(datetime.datetime.strptime(now.strftime("%Y/%m/%d"), "%Y/%m/%d").timetuple()))
	tomorrow = now + datetime.timedelta(days=1)
	end = int(time.mktime(datetime.datetime.strptime(tomorrow.strftime("%Y/%m/%d"), "%Y/%m/%d").timetuple()))
	event_url = event_url.format(begin=begin, end=end)
	return (event_url)

def checkUserReserveOrNot(session):
	res = session.get(makeEventUrl())
	js = res.json()
	print(js)
	for i in range(getStartIndexOfEvent(), getLastIndexOfEvent()):
		ev = js[i]
		b = ev['is_subscribed']
		if b == True:
			return (True)
	return (False)

from bs4 import BeautifulSoup
from urllib.parse import urlparse

login_url = "https://reservation.42network.org/signin"

def dududunga(id, password):
	with requests.Session() as session:
		res = session.get(login_url)
		soup = BeautifulSoup(res.text, 'html.parser')
		token = soup.find('input', {'name': 'authenticity_token' })['value']
		form_data = makeFormDataByIdAndPassword(token, id, password)
		headers = makeHeaders(res.url)
		res = session.post(res.url,
							data=makeFormDataByIdAndPassword(token, id, password),
							headers=headers,
							allow_redirects=False)
		if res.status_code == 302 and res.headers["Location"] == "https://signin.intra.42.fr/users/sign_in":
			print("Invalid user id or password")
			exit()

		# TODO: 아래 함수화 하기
		#  headers = deleteUselessHeaders(headers)
		headers['Host'] = "{uri.netloc}".format(uri=urlparse(res.headers['Location']))
		del headers["Content-Length"]
		del headers["Content-Type"]
		#  아래의 res는 새롭게 만들어진다.
		res = session.get(res.headers['Location'], headers=headers, allow_redirects=False)
		headers['Host'] = "{uri.netloc}".format(uri=urlparse(res.headers['Location']))
		#  reservation 쿠키 획득
		res = session.get(res.headers['Location'], headers=headers, allow_redirects=False)


		# checkUserReserveOrNot

		b = checkUserReserveOrNot(session)
		if b == True:
			print("Reserve")
			play_music(id)
		else:
			print("NOT RESERE!")

import pygame

def play_music(intra_id, is_warning=False):

	if is_warning == True:
		pygame.mixer.init(16000, -16, 1, 2048)
		pygame.mixer.music.load('warning.wav')
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy():
			pygame.time.Clock().tick(10)
		pygame.mixer.quit()
	else:
		kakao_speech_url = 'https://kakaoi-newtone-openapi.kakao.com/v1/synthesize'
		headers = {
			'Content-Type': 'application/xml',
			'Authorization': 'KakaoAK 7cc347f5ecfb519911e397897c264b2e',
		}

		data = '\
		<speak>\
		<prosody rate="0.7" volume="loud">'\
		+ intra_id\
		+ '</prosody>\
		<prosody rate="medium" volume="loud">두둥등장! 안녕하세요.</prosody>\
		</speak>\
		'

		# <speak> Iwoo. <voice name="MAN_DIALOG_BRIGHT">두둥등장!</voice> </speak> \
		res = requests.post(kakao_speech_url, headers=headers, data=data.encode('utf-8'))

		with open('a.mp3', 'wb') as f:
			f.write(res.content)

		pygame.mixer.init(16000, -16, 1, 2048)
		pygame.mixer.music.load('a.mp3')
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy():
			pygame.time.Clock().tick(10)
		pygame.mixer.quit()


import csv
import getpass
import requests

INTRA_LOGIN_URL = "https://signin.intra.42.fr/users/sign_in"

def is_valid_intra_info(intra_id, intra_pw):

	session = requests.Session()

	request_login_page = session.get(INTRA_LOGIN_URL)
	if request_login_page.status_code == 200:
		page_signin = request_login_page.content.decode("utf-8")
	else:
		return False

	soup = BeautifulSoup(page_signin, features="html.parser")

	post_data = {}
	for form_input in soup.find_all("input"):
		key = form_input.get("name")
		value = form_input.get("value")
		post_data[key] = value

	post_data["user[login]"] = intra_id
	post_data["user[password]"] = intra_pw

	request_login = session.post(INTRA_LOGIN_URL, data=post_data, allow_redirects=False)

	soup = BeautifulSoup(request_login.text, 'html.parser')
	redirect_url = soup.find('a')['href']

	if redirect_url == INTRA_LOGIN_URL:
		return False
	else:
		return True

# 'INTRA_ID', 'INTRA_PW', 'UID_1', 'UID_2', 'UID_3', 'UID_4'
def write_csv(intra_id, intra_pw, uids):
	with open('db.csv', 'a', newline='', encoding='utf-8') as f:
		wr = csv.writer(f)
		wr.writerow([intra_id, intra_pw, uids[0], uids[1], uids[2], uids[3]])

import socket

def run_server():
	conn, addr = s.accept()
	msg = conn.recv(1024)
	# msg = list(msg)
	conn.close()
	return msg

if __name__ == "__main__":
	host = ''
	port = 4001
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(1)
	while True:
		uids = run_server()
		print("uids :", uids)
		print("type :", type(uids))
		# uids = ['22','7a','f2','37']
		with open('db.csv', 'r', newline='', encoding='utf-8') as f:
			datas = csv.reader(f)
			data = list(datas)[1:]
			if (len(data) == 0):
				write_csv(uids)
				f = open('db.csv', 'r', newline='', encoding='utf-8')
				datas = csv.reader(f)
				data = list(datas)[1:]
			stored_uids = []
			for row in data:
				stored_uids.append(row[2:])
			flag = 0;
			print(stored_uids)
			i = 0
			for stored_id in stored_uids:
				if stored_id == uids:
					flag = 0
					break ;
				else:
					flag = 1
				i += 1
			if flag == 1:
				# 아이패드 ssh에 아이디/비번 입력하게 함.
				for i in range(5):
					print('{}번 째 시도'.format(i + 1))
					intra_id = input('User ID: ')
					intra_pw = getpass.getpass()
					is_valid = is_valid_intra_info(intra_id, intra_pw)
					if is_valid == True:
						print('new id')
						write_csv(intra_id, intra_pw, uids)
						print('store success! tag one more your id card')
						break
					else:
						play_music(intra_id, is_warning=True)
						continue
					# 경고음

				#print("new id")
				#write_csv(uids)
				# NFC 태깅하게 하자
			else:
				print("exist")
				dududunga(data[i][0], data[i][1])
				# 저장된 인트라 아이디/비번을 이용하여 로그인
					# 실패 -> 위 처리 다시 시도
				# 크롤링 후 예약시간조회
					# 실패 -> 경고알림
				# 두둥등장
		time.sleep(1)
