# GET PROXIES LIVE by g4rzk
# System: get proxies -> check -> filter and save to json

import os
import json
import random
import argparse
import requests
import datetime
from time import time
from concurrent.futures import ThreadPoolExecutor

red = "\033[1;91m"
green = "\033[1;92m"
white = "\033[1;97m"
timeNow = datetime.datetime.now()

class getProxies:
	
	def __init__(self, protocol, output):
		self.o = output
		self.p = protocol
		self.proxies = []
		self.tampung = []
		self.timeout = 10
		self.__start__()
		self.__save__()
	
	def user_agent(self):
		useragent = [
			"Mozilla/5.0 (Linux; Android 5.0.1; Nexus 7 Build/LRX22C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Safari/537.36 Viber/17.5.0.6", 
			"Mozilla/5.0 (Linux; U; Android 4.2.2; ME302KL Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Chrome/ Safari/534.30 OPR/60.0.2254.59405",
			"Mozilla/5.0 (Linux; Android 5.0; ASUS_Z00AD Build/LRX21V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 GSA/11.31.16.21.x86", 
			"Mozilla/5.0 (Linux; Android 6.0.1; ASUS_Z010D Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
		]
		return random.choice(useragent)
		
	def __start__(self):
		self.proxyScape()
		with ThreadPoolExecutor(max_workers=30) as th:
			print(f"{white}[TOTAL]=> {green}{len(self.proxies)}{white}")
			for i in self.proxies:
				th.submit(self.checkerProxy, i)

	def proxyScape(self):
		try:
			r = requests.get(f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={self.p}&timeout=10000&country=all&ssl=all&anonymity=all", headers={"user-agent": self.user_agent()}).text
			for a in r.splitlines():
				self.proxies.append(a)
		except:
			pass
		
		return self.proxies
	
	def checkerProxy(self, i):
		data = {}
		try:
			start = time()
			response = requests.get("http://ip-api.com/json/?fields=66842623", 
				headers={"user-agent": self.user_agent()}, 
				proxies={"http": f"{self.p}://{i}", "https": f"{self.p}://{i}"}, 
				timeout=self.timeout)
			finish = time() - start
			
			if response.status_code == 200:
				print(f" {white}[{green}LIVE{white}]=> {i}")
				ipProxy = i.split(":")
				data["ip"] = ipProxy[0]
				data["port"] = ipProxy[1]
				data["type"] = self.p
				data["country"] = response.json()["country"]
				data["time_response"] = str(finish)[0:3] + " ms"
				if ipProxy[0] in response.json()["query"]:
					data["anonymity"] = "Transparent"
				else:
					data["anonymity"] = "Anonymous"
				
				with open(f"{self.o.split('.')[0]}.txt", "a") as file:
					file.write(f"{i}\n")
				self.tampung.append(data)
		except:
			print(f" {white}[{red}DEAD{white}]=> {i}")
	
	def __save__(self):
		arrayJson = {
			"lastupdate": f"{timeNow}", 
			"data": self.tampung
		}
		with open(self.o, "w") as file:
			json.dump(arrayJson, file)

if __name__ == "__main__":
	os.system("clear")
	parser = argparse.ArgumentParser(description="Get Proxies Live Free For You")
	parser.add_argument("-p", type=str, metavar="<PROTOCOL>", help="Protocol proxies, exampe: https, socks4 or socks5")
	parser.add_argument("-o", type=str, metavar="<OUTPUT>", help="Output file")
	args = parser.parse_args()
	
	if args.p:
		getProxies(args.p, args.o)
	else:
		parser.print_help()