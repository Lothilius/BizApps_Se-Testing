__author__ = 'Lothilius'

from selenium import webdriver, common
from authentication import salesforce_login_staging

import sys

baseurl = "https://cs13.salesforce.com/500W000000329Pb"

browser = webdriver.Firefox()
browser.get(baseurl)
browser.maximize_window()

username, pw = salesforce_login_staging()

# Login function
def login(browser):
    #Write Username in Username TextBox
    browser.find_element_by_name("username").send_keys(username)

    #Write PW in Password TextBox
    browser.find_element_by_name("pw").send_keys(pw)

    #Click Login button
    browser.find_element_by_css_selector("#Login").click()

try:
    login(browser)
except common.exceptions.ElementNotVisibleException:
    browser.implicitly_wait(3)
    login(browser)

try:
    #Click Edit button
    browser.find_element_by_name("edit").click()
except:
    print "Unexpected error:", sys.exc_info()[0]
    #Wait for page to load.
    browser.implicitly_wait(10)
    browser.find_element_by_name("edit").click()

try:
    # Select Status
    browser.find_element_by_id('cas7').send_keys('S')
    # Clear and write Subject
    browser.find_element_by_id('cas14').clear()
    browser.find_element_by_id('cas14').send_keys('This is cool!!')
    # Set Product
    browser.find_element_by_id('00N50000001xV5Z').send_keys('A&A Microsite')
    # Clear and fill Client Problem
    browser.find_element_by_id('00NW0000000tvln').clear()
    browser.find_element_by_id('00NW0000000tvln').send_keys('So this client ...')
    # Clear and fill Description
    browser.find_element_by_id('cas15').clear()
    browser.find_element_by_id('cas15').send_keys('Some description about the feature. ')
    # Clear and fill Value to customer
    browser.find_element_by_id('00NW0000000tvmR').clear()
    browser.find_element_by_id('00NW0000000tvmR').send_keys('The value to the customer will be this long thing...')
    # Cick on Prioritize
    browser.find_element_by_id('00NW0000000tzIk').click()

    # Save
    browser.find_element_by_name("save").click()

except:
    print "Unexpected error:", sys.exc_info()[0]


try:
    browser.implicitly_wait(15)
    displayed = browser.find_element_by_id('errorDiv_ep').is_displayed()
    if displayed:
        the_error = browser.find_element_by_id('errorDiv_ep').text
        print 'Oh no there is an error! \n'
        print the_error
    else:
        print 'We are good!'

except common.exceptions.NoSuchElementException, e:
    print e



