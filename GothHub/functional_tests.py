from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_log_to_site(self):
        #user is redirected to login page
        self.browser.get('http://localhost:8000/login/')

        #Title should inform it's a login page
        self.assertIn('Login',self.browser.title)

        #Header should inform it's a login form
        header_text=self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Logowanie',header_text)

        #User provides username
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('JanKowalski')

        #User provides password
        password_input = self.browser.find_element_by_id('id_password')
        password_input.send_keys('Haslo_to_okon')

        #User sends form
        password_input.send_keys(Keys.ENTER)

    def test_can_register_to_site(self):
        #user is redirected to registation page
        self.browser.get('http://localhost:8000/join/')

        #Title should inform it's a registation page
        self.assertIn('Registration',self.browser.title)

        #Header should inform it's a login form
        header_text=self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Rejestracja',header_text)

        #User provides username
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('JanKowalski')

        #User provides email address
        email_input = self.browser.find_element_by_id('id_email')
        email_input.send_keys('jankowalski@gmail.com')

        #User provides password
        password_input = self.browser.find_element_by_id('id_password1')
        password_input.send_keys('Haslo_to_okon')

        #User repeats password
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        password_confirm_input.send_keys('Haslo_to_okon')

        #User sends form
        password_confirm_input.send_keys(Keys.ENTER)

    @unittest.expectedFailure
    def test_user_provides_wrong_email(self):

        self.browser.get('http://localhost:8000/join/')
        #User provides username
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('JanKowalski')

        #User provides wrong email address
        email_input = self.browser.find_element_by_id('id_email')
        email_input.send_keys('jankowalski')

        #User provides password
        password_input = self.browser.find_element_by_id('id_password1')
        password_input.send_keys('Haslo_to_okon')

        #User repeats password
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        password_confirm_input.send_keys('Haslo_to_okon')

        #User sends form
        password_confirm_input.send_keys(Keys.ENTER)

    @unittest.expectedFailure
    def test_passwords_do_not_match(self):
        #User provides username
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('JanKowalski')

        #User provides email address
        email_input = self.browser.find_element_by_id('id_email')
        email_input.send_keys('jankowalski@gmail.com')

        #User provides password
        password_input = self.browser.find_element_by_id('id_password1')
        password_input.send_keys('Haslo_to_okon')
        
        #User repeats incorrect password
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        password_confirm_input.send_keys('Haslo_to_jednak_nie_okon')

        #User sends form
        password_confirm_input.send_keys(Keys.ENTER)


    class UserFunctionsTest(unittest.TestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()

        def tearDown(self):
            self.browser.quit()
        def test_can_upload_file_to_site(self):
            pass
        def test_can_create_repository(self):
            pass
        def test_can_create_catalogue(self):
            pass
        def test_can_change_name_of_a_file(self):
            pass
        def test_download_file(self):
            pass
        def test_can_delete_file(self):
            pass

if __name__ == '__main__':
    unittest.main(warnings='ignore')
