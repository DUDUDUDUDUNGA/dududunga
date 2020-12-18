from module import *
from bs4 import BeautifulSoup
from urllib.parse import urlparse

login_url = "https://reservation.42network.org/signin"

def dududunga():
	with requests.Session() as session:
		res = session.get(login_url)
		soup = BeautifulSoup(res.text, 'html.parser')
		token = soup.find('input', {'name': 'authenticity_token' })['value']
		form_data = makeFormDataByIdAndPassword(token)
		headers = makeHeaders(res.url)
		res = session.post(res.url,
							data=makeFormDataByIdAndPassword(token),
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
			print("Reserve!")
		else:
			print("NOT RESERE!")

dududunga()



