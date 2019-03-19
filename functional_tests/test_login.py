from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import time
import os
import poplib
from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['POP_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines=[l.decode('utf8') for l in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
                inbox.quit()

    def test_can_get_email_link_to_login(self):
        # Edith goes to the superlists site
        # and notices a Log in section in the navbar with the first item
        # it's telling her to enter her email, so she does

        if self.staging_server:
            test_email = 'lauratdduser@gmail.com'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # a message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # she checks her email and finds a message
        email_body = self.wait_for_email(test_email, SUBJECT)
        # it has a url link in it
        self.assertIn('Use this link to log in', email_body)
        url_search = re.search(r'http://.+/.+$', email_body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email_body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(test_email)


        # she now logs out
        self.browser.find_element_by_link_text('Log out').click()

        # she is logged out
        self.wait_to_be_logged_out(test_email)

        