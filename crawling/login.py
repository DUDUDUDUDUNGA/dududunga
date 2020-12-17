import requests
import getpass

login_url = "https://reservation.42network.org/signin"

id = input("User ID: ")
password = getpass.getpass()
with requests.Session() as s:
	res = s.get(login_url)
	html = res.text

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(html, 'html.parser')
	token = soup.find('input', {'name': 'authenticity_token' })['value']

	login_info = {
		"utf8": "✓",
		"authenticity_token": token,
		"user[login]": id,
		"user[password]": password,
		"commit": "Sign in"
	}
	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
		"Cache-Control": "max-age=0",
		"Content-Length": "207",
		"Connection": "keep-alive",
		"Content-Type": "application/x-www-form-urlencoded",
		"Host": "signin.intra.42.fr",
		"Referer": res.url,
		"Sec-Fetch-Dest": "document",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "same-site",
		"Sec-Fetch-User": "?1",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
	}

	res = s.post(res.url, data=login_info, headers=headers, allow_redirects=False)
	if res.status_code == 302 and res.headers["Location"] == "https://signin.intra.42.fr/users/sign_in":
		print("Invalid user id or password")
		exit()
	
	from urllib.parse import urlparse
	
	headers['Host'] = "{uri.netloc}".format(uri=urlparse(res.headers['Location']))
	del headers["Content-Type"]
	del headers["Content-Length"]

	res = s.get(res.headers['Location'], headers=headers, allow_redirects=False)

	headers['Host'] = "{uri.netloc}".format(uri=urlparse(res.headers['Location']))
	# reservation 쿠키 획득
	res = s.get(res.headers['Location'], headers=headers, allow_redirects=False)

	# event id 얻기
	event_url = "https://reservation.42network.org/api/me/events?begin_at={begin:d}&end_at={end:d}"
	
	import time
	import datetime
	# 날짜 입력
	# 현재 날짜에서 가장 가까운 월요일
	def get_next_monday():
		x = datetime.datetime.now()
		while x.strftime("%a") != "Mon":
			x += datetime.timedelta(days=1)
		return x

	next_monday = get_next_monday()
	print(next_monday.strftime("%Y/%m/%d"))
	begin = int(time.mktime(datetime.datetime.strptime(next_monday.strftime("%Y/%m/%d"), "%Y/%m/%d").timetuple()))
	end_date = next_monday + datetime.timedelta(days=7) 
	end = int(time.mktime(datetime.datetime.strptime(end_date.strftime("%Y/%m/%d"), "%Y/%m/%d").timetuple()))
	event_url = event_url.format(begin=begin, end=end)
	event_list = []

	# 이벤트가 생성되었는지 확인
	while len(event_list) == 0:
		res = s.get(event_url)
		event_list = res.json()
		print(len(event_list))
		time.sleep(1)

	# 월요일 오전 event id
	first_event = int(event_list[0]["Event"]["event_id"])
	# 월화수목토일 오후
	book_events = [first_event + i for i in [1, 4, 7, 10, 15, 18]]
	headers = {
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
		"Connection": "keep-alive",
		"Content-Length": "0",
		"Host": "reservation.42network.org",
		"Origin": "https://reservation.42network.org",
		"Referer": "https://reservation.42network.org/static/",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
	}

	book_url = "https://reservation.42network.org/api/me/events/"
	
	import threading
	
	def reserve(session, event_id):
		res = session.post(book_url + event_id, headers)
		# 예약 실패시 exception 발생
		res.raise_for_status()
		print(event_id + ": Success!")
		now = datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print("Current Time =", current_time)
		
	for event in book_events:
		t = threading.Thread(target=reserve, args=(s, str(event)))
		t.start()

