from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
import yagmail
import sys

keywords = ['purr', 'nuzzl', 'snarl', 'growl', 'rumbl', 'knight', 'cry', 'preen', 'warrior', 'gift', 'fighter', 'hunt', 'predator', 'prowl', 'feral', 'mewl']
#Slayer side, Slayer demon, Shadow demon
count = 0

###########################################################
class Work:
	def __init__(self, title, rating, keywords):
		self.title = title
		self.rating = rating
		self.keywords = dict()
		for word in keywords:
			self.keywords[word] = 0
		self.total = 0

	def get_wordcount(self, wordcount):
		self.wordcount = wordcount

###########################################################

def search(driver, pagelink=None):
	if pagelink is not None:
		driver.get(pagelink)
	else:
		driver.get("https://dark-solace.org/elysian/search.php")
		element = driver.find_element_by_xpath("//div[@id='mainpage']/div[2]/form[1]/div[1]/input[@type='submit']")
		driver.execute_script("arguments[0].click();", element)

def cycle(driver, pagelink=None):
	### Go to all results on page ###
	evenList = driver.find_elements_by_xpath("//div[@class='listboxa even']")
	oddList = driver.find_elements_by_xpath("//div[@class='listboxa odd']")

	evenLen = len(evenList)
	oddLen = len(oddList)

	Works = []
	for i in range(evenLen + oddLen):
		if pagelink is not None:
			search(driver, pagelink)
		else:
			search(driver)

		#Get info
		box = "//div[@id='mainpage']/div[" + str(i+3) + "]"
		info = box + "/div[1]/a[1]"
		title_ = box + "/div[1]/a[1]"
		rating_ = box + "/div[1]/span"

		link = driver.find_element_by_xpath(info)
		title = driver.find_element_by_xpath(title_).text
		rating = driver.find_element_by_xpath(rating_).text
		#print(title + " " + rating)

		#Go to link
		driver.execute_script("arguments[0].click();", link)

		#accept alert
		try:
			alert = driver.switch_to.alert
			alert.accept()
		except NoAlertPresentException:
			pass

		W = get_matches(driver, title, rating, driver.current_url)
		if W.total > 1:
			sys.stdout.write(title + " ")
			sys.stdout.write(rating + ", ")
			for key in W.keywords:
				sys.stdout.write(str(key) + ": " + str(W.keywords[key]) + ", ")
			sys.stdout.write("total: " + str(W.total) + ", ")
			sys.stdout.write(str(W.wordcount))
			Works.append(W)
			print
	return Works
	#################################

def get_matches(driver, title, rating, link):
	W = Work(title, rating, keywords)

	pagelink = link + "&view=all"
	#print(pagelink)
	driver.get(pagelink)

	path = "//div[@id='mainpage']/div[@id='story']/div[@"
	style = path + "style='font-size: 100%; line-height: 150%;']"

	worktext = driver.find_elements_by_xpath(style)
	wordcount = 0
	for work in worktext:
		#print(work.text)
		text = work.text.split()
		wordcount += len(text)
		for t in text:
			b = False
			for word in keywords:
				if  word.lower() in t.lower():
					#print(word, t)
					W.keywords[word] += 1
					W.total += 1
					b = True
					break
			if b == True:
				break
	W.get_wordcount(wordcount)
	return W

def write_results(Results, first):
	if first == True:
		op = "w"
	else:
		op = "a"

	foobar = open("Results1.txt", op)
	for r in Results:
		if r.total > 1:
			text = r.title + " " + r.rating + ", "
			for key in r.keywords:
				text += str(key) + ": " + str(r.keywords[key]) + ", "
			text += "total: " + str(r.total) + ", "
			text += str(r.wordcount) + "\n"
			foobar.write(text.encode('utf-8'))
	foobar.close()

def send_results():
	yag = yagmail.SMTP('3Megan3hieCATS@gmail.com', 'Redred33')
	contents = ['Results1.txt']
	yag.send("3redpurple3@gmail.com", "Results", contents)

def print_results(Works):
	for W in Works:
		if W.total > 0:
			sys.stdout.write(title + " ")
			sys.stdout.write(rating + ", ")
			for key in W.keywords:
				sys.stdout.write(str(key) + ": " + str(W.keywords[key]) + ", ")
			sys.stdout.write(str(r.total) + ", " + str(W.wordcount))
			Works.append(W)
			print
