import urllib2

class CodeForces(object):
	def __init__(self):
		self.contest_url = 'http://www.codeforces.com/contests/'
		self.filename = 'news.txt'
		self.data = ''	
		self.multiList = []
		self.parse_page()
		self.find_future_contests()
		self.write_contests()

	def parse_page(self):
		'''
			parses codeforces.com/contest page
			Avoid the next 4 lines, if you aren't using a proxy server
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
			searches the raw data of codeforces.com/contest page
			for upcoming contests and adds them to multiList
		'''
		start_link = self.data.find('Current or upcoming contests')
		end_link = self.data.find('Contest history')
		z = self.data[start_link:end_link]
		while 1:
			start_link = z.find('data-contestId=')
			z = z[start_link:]
			end_link = z.find('</tr>')
			if start_link == -1 and end_link == -1:
				break
			self.multiList.append(self.fetch_details(z[:end_link]))
			z = z[end_link+5:]

	def fetch_details(self, s):
		ret = []
		start = s.find('<td>')
		end = s.find('</td>')
		ret.append(str(s[start+5:end]).strip())	#append contest name
		s = s[end+5:]
		start = s.find('">')
		end = s.find('</a>')
		ret.append(str(s[start+3:end]).strip())	#append startDate and startTime
		s = s[end:]
		start = s.find('<td>')
		s = s[start:]
		end = s.find('</td>')
		ret.append(str(s[5:end]).strip())	#append Duration
		return ret

	def write_contests(self):
		'''
			reads the contest info from multiset and
			writes them to file
		'''
		n = len(self.multiList)
		for i in range(n):
			s = 'CodeForces is hosting ' + self.multiList[i][0]+ ' of Duration ' + self.multiList[i][2] 
			self.multiList[i][1] = self.correct_timezone(self.multiList[i][1])
			s = s + ' on ' + self.multiList[i][1] + ' (IST)'
			self.write_file(s, self.filename)

	def correct_timezone(self, s):
		'''
			corrects the timezone from UTC --> IST
		'''
		s = s.split()
		HH = int(s[1][:2])
		MM = int(s[1][3:])
		MM += 30
		if MM == 60:
			MM = str('00')
			HH += 3
		else:
			MM = str(MM)
			HH += 2
		HH = str(HH)
		correctedTime = s[0] + ' ' + HH + ':' + MM
		return correctedTime

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
                        print 'A new Codeforces contest has been added to the file.'
		file.close()


if __name__ == "__main__":
	CF = CodeForces()