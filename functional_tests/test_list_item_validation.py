#!/usr/bin/env python
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
    
    def check_input_state(self, valid):
        selector_text = '#id_text:valid' if valid else '#id_text:invalid'
        self.browser.find_element_by_css_selector(selector_text)

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        self.wait_for(lambda: self.check_input_state(False))


        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.check_input_state(True))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.check_for_row_in_list_table('1: Buy milk'))

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.check_input_state(False))
        # She receives a similar warning on the list page




        self.get_item_input_box().send_keys('Make Tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.check_for_row_in_list_table('1: Buy milk'))
        self.wait_for(lambda: self.check_for_row_in_list_table('2: Make Tea'))