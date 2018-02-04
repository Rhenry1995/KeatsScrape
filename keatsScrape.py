'''
Author: Ross Henry
Date:4/2/2018
'''

import requests
import argparse
from bs4 import BeautifulSoup as BS

def login(password, username):

    payload = {'username': username, 'password': password}
    url='https://keats.kcl.ac.uk/login/index.php'
    r = requests.post(url, data=payload)
    try:
        if r.headers['Access-Control-Allow-Origin'] == 'https://login-keats.kcl.ac.uk':
            print('Login Successful')
            return r
    except:
        print('Username or password is incorrect. Check and retry')


def findData(htmlData):
    data = BS(htmlData, 'html.parser')
    #print(data.prettify())



def main():
    # Parser for arguments
    pr = argparse.ArgumentParser()
    pr.add_argument("-pw", "--password", help="Password for Kings")
    pr.add_argument("-un", "--username", help="Username for Kings")

    args = pr.parse_args()
    password = args.password
    username = args.username

    htmlData = login(password, username)
    #findData(htmlData)


if __name__ == '__main__':
    main()
