import os 

intra_id = 'yohlee'
intra_pw = '123123'
naver_id = 'yohan'
naver_pw = '55'

os.system('cp -r covid19-qrcode ' + intra_id)
os.system('cd ' + intra_id + '&& sed "s/NAVER_ID/'+ naver_id +'/g" ./app/controllers/qr.controller_copy.ts > ./app/controllers/qr.controller1.ts')
os.system('cd ' + intra_id + '&& sed "s/NAVER_PW/'+ naver_pw +'/g" ./app/controllers/qr.controller1.ts > ./app/controllers/qr.controller.ts')
os.system('cd ' + intra_id + '&& npm i')

# os.system('cp -r covid19-qrcode ' + intra_id)
# os.system('cd ' + intra_id + '&& sed "s/NAVER_ID/'+ naver_id +'/g" ./app/controllers/qr.controller_copy.ts > ./app/controllers/qr.controller1.ts')
# os.system('sed "s/NAVER_PW/'+ naver_pw +'/g" ./app/controllers/qr.controller1.ts > ./app/controllers/qr.controller.ts')
# os.system('cd .. && npm i')
