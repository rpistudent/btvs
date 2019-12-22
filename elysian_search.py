from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from functions import *

url = "https://dark-solace.org/elysian/index.php"#'http://google.com'

chrome_options = webdriver.ChromeOptions(); 
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")

driver.get(url)

#Login info
username = driver.find_element_by_id("penname").send_keys("<INSERT PENNAME>")
password = driver.find_element_by_id("password").send_keys("<INSERT PASSWORD>")

#Execute login
d = driver.find_element_by_id("loginblock")
e = d.find_element_by_name("submit")
element = driver.find_element_by_xpath("//form[@id='loginblock']/p[3]/input[1]")
driver.execute_script("arguments[0].click();", element)

#Number of pages to go through
search(driver)
firstPageNum = eval(driver.find_element_by_xpath("//div[@id='pagelinks']/a[1]").text)
lastPageNum = eval(driver.find_element_by_xpath("//div[@id='pagelinks']/a[6]").text)

Results = []
#Cycle the first page
result = cycle(driver)
search(driver)
write_results(result, True)

for r in result:
	Results.append(r)

#Go through all pages
currentPageNum = firstPageNum
while currentPageNum != lastPageNum:
	nextPageNum = currentPageNum + 1
	pagelinks = driver.find_elements_by_xpath("//div[@id='pagelinks']/a")

	for p in pagelinks:
		if eval(p.text) == nextPageNum:
			link = p.get_attribute("href")
			break

	print("Page " + str(currentPageNum))
	result = cycle(driver, str(link))
	write_results(result, False)
	currentPageNum = nextPageNum
	driver.get(link)
