import cv2
import urllib.request
import numpy as np

with urllib.request.urlopen("http://localhost:3000/qr") as url:
    s = url.read()
    # I'm guessing this would output the html source code ?
    # print(s)
    arr = np.asarray(bytearray(s), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'

    cv2.imshow('QR', img)
    if cv2.waitKey() & 0xff == 27: quit()
