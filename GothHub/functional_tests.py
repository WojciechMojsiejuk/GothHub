from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_log_to_site(self):
        self.browser.get('http://localhost:8000/login/')

        #Title should inform it's a login page
        #self.assertIn('Login',self.browser.title)
        
        #Header should inform it's a login form
        header_text=self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Logowanie',header_text)
        
        #User provides username
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('JanKowlaski')

        #User provides password
        password_input = self.browser.find_element_by_id('id_password')
        password_input.send_keys('Haslo_to_okon')

        #User sends form
        password_input.send_keys(Keys.ENTER)
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
