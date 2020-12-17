import requests
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

# play_music('yohlee', True)
speech_description()