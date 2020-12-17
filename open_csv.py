import csv

from http.client import HTTPResponse

# SERVER_ADDR = '127.0.0.1'
# SERVER_PORT = 80

def check_user_exist():
    request_header = 'GET / HTTP/1.1\r\nHost:{}\r\n\r\n'.format(SERVER_ADDR)
    http_response = send_request(request_header)
    if http_response.status != 200:
        print('error: {}'.format(__file__))
        print('expected status: {}, actual status: {}'.format('200', str(http_response.status)))

def get_access_token():
	line = 'POST /oauth/token HTTP/1.1\r\n'
	header = 'Host: api.intra.42.fr\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n'
	body = 'client_id=5f264311aa46ec2421d6f503139cd1749b8f61260ce0040324d3be9665ee37d9&client_secret=49fa112ae9371e3515b7468bfc990bfa586de180538876fca82eae4bf290936c&grant_type=client_credentials'
	
	http_response = send_request(line + header + body)
	if http_response.status != 200:
		print('error: {}'.format(__file__))
	else
		print(http_response.values())

	# https://api.intra.42.fr/oauth/token

# UID (NFCID1): 22  70  fe  36
# 'INTRA_ID', 'INTRA_PW', 'UID_1', 'UID_2', 'UID_3', 'UID_4'

def write_csv(uids):

	with open('db.csv', 'a', newline='', encoding='utf-8') as f:
		wr = csv.writer(f)

		# intra_id = get_intra_id();
		# intra_pw = get_intra_pw();
		# wr.writerow([intra_id, intra_pw, uids[0], uids[1], uids[2], uids[3]])
		wr.writerow(['yohlee','123123', uids[0], uids[1], uids[2], uids[3]])


if __name__ == "__main__":

	# uids = get_nfc_ids()
	uids = ['22','7a','f2','36']

	with open('db.csv', 'r', newline='', encoding='utf-8') as f:
		datas = csv.reader(f)
		data = list(datas)[1:]

		stored_uids = []
		for row in data:
			stored_uids.append(row[2:])

		flag = 0;
		for stored_id in stored_uids:
			if stored_id == uids:
				flag = 0
				break ;
			else:
				flag = 1
		if flag == 1:
			# 아이패드 ssh에 아이디/비번 입력하게 함.
			# 42API에서 유저정보 확인
				# 실패 -> 경고음 + 반복을 통해 재입력하게 함
			write_csv(uids)
			# NFC 태깅하게 하자
		# else:
			# 저장된 인트라 아이디/비번을 이용하여 로그인
				# 실패 -> 위 처리 다시 시도
			# 크롤링 후 예약시간조회
				# 실패 -> 경고알림
			# 두둥등장