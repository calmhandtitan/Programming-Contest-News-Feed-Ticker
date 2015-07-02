import os
import codechef
import codeforces
import checkfile

if __name__ == "__main__":
	CC = codechef.CodeChef()
	CF = codeforces.CodeForces()
	if os.path.exists("news.txt"):
		checkFile = checkfile.CheckFile()
