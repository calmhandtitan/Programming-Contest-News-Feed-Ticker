import os
import codechef
import codeforces
import checkfile
from bcolors import *

def getProxy():
	print bColors.HEADER + 'Do you use a proxy server for accessing Internet?(y or n)' + bColors.ENDC
	response = raw_input().strip().lower()
	proxyConfig = ""
	if 'y' in response:
		print bColors.OKBLUE + 'Enter HOST:PORT' + bColors.ENDC
		host, port = raw_input().strip().split(':')
		print bColors.OKBLUE + 'Enter Username:Password' + bColors.ENDC
		uname, pswd = raw_input().strip().split(':')
		proxyConfig = "http://" + uname + ":" + pswd + "@" + host + ":" + port
	return proxyConfig
	

if __name__ == "__main__":
	proxyConfig = getProxy()	
	CC = codechef.CodeChef(proxyConfig)
	CF = codeforces.CodeForces(proxyConfig)
	if os.path.exists("news.txt"):
		checkFile = checkfile.CheckFile()
