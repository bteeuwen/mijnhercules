# selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from sportlinkpage import sportlinksyncPage
from matchpage import matchImportPage

class NavigationMenu():
    _Administratie_locator = (By.LINK_TEXT, "Administratie")
    _Wedstrijden_locator = (By.LINK_TEXT, "Wedstrijden")
    _SpelersSLsync_locator = (By.LINK_TEXT, "Spelers SL sync")
    _UserMenu_locator = (By.ID, "user_menu")
    _AdminMenu_locator = (By.ID, 'administratie_menu')
    
    def __init__(self,driver):
        self.driver = driver
    
    def toSportlink(self):
        self.driver.find_element(*self._Administratie_locator).click()
        self.driver.find_element(*self._SpelersSLsync_locator).click()
        return sportlinksyncPage(self.driver)

    def toMatches(self):
        self.driver.find_element(*self._Administratie_locator).click()
        self.driver.find_element(*self._Wedstrijden_locator).click()
        return matchImportPage(self.driver)

    def toAdmin(self):
        self.driver.find_element(*self._UserMenu_locator).click()
        self.driver.find_element(*self._AdminMenu_locator).click()