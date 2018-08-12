"""A file to contain the InstaScrape project."""
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sqlite3
import requests
import shutil


# todo: ALWAYS REMEMBER: FOR THIS PROJECT, ID TO BE USED IS  @sidhusultann AND PASSWORD Sujinder64

DATABASE_NAMES = []
print("Length of Database Names: ", len(DATABASE_NAMES))

db_name = input("Enter the name of the database (no spaces please): ").strip()
print("The following database names have been taken: ")
for thename in DATABASE_NAMES:
    print(thename)

databasename = db_name + ".db"
conn = sqlite3.connect(databasename)
cursor = conn.cursor()
if db_name not in DATABASE_NAMES:
    DATABASE_NAMES.append(db_name)
    print("Length of DATABASE_NAMES: ", len(DATABASE_NAMES))
    cursor.execute("""CREATE TABLE Information (
                        Name text,
                        Username text,
                        Followers Integer,
                        Following Integer,
                        Display_Pic text)""")


def add_to_db(parsed_object: 'InstaParse', cursor_object):
    """Add information from the current profile to the database."""
    info = parsed_object.return_info()
    cursor_object.execute("INSERT INTO Information VALUES (?, ?, ?, ?, ?)", (info[0], info[1], info[2], info[3], info[4]))


def show_all_data(cursor: 'Cursor'):
    """Shows all data present within the database."""
    cursor.execute('SELECT * FROM Information')
    print('FETCHALL INITIATING!')
    x = cursor.fetchall()
    for y in x:
        print(y, end="\n")


class InstaParse:
    """A class that contains an instagram parser."""

    def __init__(self):  # , cursor, name_of_database
        """Initializes a InstaParse object."""
        self.username = input("What is your username? ").lower().strip()
        self.password = input("What is your password? ").strip()
        self.url = "http://instagram.com/accounts/login"
        self.path = '/Users/sultansidhu/Desktop/chromedriver'  # location of the chromedriver for selenium
        self.driver = webdriver.Chrome(self.path)
        self.pic_folder_path = '/Users/sultansidhu/Desktop/Python/InstaScrape/parsed_dps/'
        self.driver.get(self.url)
        self.currenturl = self.url
        self.currentprofile = ""
        self.signin()
        print('done!')

    def signin(self):
        """A function that takes the login credentials of the user and logs into the
        instagram account of the user."""
        usernamefield = self.driver.find_element_by_xpath('//input[@aria-label="Phone number, username, or email"]')
        usernamefield.send_keys(self.username)
        pwordfield = self.driver.find_element_by_xpath('//input[@aria-label="Password"]')
        pwordfield.send_keys(self.password)
        sleep(2)
        pwordfield.submit()

    def own_profile(self):
        """Navigates to the profile of the user himself."""
        self.currenturl = self.url[:self.url.find("accounts")] + self.username + "/"
        sleep(2)
        self.driver.get(self.currenturl)

    def get_following(self):
        """Gets the profiles that the user follows."""
        followbutton = self.driver.find_element_by_partial_link_text("following")
        sleep(2)
        followbutton.click()

    def go_to_target(self):
        """Takes the user to the target profile, searching by username."""
        user_entry = input("Please enter the desired username? ").strip()
        self.currentprofile = user_entry
        self.currenturl = "https://instagram.com/" + user_entry + "/"
        self.driver.get(self.currenturl)
        self.check_validity()
        # self.add_to_db(user_entry)

    def check_validity(self):
        """Checks if the username entered is valid or not."""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        error_message = soup.find('div', class_="error-container -cx-PRIVATE-ErrorPage__errorContainer -cx-PRIVATE-ErrorPage__errorContainer__")
        if error_message is not None:
            raise Exception("Invalid Username!")
        else:
            pass

    def return_info(self):
        """Add information from the current profile to the database."""

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        followers = soup.find('li', class_="Y8-fY").nextSibling.a.span.string
        following = soup.find('li', class_="Y8-fY").nextSibling.nextSibling.a.span.string
        name = soup.find('h1', class_="rhpdm").string
        user_name = self.currentprofile
        recent_pic_path = self.get_dp_path()
        return [followers, following, name, user_name, recent_pic_path]

    def get_dp_path(self):
        """Downloads the display pic of the specified profile and then downloads their display pic. Returns path."""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        dp = soup.find('img')
        image_path = self.pic_folder_path + self.currentprofile + "dp"
        link = dp["src"]
        response = requests.get(link, stream=True)
        try:
            with open(image_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            return image_path
        except Exception as error:
            print(error)
            print('Could not download image from the internet!')

        # TODO: ANOTHER PROBLEM - CANNOT RECONNECT TO OLDER DATABASE
        # TODO: ANOTHER PROBLEM - NO DATABASE NAMES BEING ADDED TO THE DB NAMES LIST


if __name__ == "__main__":
    newparse = InstaParse()
    print('The program will now proceed to user\'s own profile.')
    newparse.own_profile()
    answer = input('Would you like to access profiles? Answer in yes or no ').strip().lower()
    while not answer == "no":
        newanswer = input("Would you like to continue?: ").strip().lower()
        if newanswer == "no":
            break
        newparse.go_to_target()
        newparse.get_dp_path()
        add_to_db(newparse, cursor)

    answer2 = input("Would you like to see all entries to the database? Answer in yes or no please. ").lower().strip()
    if answer2 == "yes":
        show_all_data(cursor)
