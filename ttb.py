from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def findCourse(course, tuts):

	available_tuts = []


	PATH = os.getenv("DRIVER_PATH")

	driver = webdriver.Chrome(PATH)

	driver.get('https://ttb.utoronto.ca/')

	dropdown = WebDriverWait(driver, 10).until(
	    EC.presence_of_element_located((By.ID, "division"))
	)

	dropdown.click()

	utsc = WebDriverWait(driver, 1).until(
	    EC.presence_of_element_located((By.ID, "division-option-5-University of Toronto Scarborough"))
	)

	utsc.click()

	courseSearch = WebDriverWait(driver, 1).until(
	    EC.presence_of_element_located((By.XPATH, '//*[@id="courseSearch"]/div/div[2]/div[1]/input'))
	)

	courseSearch.send_keys(course)

	search = WebDriverWait(driver, 1).until(
	    EC.presence_of_element_located((By.XPATH, "/html/body/app-root/main/app-dashboard/app-search/div/div[3]/button[1]"))
	)

	search.click()

	tut_parent = WebDriverWait(driver, 2).until(
	    EC.presence_of_element_located((By.XPATH, '/html/body/app-root/main/app-dashboard/div/app-result/div[2]/app-course/div[3]/div[2]'))
	)

	all_tuts = tut_parent.find_elements(By.XPATH, "*")

	for course in all_tuts[1:]:

		tut_name = course.find_element(By.XPATH, "./div/h5/span").text

		if tut_name in tuts:

			avail = course.find_element(By.XPATH, "./div/div[1]/div[4]/span").text.split(" ")[0]
			if int(avail) > 0:
				available_tuts.append(tut_name)


	driver.close()

	return available_tuts