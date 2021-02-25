from selenium import webdriver
import pytest
import time


def test_setup():
	global driver
	driver = webdriver.Chrome('C:\\Program Files\\chromedriver.exe')
	driver.maximize_window()
	time.sleep(5)
	driver.get('https://community-z.com/communities')


def test_cookie_notification_alert_is_present():
	cookie_notification_bar = driver.find_elements_by_css_selector('#app > div.alert.evnt-alert.justify-content.bottom-position.cookie-alert')

	assert len(cookie_notification_bar) == 1


def test_cookie_text_is_correct():
	expected = "This website uses cookies for analytics, personalization and advertising. Click here to learn more. By continuing to browse, you agree to our use of cookies."
	
	actual = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/p').text

	assert actual == expected


def test_accept_button_is_displayed():
	accept_button = driver.find_element_by_xpath('//button[text()="Accept"]')

	assert accept_button.is_displayed() == True


def test_notification_dissapear_if_clicked():
	accept_button = driver.find_element_by_xpath('//button[text()="Accept"]')
	accept_button.click()

	with pytest.raises(Exception):
		assert driver.find_element_by_css_selector('#app > div.alert.evnt-alert.justify-content.bottom-position.cookie-alert')


def test_teardown():
	driver.quit()
