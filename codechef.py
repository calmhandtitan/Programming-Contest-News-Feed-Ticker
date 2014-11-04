import urllib2

class CodeChef(object):
	def __init__(self):
		self.contest_url = 'http://www.codechef.com/contests/'
		self.filename = 'news.txt'
		self.data = ''	
		self.multiList = []
		self.parse_page()
		self.find_future_contests()
		self.write_contests()
	def parse_page(self):
		'''
			parses codechef.com/contest page
			Avoid the next 4 lines if you aren't using a proxy server
		'''
		proxy_url = "http://username:password@host:port"
		proxy_support = urllib2.ProxyHandler({'http' : proxy_url})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		try:
			req = urllib2.Request(self.contest_url)
			response = urllib2.urlopen(req)
			self.data = response.read()
		except urllib2.HTTPError as e:
			print e.reason

	def find_future_contests(self):
		'''
			searches the raw data of codechef.com/contest page
			for upcoming contests and adds them to multiList
		'''
		start_link = self.data.find('Future Contests')
		end_link = self.data.find('Past Contests')
		z = self.data[start_link:end_link]
		start_link = z.find('</tr>')
		z = z[start_link+5:]
		while 1:
			start_link = z.find('<tr >')
			end_link = z.find('</tr>')
			if start_link == -1 and end_link == -1:
				break
			self.multiList.append(self.fetch_details(z[start_link:end_link]))
			z = z[end_link+5:]
		

	def fetch_details(self, s):
		'''
			fetch_details() fetches contest info from the given string s, and
			Returns a list of info about each contest
			list[0] is the name of the contest
			list[1] is the startDate and startTime of the contest
			list[2] is the endDate and endTIme of the contest
			list[3] is the contest Code	
		'''
		List = []
		start = s.find('<td >')
		end = s.find('</td>')
		contest_code = str(s[start+5:end])
		s = s[end:]
		start = s.find('">')
		end = s.find('</a>')
		List.append(str(s[start+2:end]))	#append the contest name
		s = s[end:]
		start = s.find('<td >')
		s = s[start:]
		end = s.find('</td>')
		List.append(str(s[5:end]))		#append the startDate & startTime
		s = s[end+5:]
		start = s.find('<td >')
		end = s.find('</td>')
		List.append(str(s[start+5:end]))	#append the endDate & endTime
		s = s[end:]
		List.append(self.contest_url+contest_code)	#append the contest Code
		return List

					
	def write_contests(self):
		'''
			reads the contest info from multiset and
			writes them to file
		'''
		n = len(self.multiList)
		for i in range(n):
			s = 'Codechef is hosting ' + self.multiList[i][0]+' from ' + self.multiList[i][1]
			s = s +' to ' + self.multiList[i][2]+' Goto: ' + self.multiList[i][3]
			self.write_file(s, self.filename)


	def write_file(self, s, filename):
		'''
			writes string s to file with given
			filename is string is already not present in that file
		'''
		added = False
		with open(filename, "a+") as file:
			if (s+"\n") not in file:
				print >> file, s
				added = True
		if added:
                        print 'A new Codechef contest has been added to the file.'
		file.close()


if __name__ == "__main__":
	CC = CodeChef()
