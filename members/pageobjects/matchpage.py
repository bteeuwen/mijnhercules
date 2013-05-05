# selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class matchImportPage():
 
    _matchfileupload_locator = (By.ID, "id_matches")
    _submit_locator = (By.ID, "Uploaden")

    def __init__(self,driver):
        self.driver = driver

    def postMatches(self, filename):
        self.driver.find_element(*self._matchfileupload_locator).send_keys(filename)
        self.driver.find_element(*self._submit_locator).click()
        return self.driver