__author__ = 'Lothilius'

from selenium.webdriver.support.select import Select
from selenium import webdriver, common
from authentication import salesforce_login_staging
import sys
import string
import random

baseurl = "https://cs13.salesforce.com/005?retURL=%2Fui%2Fsetup%2FSetup%3Fsetupid%3DUsers&setupid=ManageUsers"
switch_url = 'https://cs13.salesforce.com/00550000002rCYS?noredirect=1'

browser = webdriver.Firefox()
browser.get(baseurl)

username, pw = salesforce_login_staging()


def string_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

# Create user first, and last name and email from random letters
def random_user_data():
    first_name = string_generator()
    last_name = string_generator()
    email_end = '@example' + string_generator(3) + '.com'
    email = ''.join([first_name, '.', last_name, email_end])

    return first_name, last_name, email


# Login function
def login(browser):
    #Write Username in Username TextBox
    browser.find_element_by_name("username").send_keys(username)

    #Write PW in Password TextBox
    browser.find_element_by_name("pw").send_keys(pw)

    #Click Login button
    browser.find_element_by_css_selector("#Login").click()

def fill_out_form(first_name, last_name, email, user_name, user_type):
    # Set first name
    browser.find_element_by_id('name_firstName').send_keys(first_name)
    # Clear and write Subject
    browser.find_element_by_id('name_lastName').clear()
    browser.find_element_by_id('name_lastName').send_keys(last_name)
    # Set Product
    browser.find_element_by_id('Email').send_keys(email)
    # Clear and fill Username
    browser.find_element_by_id('Username').clear()
    browser.find_element_by_id('Username').send_keys(user_name)

    if user_type == '100500000000D6z':
        # Select role
        Select(browser.find_element_by_id("role")).select_by_value('00E50000000sBWP')
        # Fill License and Profile
        Select(browser.find_element_by_id("user_license_id")).select_by_value(user_type)
        Select(browser.find_element_by_id('Profile')).select_by_visible_text('Client Success')
    elif user_type == '10050000000M69y':
        # Fill License and Profile
        Select(browser.find_element_by_id("user_license_id")).select_by_value(user_type)
        Select(browser.find_element_by_id('Profile')).select_by_value('00e50000001BUwf')
    else:
        # Select role
        Select(browser.find_element_by_id("role")).select_by_value('00E50000000sBWP')
        print 'none'

    print first_name, last_name, user_type

    # Cick on Prioritize
    browser.find_element_by_id('new_password').click()

    # Save
    browser.find_element_by_name("save").click()
    browser.implicitly_wait(15)

def open_new_record():
    browser.implicitly_wait(4)
    displayed = browser.find_element_by_name("new").is_displayed()
    if not displayed:
        for i in range(0, 3):
            displayed = browser.find_element_by_name("new").is_displayed()
            if displayed:
                #Click New button
                browser.find_element_by_name("new").click()
                break
            else:
                browser.implicitly_wait(3)
    else:
        browser.find_element_by_name("new").click()


def create_user(user_type='100500000000D6z'):
    try:
        browser.implicitly_wait(5)
        open_new_record()
    except:
        print "Unexpected error 1:", sys.exc_info()[0]
        #Wait for page to load.
        browser.implicitly_wait(10)
        browser.find_element_by_name("new").click()

    first_name, last_name, email = random_user_data()
    try:
        fill_out_form(first_name, last_name, email, email, user_type)
    except:
        print "Unexpected error 2:", sys.exc_info()[0]

    # try:
    #     fill_out_form('martin', 'testing', 'martin.valenzuela@bazaarvoice.com', 'dup' + email, user_type)
    # except:
    #     print "Unexpected error 2b:", sys.exc_info()[0]

    try:
        browser.implicitly_wait(15)
        displayed = browser.find_element_by_id('errorDiv_ep').is_displayed()
        print displayed
        if displayed:
            the_error = browser.find_element_by_class_name('errorMsg').text
            print 'Oh no there is an error! \n'
            print the_error
        else:
            print 'We are good!'
            browser.get(baseurl)
    except common.exceptions.NoSuchElementException, e:
        print '3', e

def main():
    try:
        login(browser)
    except common.exceptions.ElementNotVisibleException:
        browser.implicitly_wait(3)
        login(browser)

    # Login in as Dave
    # try:
    #     browser.implicitly_wait(8)
    #     browser.find_element_by_name('login').click()
    #     browser.implicitly_wait(8)
    #     browser.get(baseurl)
    # except common.exceptions.NoSuchElementException, e:
    #     print '4', e

    # User license types [standard, platform, chatter], '100500000000D6z', '0050000000M7o4', '10050000000M69y
    user_types = ['100500000000D6z', '0050000000M7o4', '10050000000M69y']

    for each in user_types:
        create_user(each)


main()


