from splinter import Browser
import time
import os
from urllib.parse import urljoin


SLEEP_BETWEEN_PAGES = 1


def check_env_variable(env_var_name):
    assert os.environ.get(env_var_name), \
        'The environment variable {v} should be set properly'.format(
            v=env_var_name)


def check_setup():
    check_env_variable('TARGET_SERVER')
    check_env_variable('OPENSHIFT_USERNAME')
    check_env_variable('OPENSHIFT_PASSWORD')


def front_page(browser, server):
    '''Go to the Openshift.io front page and click the Login button.'''
    url = server
    browser.visit(url)
    login_button = browser.find_by_css('button#login').first
    assert login_button.visible
    assert login_button.value == 'LOG IN'
    time.sleep(SLEEP_BETWEEN_PAGES)
    login_button.click()


def login_page(browser, server, username, password):
    '''Login into the Openshift.io using the provided username and
    password.'''
    username_input = browser.find_by_id('username').first
    password_input = browser.find_by_id('password').first
    assert username_input.visible
    assert password_input.visible
    browser.fill('username', username)
    browser.fill('password', password)
    login_button = browser.find_by_id('kc-login').first
    assert login_button.visible
    time.sleep(SLEEP_BETWEEN_PAGES)
    login_button.click()


def get_all_existing_space_names(browser):
    '''Returns list of names of Spaces.'''
    spaces = browser.find_by_xpath("//div[@class='space-item']/h2/a")
    assert spaces is not None
    names = [space.value for space in spaces]
    print("Already created Spaces")
    for name in names:
        print("    " + name)
    return names


def generate_space_prefix():
    localtime = time.localtime()
    return time.strftime("test%Y-%m-%d-")


def space_name(prefix, index):
    return "{p}{i}".format(p=prefix,i=index)


def is_space_name_unique(prefix, index, space_names):
    name = space_name(prefix, index)
    return name not in space_names


def generate_unique_space_name(space_names):
    '''Generate a name for a Space. The name is based on current date
    and is unique (by adding a small index to the date.'''
    prefix = generate_space_prefix()

    index = 1
    while not is_space_name_unique(prefix, index, space_names):
        index += 1
    return space_name(prefix, index)


def spaces_page(browser, server, username):
    '''Go to the Spaces page with list of available Spaces.'''
    url = urljoin(server, username+"/_spaces")
    browser.visit(url)
    space_names = get_all_existing_space_names(browser)
    new_space_name = generate_unique_space_name(space_names)

    time.sleep(SLEEP_BETWEEN_PAGES)


def run_tests(engine, server, username, password):
    with Browser(engine) as browser:
        front_page(browser, server)
        login_page(browser, server, username, password)


check_setup()
server = os.environ.get('TARGET_SERVER')
username = os.environ.get('OPENSHIFT_USERNAME')
password = os.environ.get('OPENSHIFT_PASSWORD')
engine = os.environ.get('BROWSER_ENGINE', 'chrome')

print("Using the following browser engine {e}".format(e=engine))

run_tests(engine, server, username, password)
