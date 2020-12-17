import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://signin.intra.42.fr/users/sign_in"

def is_valid_intra_info():

    session = requests.Session()

    request_login_page = session.get(LOGIN_URL)
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

    post_data["user[login]"] = 'yohlee' # INTRA_ID
    post_data["user[password]"] = '123123' # INTRA_PW

    request_login = session.post(LOGIN_URL, data=post_data, allow_redirects=False)

    soup = BeautifulSoup(request_login.text, 'html.parser')
    redirect_url = soup.find('a')['href']

    if redirect_url == LOGIN_URL:
        return False
    else:
        return True
