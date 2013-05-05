# selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class loginPage():
 
    _username_locator = (By.ID, "username")
    _password_locator = (By.NAME, "password")
    _submit_locator = (By.ID, "submit")

    def __init__(self,driver):
        self.driver = driver

    def userLogin(self, username, password, address):
        self.driver.get(address)
        self.driver.find_element(*self._username_locator).clear()
        self.driver.find_element(*self._username_locator).send_keys(username)
        self.driver.find_element(*self._password_locator).clear()
        self.driver.find_element(*self._password_locator).send_keys(password)
        self.driver.find_element(*self._submit_locator).click()
        # return 