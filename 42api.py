import requests

def get_user_info(access_token):

	headers = {'Authorization': 'Bearer ' + access_token}
	response = requests.get('https://api.intra.42.fr/v2/users/yohlee', headers=headers)
	if (response.status_code != 200):
		print('Error')
	else:
		print(response.text)

def get_access_token():

	tokens = {
		'client_id':'YOUR_CLIENT_ID',
		'client_secret':'YOUR_SECRET_TOKEN',
		'grant_type':'client_credentials'
	}
	
	url = 'https://api.intra.42.fr/oauth/token'
	response = requests.post(url, params=tokens)

	if response.status_code != 200:
		print('Error')
	else:
		print(response.json()['access_token'])

	access_token = response.json()['access_token']
	get_user_info(access_token)

get_access_token()