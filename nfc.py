# -*- coding: utf-8 -*- 

"""
    This example will wait for any ISO14443A card or tag, and
    depending on the size of the UID will attempt to read from it.

    If the card has a 4-byte UID it is probably a Mifare
    Classic card, and the following steps are taken:

    - Authenticate block 4 (the first block of Sector 1) using
      the default KEYA of 0XFF 0XFF 0XFF 0XFF 0XFF 0XFF
    - If authentication succeeds, we can then read any of the
      4 blocks in that sector (though only block 4 is read here)

    If the card has a 7-byte UID it is probably a Mifare
    Ultralight card, and the 4 byte pages can be read directly.
    Page 4 is read by default since this is the first 'general-
    purpose' page on the tags.

    To enable debug message, define DEBUG in nfc/pn532_log.h
"""
import time
# import binascii

# from pn532pi import Pn532, pn532
# from pn532pi import Pn532I2c

# def setup():
#     nfc.begin()

#     versiondata = nfc.getFirmwareVersion()
#     if (not versiondata):
#         print("Didn't find PN53x board")
#         raise RuntimeError("Didn't find PN53x board")  # halt

#     #  Got ok data, print it out!
#     print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
#                                                                 (versiondata >> 8) & 0xFF))

#     #  configure board to read RFID tags
#     nfc.SAMConfig()

#     print("Waiting for an ISO14443A Card ...")


# def get_nfc_ids():
#     #  Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
#     #  'uid' will be populated with the UID, and uidLength will indicate
#     #  if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
#     success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

#     if (success):
#         #  Display some basic information about the card

#         if (len(uid) == 4):
#             keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

#             #  Start with block 4 (the first block of sector 1) since sector 0
#             #  contains the manufacturer data and it's probably better just
#             #  to leave it alone unless you know what you're doing
#             success = nfc.mifareclassic_AuthenticateBlock(uid, 4, 0, keya)

#             if (success):
#                 #  If you want to write something to block 4 to test with, uncomment
#                 #  the following line and this text should be read back in a minute
#                 # data = bytearray([ 'a', 'd', 'a', 'f', 'r', 'u', 'i', 't', '.', 'c', 'o', 'm', 0, 0, 0, 0])
#                 # success = nfc.mifareclassic_WriteDataBlock (4, data)

#                 #  Try to read the contents of block 4
#                 success, data = nfc.mifareclassic_ReadDataBlock(4)

#                 if (success):
#                     uids = [uid.hex()[:2], uid.hex()[2:4], uid.hex()[4:6], uid.hex()[6:]]
#                     print("uids: ", uids)
#                     return uids

#                 else:
#                     print("Ooops ... unable to read the requested block.  Try another key?")
#             else:
#                 print("Ooops ... authentication failed: Try another key?")

#         elif (len(uid) == 7):
#             #  We probably have a Mifare Ultralight card ...
#             print("Seems to be a Mifare Ultralight tag (7 byte UID)")

#             #  Try to read the first general-purpose user page (#4)
#             print("Reading page 4")
#             success, data = nfc.mifareultralight_ReadPage(4)
#             if (success):
#                 #  Data seems to have been read ... spit it out
#                 binascii.hexlify(data)
#                 return 0

#             else:
#                 print("Ooops ... unable to read the requested page!?")

#     return 0

### check reservation
import requests
import time
import datetime
import getpass

def makeFormDataByIdAndPassword(token, id, password):
        # id, password = getIdAndPassword()
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
                        play_music(id, is_warning=True)
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

def speech_description(sequence):
		kakao_speech_url = 'https://kakaoi-newtone-openapi.kakao.com/v1/synthesize'
		headers = {
			'Content-Type': 'application/xml',
			'Authorization': 'KakaoAK 7cc347f5ecfb519911e397897c264b2e',
		}

		data = ''

		if sequence == 0:
			data = '\
			<speak>\
			<prosody rate="medium" volume="loud">아이패드에 인트라 아이디와 패스워드를 입력해주세요.</prosody>\
			</speak>\
			'
		elif sequence == 1:
			data = '\
			<speak>\
			<prosody rate="medium" volume="loud">성공적으로 등록되었습니다.</prosody>\
			</speak>\
			'

		res = requests.post(kakao_speech_url, headers=headers, data=data.encode('utf-8'))

		with open('b.mp3', 'wb') as f:
			f.write(res.content)

		pygame.mixer.init(44100, -16, 1, 2048)
		pygame.mixer.music.load('b.mp3')
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

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:
	def __init__(self, key):
		self.bs = 32
		self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

	@staticmethod
	def str_to_bytes(data):
		u_type = type(b''.decode('utf-8'))
		if isinstance(data, u_type):
			return data.encode('utf-8')
		return data

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))
	
	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]
	
	def encrypt(self, raw):
		raw = self._pad(AESCipher.str_to_bytes(raw))
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

	def decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

