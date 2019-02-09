#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest



class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes to tcheck out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathres')

        # When she hits enter, the page updates, and now the page lists
        # 1: By peacock feathres@ as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # There is still a test bo inviting her to add another item. She
        # enters "Use pacock feathres" as an item
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        self.fail('Finish thet test!')

        # The page updates again, and now shows both items on her list

        # Edith wonders wither the site will remember her list. The she 
        # sees that the site has generated a uniwue URL for her -- there 
        # is some eplanatory text to that effect

        # She visiets that URL - her to-do list is still there

        # Satified she goes back to sleep

if __name__ == '__main__':
        unittest.main(warnings='ignore')