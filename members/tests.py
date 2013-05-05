from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
from members.models import *
from members.views import *
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from members.pageobjects.loginpage import loginPage
from members.pageobjects.navigationPage import *
from members.pageobjects.sportlinkpage import *
# from members.pageobjects.adminpage import *

class BaseTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.driver.quit()

class BaseTestCaseClean(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(BaseTestCaseClean, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCaseClean, cls).tearDownClass()
        cls.driver.quit()

username = 'admin'
password = 'root'
url = "localhost:8000"

class testLogin(BaseTestCase):
# staff player sees admin options
# regular player does not see admin options

    _email = 'bteeuwen@gmail.com'
    _name = 'johnnie'
    _surname = 'testing'
    _password = 'testtest'
    _noplayertext = "No players are available."

    # user account without link to a player model instance is able to login 
    # does not see staff privilidge menu items
    def test01LoginUnknownPlayerNoAdmin(self):
        user = User.objects.create_user(self._name, self._email, self._password)
        login = loginPage(self.driver)
        loginresult = login.userLogin(self._name, self._password, self.live_server_url)
        self.assertIn(self._noplayertext, self.driver.page_source) 
        self.assertTrue(len(self.driver.find_elements_by_id('administratie_menu')) == 0)

    # user account without link to a player model instance is able to login 
    # does see staff privilidge menu items
    def test02LoginUnknownPlayerAdmin(self):
        user = User.objects.create_user(self._name, self._email, self._password)
        user.is_staff = True
        user.save()
        login = loginPage(self.driver)
        loginresult = login.userLogin(self._name, self._password, self.live_server_url)
        self.assertIn(self._noplayertext, self.driver.page_source) 
        self.assertTrue(self.driver.find_element_by_id('administratie_menu'))
        self.assertTrue(self.driver.find_element_by_id('adminlink_menu'))

    # def test03LoginKnownPlayerNoAdmin(self):
    #     login = loginPage(self.driver)
    #     # add player        
    #     usertest = User.objects.create_user(self._name + self._surname, self._email, self._password)
    #     p1 = Player(
    #         first_name=self._name,
    #         last_name=self._surname,
    #         user=usertest)
    #         # knvbnr=pkpass,
    #         # gender=str(v[4]),
    #         # age=datetime.strptime(str(v[5]), "%d-%m-%y"),
    #         # email=str(v[8]),
    #         # cellphone=str(v[6]),
    #         # regularphone=str(v[7]),
    #         # postalcode=str(v[14]),
    #         # street=str(v[11]),
    #         # streetnr=str(v[12]),
    #         # herculesnr=pkherc,
    #         # streetnrplus=str(v[13]),
    #         # city=str(v[10]))
    #     p1.save()
    #     loginresult = login.userLogin(self._name + self._surname, self._password, self.live_server_url)
    #     self.assertIn(self._noplayertext, self.driver.page_source) 
    #     self.assertTrue(len(self.driver.find_elements_by_id('administratie_menu')) == 0)

    # def test04LoginKnownPlayerAdmin(self):
    #     login = loginPage(self.driver)
    #     # loginresult = login.userLogin(username, password, self.live_server_url)

class testSportlinkSynchronisation(BaseTestCase):
    fixtures = ['empty.json']

    _email = 'bteeuwen@gmail.com'
    _name = 'johnnie'
    _surname = 'testing'
    _password = 'testtest'
    _noplayertext = "No players are available."

    _sltest1a = "/Users/bteeuwen/dev/mijnhercules/members/pageobjects/slsync1.csv"
    _sltest1b = "/Users/bteeuwen/dev/mijnhercules/members/pageobjects/slsync1_all.csv"
    _sltest1c = "/Users/bteeuwen/dev/mijnhercules/members/pageobjects/slsync1_oud.csv"
    _sltest2a = "pageobjects/slsync2.csv"
    _sltest2b = "pageobjects/slsync2_all.csv"
    _sltest2c = "pageobjects/slsync2_oud.csv"
    _sltest3a = "pageobjects/slsync3.csv"
    _sltest3b = "pageobjects/slsync3_all.csv"
    _sltest3c = "pageobjects/slsync3_oud.csv"

    def test01InitialUpload(self):
        user = User.objects.create_user(self._name, self._email, self._password)
        user.is_staff = True
        user.save()
        login = loginPage(self.driver)
        # loginresult = login.userLogin(self._name, self._password, url)
        loginresult = login.userLogin(username, password, self.live_server_url)
        navigation = NavigationMenu(self.driver)
        sportlink = navigation.toSportlink()
        navigation = NavigationMenu(sportlink.postMembers(self._sltest1a, self._sltest1b, self._sltest1c))
        self.assertIn("geimporteerd", navigation.page_source)
        # admin = navigation.toAdmin()
        
        sportlink = navigation.toSportlink()
        navigation = NavigationMenu(sportlink.postMembers(self._sltest2a, self._sltest2b, self._sltest2c))
        self.assertIn("geimporteerd", navigation.page_source)

        sportlink = navigation.toSportlink()
        navigation = NavigationMenu(sportlink.postMembers(self._sltest3a, self._sltest3b, self._sltest3c))
        self.assertIn("geimporteerd", navigation.page_source)



    
    # def test_update_temp_player(TestCase):
    # def test_update_herculesnumber(TestCase):
    # def test_delete_from_hercules(TestCase):
    # def test_delete_from_futsal(TestCase):
    # def test_check_logging(TestCase):

class importMatches(BaseTestCase):
    _match1 = "/Users/bteeuwen/dev/mijnhercules/members/pageobjects/wedstr02-18_stefan.csv"
    _email = 'bteeuwen@gmail.com'
    _name = 'johnnie'
    _surname = 'testing'
    _password = 'testtest'
    ## frontend: only import futsal matches of excel file with mixed types of matches
    
    # 'wedstr02-18_stefan.csv', [54423, 08679, 148194, 6517] should be imported.
    # onder andere [10910, 209419, 13952, 102308] should not be imported.
    def test01variousmatches(self):
        user = User.objects.create_user(self._name, self._email, self._password)
        user.is_staff = True
        user.save()
        login = loginPage(self.driver)
        loginresult = login.userLogin(self._name, self._password, self.live_server_url)
        navigation = NavigationMenu(self.driver)
        matches = navigation.toMatches()
        matchesresult = matches.postMatches(self._match1)
        self.assertIn("Er zijn 4 wedstrijden geimporteerd", matchesresult.page_source) 
        self.assertNotIn("Hillegom", matchesresult.page_source) 

    ## import same matches, but with different dates/times:
    # 'wedstr02-18_stefan_newdates.csv' 6517 >> 21:10, 148194 >> 18-2-2013


    ## delete matches that are postponed
    #'wedstr02-18_stefan_1missing.csv', [148194, 6517] should be missing.

    # match for team x visible at dashboard for player of team x

    ## fout met bestand = foutmelding + mail met bestand naar beheerder.
    # geen kolom 'Wedstrijdnummer'

## todo: users & passwords

# fix_real = '130127slsync'

# class BackendTests(TestCase):
#     fixtures = ['testdata']

    # def setUp(self):
    #     self.driver = webdriver.Firefox()
    #     self.driver.implicitly_wait(30)    
    #     self.verificationErrors = []
    #     self.accept_next_alert = True
        
    # def test_get_into_admin(self):
    #     """
    #     Log into Admin
    #     """
    #     self.driver.get('localhost:8000/admin/')
    #     username = self.driver.find_element_by_css_selector("input#id_username")
    #     username.clear()
    #     username.send_keys("bteeuwen")
    #     password = self.driver.find_element_by_css_selector("input#id_password")
    #     password.clear()
    #     password.send_keys("geen")
    #     self.driver.find_element_by_css_selector("input[type='submit']").click()
    #     body = self.driver.find_element_by_tag_name('body')
    #     self.assertIn('Hercules', body.text)

    # def tearDown(self):
    #     self.driver.quit()
    #     self.assertEqual([], self.verificationErrors)

# class PlayerAddRemove(TestCase):
#     def test_new_player(self):
#         player = ['BVE23T','Jan','','Manusje','M','16-06-61','','030-2710232','bteeuwen@gmail.com','8305','UTRECHT','Van Herdenlaan','30','','3571 ZK','24-10-03','24-10-03','Zaal -  Week']
#         addPlayer(player)
#         p = Player.objects.get(knvbnr__knvbnr=player[0])
#         self.assertEqual(p.first_name, player[1])
#         self.assertEqual(p.last_name, player[3])
#         self.assertEqual(p.email, player[8])
#         self.assertEqual(p.herculesnr.soccer, ("Veld" in player[17]))

#     def test_new_temp_player(self):
#         player = ['235312','Janerinus','','Herder','V','16-06-64','','030-2234232','bteeuwen@gmail.com','8125','UTRECHT','Van Kanussen','10','','3522 XX','24-10-01','24-10-05','Veld - zaterdag, Zaal -  Week']
#         addPlayer(player)
#         pas = Pass.objects.get(knvbnr=player[0])
#         self.assertEqual(pas.knvbnr, player[0])
#         p = Player.objects.get(knvbnr__knvbnr=player[0])
#         self.assertEqual(p.first_name, player[1])
#         self.assertEqual(p.last_name, player[3])
#         self.assertEqual(p.email, player[8])
#         if player[9] != '':
#             self.assertEqual(p.herculesnr.soccer, ("Veld" in player[17]))
#             self.assertEqual(p.herculesnr.herculesnr, player[9])

#     # delete player
#     def testDeletePlayer(self):
#         player = ['BVE23T','Jan','','Manusje','M','16-06-61','','030-2710232','bteeuwen@gmail.com','8305','UTRECHT','Van Herdenlaan','30','','3571 ZK','24-10-03','24-10-03','Zaal -  Week']
#         addPlayer(player)
#         removePlayer(player[0])
#         with self.assertRaises(Player.DoesNotExist):
#             Player.objects.get(knvbnr__knvbnr = player[0])
#         with self.assertRaises(MembershipHercules.DoesNotExist):
#             MembershipHercules.objects.get(herculesnr = player[9])

# regular player can not edit players



# # class selfEditInfo(TestCase):
#     # view form with name, email, pas, verloopdatum, abonnement, 
#     #def front end form
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.driver.implicitly_wait(30)    
#         self.verificationErrors = []
#         self.accept_next_alert = True
    
#     def testProfileForm(self):    
#         """
#         Log into Admin
#         """
#         self.driver.get('localhost:8000/')
#         username = self.driver.find_element_by_name("username")
#         username.clear()
#         username.send_keys("bteeuwen")
#         password = self.driver.find_element_by_name("password")
#         password.clear()
#         password.send_keys("geen")
#         password.send_keys(Keys.RETURN)
#         #self.driver.find_element_by_css_selector("input[type='submit']").click()
#         body = self.driver.find_element_by_tag_name('body')
#         self.assertIn('Hercules', body.text)

#     def tearDown(self):
#         self.driver.quit()
#         self.assertEqual([], self.verificationErrors)

# class addNewPlayer(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.driver.implicitly_wait(30)    
#         self.verificationErrors = []
#         self.accept_next_alert = True
        
#     def test_get_into_admin(self):
#         """
#         Log into Admin
#         """
#         self.driver.get('localhost:8000/')
#         # username = self.driver.find_element_by_css_selector("input#id_username")
#         # username.clear()
#         # username.send_keys("bteeuwen")
#         # password = self.driver.find_element_by_css_selector("input#id_password")
#         # password.clear()
#         # password.send_keys("geen")
#         # self.driver.find_element_by_css_selector("input[type='submit']").click()
#         # body = self.driver.find_element_by_tag_name('body')
#         # self.assertIn('Hercules', body.text)

#     def tearDown(self):
#         self.driver.quit()
#         self.assertEqual([], self.verificationErrors)

# class Substitutes(TestCase):
#     fixtures = [fix_real]

#     def test_playersubstituteboolean(self):
#         players = Player.objects.all()
#         p = players[10]
#         p.substitutewilling = True
#         p.save()
#         self.assertEqual(p.substitutewilling, True)

#     # ylayer willing to substitute visible at invallerslijst below match
#     # subs needed = appearance global with amount thats needed
#     # email link player works
#     # player receives text with exact match data as imported (timezone!)
