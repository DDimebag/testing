from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest


def test_setup():
	global driver
	driver = webdriver.Chrome('C:\\Program Files\\chromedriver.exe')
	driver.maximize_window()
	time.sleep(5)
	driver.get('https://community-z.com/communities')


@pytest.mark.skip(reason="...")
def test_is_searchbox_enabled():
	assert driver.find_element_by_xpath('//input[@type="text"]').is_enabled() == True


@pytest.mark.skip(reason="...")
def test_is_searchbox_value_valid():
	expected = "this is a test string"
	searchbox = driver.find_element_by_xpath('//input[@type="text"]')

	searchbox.send_keys(expected)

	searchbox_value = driver.find_element_by_xpath('//input[@type="text"]').get_attribute('value')

	assert expected == searchbox_value


@pytest.mark.skip(reason="...")
def test_validate_search_results():
	time.sleep(3)
	search_input = '123'
	try:
		driver.find_element_by_class_name('evnt-search-clear').click()
	except Exception as e:
		print("Element Not Found\n", e)

	searchbox = driver.find_element_by_xpath('//input[@type="text"]')
	searchbox.send_keys(search_input)

	time.sleep(2)

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
	    time.sleep(5)

	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")

	    if new_height == last_height:
	        break
	    last_height = new_height


	cards = driver.find_elements_by_class_name('evnt-communities-column')
	is_contains_searchword = [0 for x in cards]

	for i, card in enumerate(cards):
		a_element = card.find_element_by_xpath(".//a")
		url = a_element.get_attribute('href')

		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(url)
		time.sleep(5)

		#check if title contains the search word (partial match)
		if driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/section[2]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/h1').text.lower().find(search_input.lower()):
			is_contains_searchword[i] += 1

		#check if the paragraph contains the search word (exact match)
		if search_input.lower() in driver.find_element_by_css_selector('.evnt-description-wrapper > p').text.lower():
			is_contains_searchword[i] += 1

		#check if any tags contains the search word
		label_tags = driver.find_elements_by_tag_name('label')
		label_texts = []

		for label_tag in label_tags:
			label_texts.append(label_tag.text.lower())

		for label_text in label_texts:
			if search_input.lower() in label_text.lower():
				is_contains_searchword[i] += 1


		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(2)


		#print("label texts:", label_texts)

	print("Appearance per card: ", is_contains_searchword)

	assert 0 not in is_contains_searchword


@pytest.mark.skip(reason="not yet ready")
def test_validate_search_location():
	#time.sleep(2)
	countryList = ["Hungary", "Armenia"]

	try:
		driver.find_element_by_class_name('evnt-search-clear').click()
	except Exception as e:
		print("Element not found\n", e)

	if driver.get_window_size()['width'] <= 1024:
		driver.find_element_by_class_name('evnt-show-filters-button.evnt-button btn').click()

	driver.find_element_by_id('filter_location').click()

	for country in countryList:
		selector = "[data-value=" + '"' + str(country) + '"]'
		driver.find_element_by_css_selector(selector).click()

	time.sleep(3)
	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(5)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
		        break
		last_height = new_height


	cards = driver.find_elements_by_class_name('evnt-communities-column')

	for i, card in enumerate(cards):
		a_element = card.find_element_by_xpath(".//a")
		link = a_element.get_attribute('href')

		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(link)
		time.sleep(3)

		#check location is right
		try:
			location = driver.find_element_by_css_selector('#app > div.evnt-main-container.evnt-event-page > main > section.evnt-panel.evnt-card-panel.evnt-community-card > div > div > div > div.evnt-card-cell.evnt-info-cell > div.evnt-desktop-info > div.evnt-info-details.location > p > span').text
			#print("location: ", location)
		except Exception as e:
			print("Location is not defined.")
			print(e)
			driver.close()
			driver.switch_to.window(driver.window_handles[0])
			continue


		for country in countryList:
			if location.lower().find(country.lower()) != -1:
				print("Country: ", country)
				print("Location: ", location)
				print("OK")
			else:
				print("Country: ", country)
				print("Location: ", location)
				print("X")

		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(5)


def test_teardown():
	driver.quit()
