import time
import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c

PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)

def setup():
	nfc.begin()

	versiondata = nfc.getFirmwareVersion()
	if (not versiondata):
		print("Didn't find PN53x board")
		raise RuntimeError("Didn't find PN53x board")  # halt
	nfc.SAMConfig()
	print("Waiting for an ISO14443A Card ...")

def get_nfc_ids():
	success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

	if (success):
		if (len(uid) == 4):
			keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
			success = nfc.mifareclassic_AuthenticateBlock(uid, 4, 0, keya)

			if (success):
				success, data = nfc.mifareclassic_ReadDataBlock(4)

				if (success):
					uids = [uid.hex()[:2], uid.hex()[2:4], uid.hex()[4:6], uid.hex()[6:]]
					print("uids: ", uids)
					return uids

				else:
					print("Ooops ... unable to read the requested block.  Try another key?")
			else:
				print("Ooops ... authentication failed: Try another key?")

		elif (len(uid) == 7):
			print("Seems to be a Mifare Ultralight tag (7 byte UID)")
			print("Reading page 4")
			success, data = nfc.mifareultralight_ReadPage(4)
			if (success):
				binascii.hexlify(data)
				return 0

			else:
				print("Ooops ... unable to read the requested page!?")

	return 0

import socket
import pickle

def run(uid, server_ip, port = 4001):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# s.connect((server_ip, port))
		s.connect(('172.30.1.46', 4001))
		data=pickle.dumps(uid)
		s.send(data)

if __name__ == '__main__':
	server_ip = input("Enter your Mac ip address: ")
	setup()
	while True:
		uid = get_nfc_ids()
		while not uid:
			uid = get_nfc_ids()
		run(uid, server_ip)
		time.sleep(3)