# 'INTRA_ID', 'INTRA_PW', 'UID_1', 'UID_2', 'UID_3', 'UID_4', 'NAVER_ID', 'NAVER_PW'
def write_csv(data, uids):
    with open('db.csv', 'a', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow([data['intra_id'], data['intra_pw'], uids[0], uids[1], uids[2], uids[3], data['naver_id'], data['naver_pw']])

def getNaverIdAndPassword():
    naver_id = input("naver id: ")
    naver_password = getpass.getpass()
    return naver_id, naver_password

def makeUserQR(user_infos):
    os.system('cp -r covid19-qrcode ' + user_infos['intra_id'])
    os.system('cd ' + user_infos['intra_id'] + '&& sed "s/NAVER_ID/'+ user_infos['naver_id'] +'/g" ./app/controllers/qr.controller_copy.ts > ./app/controllers/qr.controller1.ts')
    os.system('cd ' + user_infos['intra_id'] + '&& sed "s/NAVER_PW/'+ user_infos['naver_pw'] +'/g" ./app/controllers/qr.controller1.ts > ./app/controllers/qr.controller.ts')
    os.system('cd ' + user_infos['intra_id'] + '&& npm i')
    os.system('cd ' + user_infos['intra_id'] + '/app/controllers && rm qr.controller1.ts qr.controller_copy.ts')
    # os.system('cd ' + user_infos['intra_id'] + '/app/controllers && rm qr.controller1.ts qr.controller_copy.ts')


# PN532_I2C = Pn532I2c(1)
# nfc = Pn532(PN532_I2C)


import socket
import pickle
import os

def run_server():
	conn, addr = s.accept()
	msg = conn.recv(1024)
	msg = pickle.loads(msg)
	# msg = list(msg)
	conn.close()
	return msg

def display_qr(server_ip, pid):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("debug 3")
        time.sleep(5)
        # s.connect(('127.0.0.1', 5001))
        s.connect((server_ip, 5001))
        print("debug 4")
        go = "1"
        s.send(go.encode())
        print("debug 5")
        resp = s.recv(1024)
        print("debug 6")
        # os.system('kill -15 ' + str(pid))
        # os.system('kill -15 `lsof -i -P -n | grep 3000 | awk \'{print$2}\'`')
        print("debug 7")
        os.wait()
        print("debug 8")
        print(resp)

if __name__ == "__main__":
    # setup()

    host = ''
    port = 4001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    server_ip = input("Enter your Monitor rasberry ip address: ")
#     display_qr(server_ip)

    # key 값을 input으로 받고, 그 key가 지정한 key와 같은지 확인하는 api server를 두는것도 괜찮을듯!
    aes_cipher = AESCipher('sanamjujeongyohlee')

    while True:
        uids = run_server()
        # uids = get_nfc_ids()
        # while not uids:
        #     uids = get_nfc_ids()
        # uids = ['22','70','fe','36']

        with open('db.csv', 'r', newline='', encoding='utf-8') as f:
            datas = csv.reader(f)
            data = list(datas)[1:]
            #TODO: 수정필요
            if (len(data) == 0):
                user_infos = dict()
                user_infos['intra_id'] = intra_id
                user_infos['intra_pw'] = intra_pw
                user_infos['naver_id'] = naver_id
                user_infos['naver_pw'] = naver_pw
                write_csv(user_infos, uids)
                # write_csv(uids)
                f = open('db.csv', 'r', newline='', encoding='utf-8')
                datas = csv.reader(f)
                data = list(datas)[1:]
            stored_uids = []
            for row in data:
                stored_uids.append(row[2:6])
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
                speech_description(0)
                for i in range(5):
                    print('{}번 째 시도'.format(i + 1))
                    intra_id = input('User ID: ')
                    intra_pw = getpass.getpass()
                    is_valid = is_valid_intra_info(intra_id, intra_pw)

                    enc_intra_id = aes_cipher.encrypt(intra_id)
                    enc_intra_pw = aes_cipher.encrypt(intra_pw)
                    if is_valid == True:
                        print('new id')
                        naver_id, naver_pw = getNaverIdAndPassword()

                        enc_naver_id = aes_cipher.encrypt(naver_id)
                        enc_naver_pw = aes_cipher.encrypt(naver_pw)

                        user_infos = dict()
                        user_infos['intra_id'] = enc_intra_id
                        user_infos['intra_pw'] = enc_intra_pw
                        user_infos['naver_id'] = enc_naver_id
                        user_infos['naver_pw'] = enc_naver_pw
                        write_csv(user_infos, uids)
                        print('store success! tag one more your id card')

                        user_infos['intra_id'] = aes_cipher.decrypt(enc_intra_id)
                        user_infos['intra_pw'] = aes_cipher.decrypt(enc_intra_pw)
                        user_infos['naver_id'] = aes_cipher.decrypt(enc_naver_id)
                        user_infos['naver_pw'] = aes_cipher.decrypt(enc_naver_pw)

                        makeUserQR(user_infos)
                        speech_description(1)
                        break
                    else:
                        play_music(intra_id, is_warning=True)
                        continue
            else:
                print("exist")
                dududunga(aes_cipher.decrypt(data[i][0]), aes_cipher.decrypt(data[i][1]))
                # TODO 5. QR 설정
                # 1. 라즈2 신호를 싸줌
                # os.system('cd ' + aes_cipher.decrypt(data[i][0]) + '&& npm run build')
                
                pid = os.fork()
                if pid == 0:
                    print("debug 1")
                    os.system('cd ' + aes_cipher.decrypt(data[i][0]) + '&& npm run build&')
                    time.sleep(10)
                    print("debug 2")
                    print("npm pid is below")
                    os.system('lsof -i -P -n | grep 3000 | awk \'{print$2}\'')
                    os.system('kill -15 `lsof -i -P -n | grep 3000 | awk \'{print$2}\'`')
                    exit

                else:
                    print("child pid: {}".format(pid))
                    display_qr(server_ip, pid)

                # 저장된 인트라 아이디/비번을 이용하여 로그인
                    # 실패 -> 위 처리 다시 시도
                # 크롤링 후 예약시간조회
                    # 실패 -> 경고알림
                # 두둥등장
        time.sleep(1)