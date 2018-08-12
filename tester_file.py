"""A file to bullshit in."""
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sqlite3

url = 'http://instagram.com/accounts/login'
path = '/Users/sultansidhu/Desktop/chromedriver'
driver = webdriver.Chrome(path)
driver.get(url)
username = input('username: ').strip()
password = input('password: ').strip()


def signin():
    """A function that takes the login credentials of the user and logs into the
    instagram account of the user."""
    usernamefield = driver.find_element_by_xpath('//input[@aria-label="Phone number, username, or email"]')
    usernamefield.send_keys(username)
    pwordfield = driver.find_element_by_xpath('//input[@aria-label="Password"]')
    pwordfield.send_keys(password)
    sleep(2)
    pwordfield.submit()


signin()
sleep(5)
newurl = 'http://instagram.com/sidhu_saaab/'
driver.get(newurl)


def get_numbers(driver):
    """Returns a list containing the number of followers and number of following from an ig account."""
    soup = BeautifulSoup(driver.page_source, 'lxml')
    followers = soup.find("li", class_="Y8-fY").nextSibling.a.span.string
    following = soup.find("li", class_="Y8-fY").nextSibling.nextSibling.a.span.string
    name = soup.find('h1', class_='rhpdm').string
    return [followers, following, name]


followers = get_numbers(driver)[0]
following = get_numbers(driver)[1]
name = get_numbers(driver)[2]
print(followers, "///////",  following, "..........", name)

connection = sqlite3.connect('test2.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM Information')
y = cursor.fetchall()
for x in y:
    print(x, end="\n\n")

