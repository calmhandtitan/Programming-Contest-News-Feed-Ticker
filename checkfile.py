from datetime import *
from time import strptime
from bcolors import *

class CheckFile(object):

	def __init__(self):
		self.filename = 'news.txt'
		self.filedata = []
		self.getFileData()
		self.checkIfContestEnded()

	'''
		this function reads file content in a variable and
		stores info about each contest in a list
		then it erases the whole file
	'''
	def getFileData(self):
		with open(self.filename, 'r') as f:
			self.filedata = f.readlines()
		with open(self.filename, 'w'):
			pass

	def checkIfContestEnded(self):
		for contest in self.filedata:
			if 'Codechef' in contest:
				startIdx = contest.find('to')
				endIdx = contest.find('Goto')
				data = contest[startIdx+2 : endIdx].strip()

				if self.checkCodechefDateTime(data.split()):#contest has ended
					self.reportEndOfCodechefContest(contest)
				else:				
					self.reWriteContest(contest)
			elif 'CodeForces' in contest:
				startIdx = contest.find('Duration')
				endIdx = contest.find(' on ')
				duration = contest[startIdx+8 : endIdx].strip()

				startIdx = contest.find(' on ')
				endIdx = contest.find('(IST)')
				dateTime = contest[startIdx+4 : endIdx].strip()

				if self.checkCodeforcesDateTime(duration, dateTime.split()):#contest has ended
					self.reportEndOfCodeforcesContest(contest)
				else:				
					self.reWriteContest(contest)

	'''
		this function reports user that a codechef contest has ended.
	'''
	def reportEndOfCodechefContest(self, contest):
		startIdx = contest.find('hosting')
		endIdx = contest.find('from')
		contestName = contest[startIdx+8 : endIdx].strip()
		print bColors.WARNING + 'Codechef contest ' + contestName + ' has ended.' + bColors.ENDC

	'''
		this function returns
			True, if a codechef contest has ended
			False, if a codechef contest is still to occur
	'''
	def checkCodechefDateTime(self, dateTime):
		tmp = dateTime[0].split('-')
		dates = map(int, tmp)

		tmp = dateTime[1].split(':')
		dates = dates + map(int, tmp)

		contestDate = datetime(dates[0], dates[1], dates[2], dates[3], dates[4], dates[5])
		present = datetime.now()
		return present > contestDate
	'''
		this function reports user that a codeforces contest has ended.
	'''
	def reportEndOfCodeforcesContest(self, contest):
		startIdx = contest.find('hosting')
		endIdx = contest.find('of')
		contestName = contest[startIdx+7 : endIdx].strip()
		print bColors.WARNING + 'Codeforces contest ' + contestName + ' has ended.' + bColors.ENDC

	'''
		this function returns
			True, if a codeforces contest has ended
			False, if a codeforces contest is still to occur
	'''
	def checkCodeforcesDateTime(self, duration, dateTime):
		tmp = dateTime[0].split('/')
		tmp[0] = strptime(tmp[0], '%b').tm_mon
		dates = map(int, tmp)

		tmp = dateTime[1].split(':')
		dates = dates + map(int, tmp)

		duration = duration.split(':')
		duration = map(int, duration)

		contestDate = datetime(dates[2], dates[0], dates[1], dates[3], dates[4])
		contestDate = contestDate + timedelta(minutes = duration[1], hours = duration[0])
		present = datetime.now()
		return present > contestDate
	
	def reWriteContest(self, contest):
		with open(self.filename, 'a+') as f:
			f.write(contest)		


if __name__ == "__main__":
	checkFile = CheckFile()
