# selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class sportlinksyncPage():
 
    _playerszv_locator = (By.ID, "id_playerszv")
    _playersall_locator = (By.ID, "id_playersall")
    _playersold_locator = (By.ID, "id_playersold")
    _submit_locator = (By.ID, "Uploaden")

    def __init__(self,driver):
        self.driver = driver

    def postMembers(self, filezv, fileall, fileold):
        self.driver.find_element(*self._playerszv_locator).send_keys(filezv)
        self.driver.find_element(*self._playersall_locator).send_keys(fileall)
        self.driver.find_element(*self._playersold_locator).send_keys(fileold)
        self.driver.find_element(*self._submit_locator).click()
        return self.driver