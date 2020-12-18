import requests
import time
import datetime
import getpass

def makeFormDataByIdAndPassword(token):
	id, password = getIdAndPassword()
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
