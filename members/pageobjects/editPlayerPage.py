# selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class editPlayerPage():
    _FirstName_locator = (By.ID, "id_first_name")
    _Suffix_locator = (By.ID, "id_suffix")
    
    def __init__(self,driver, url):
        self.driver = driver
        self._url = url

    def editProfile(self):
        self.driver.get(self._url)
        self.driver.find_element(*self._BasicSetup_locator).click()