import os
from datetime import datetime
from time import sleep

ssid_list = [{"ssid":"ZTE-ed93a8", "password":"aldian99"}, {"ssid":"hmfghhhnnvv", "password":"hehehehe"}, {"ssid": "hp-ayah", "password":"88882222"}]

while True:
	for s in ssid_list:
		try:
			now = datetime.now()
			print(now.strftime("%H:%M:%S") + "")
			os.system("nmcli device wifi connect {} password {}".format(s["ssid"], s["password"]))
			
		except Exception as e:
			print(e)
		sleep(300)


