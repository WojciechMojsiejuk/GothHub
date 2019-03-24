from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_log_to_site(self):
        self.browser.get('http://localhost:8000')
        assert 'Django' in self.browser.title
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
