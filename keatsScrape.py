'''
Author: Ross Henry
Date:4/2/2018
'''

import requests
import argparse
from bs4 import BeautifulSoup as BS

def login(creditations,session):
    url='https://keats.kcl.ac.uk/login/index.php'
    r = session.post(url, data=creditations)
    try:
        if r.headers['Access-Control-Allow-Origin'] == 'https://login-keats.kcl.ac.uk':
            print('Login Successful')
            return r
    except:
        print('Username or password is incorrect. Check and retry')




def main():
    # Parser for arguments
    pr = argparse.ArgumentParser()
    pr.add_argument("-pw", "--password", help="Password for Kings")
    pr.add_argument("-un", "--username", help="Username for Kings")

    args = pr.parse_args()
    password = args.password
    username = args.username
    creditations = {'username': username, 'password': password}

    # Set up session
    with requests.Session() as session:
        htmlData = login(creditations, session)
        dashboardData = BS(htmlData.text, 'html.parser')
        courses = dashboardData.find_all("h2", class_= 'title')
        # Print courses with index
        for i in range(0,len(courses)-1):
            print('%d: %s'%(i, courses[i].a.get('title')))

        course = int(input('Index of course\n>>>'))
        courseURL = courses[course].a.get('href')
        print(courseURL)

if __name__ == '__main__':
    main()
