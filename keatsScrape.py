'''
Author: Ross Henry
Date:4/2/2018
'''

import requests, argparse, os, re
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

def createDir(cwd, sectionName, subSection = None):
    if subSection:
        pathway = cwd + '/' + sectionName + '/' + subSection
    else:
        pathway = cwd + '/' + sectionName
    if not os.path.exists(pathway):
        os.makedirs(pathway)
        print('Folder Created: ' + sectionName + '/' + subSection)
    else:
        print('Folder exists')

def createFile(s, fileName, pathway, fileURL, fileType=None):
    if fileType:
        filePathway = pathway+'/'+fileName +'.'+fileType
    else:
        filePathway = pathway+'/'+fileName

    if not os.path.exists(filePathway):
        fileData = s.get(fileURL)
        with open(filePathway, 'wb') as f:
            f.write(fileData.content)
        print('File created: %s' % fileName)
    else:
        print('File exists')


def main():
    # Parser for arguments
    pr = argparse.ArgumentParser()
    pr.add_argument("-pw", "--password", help="Password for Kings")
    pr.add_argument("-un", "--username", help="Username for Kings")
    pr.add_argument("-wd", "--workingDirectory", default=os.getcwd())
    pr.add_argument("-zp", "--zipfile", help="Zipfile", default=False)

    args = pr.parse_args()
    password = args.password
    username = args.username
    cwd = args.workingDirectory
    zp = args.zipfile
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
        print('%s Selected' %courses[course].a.get('title'))
        courseURL = courses[course].a.get('href')
        courseData = session.get(courseURL)
        courseHTML = BS(courseData.text, 'html.parser')
        sections =courseHTML.find_all("li", class_= 'section')
        for section in sections:
            # Skip over 'Not available'
            try:
                if section.find('h3').get_text() == 'Not available':
                    continue
            except:
                pass

            #Folder created
            sectionName = section.get('aria-label')
            createDir(cwd, sectionName)
            pathway = cwd + '/' + sectionName

            files = section.find_all("li", class_='activity')
            for filex in files:
                try:
                    fileName = filex.find('span').get_text()
                except AttributeError:
                    continue
                fileID = filex.find('a')
                # Folder
                if filex.find('img', src=re.compile('folder')):
                    fileType = 'folder - This is still to be supported'
                    print(fileType)
                # Feedback link
                elif (filex.find('img', src=re.compile('feedback'))):
                    print("Feedback link")
                # URL link
                elif (filex.find('img', src=re.compile('url'))):
                    print("URL link")
                # Assignment
                elif (filex.find('img', src=re.compile('assign'))):
                    print("Assignment Input")
                # Zip File
                elif (filex.find('img', src=re.compile('archive-24'))):
                    print("Zip file - still to be supported")
                # Source Code
                elif (filex.find('img', src=re.compile('sourcecode'))):
                    if zp:
                        fileURL = filex.find('a').get('href') + '&redirect=1'
                        createFile(session, fileName, pathway, fileURL)
                    else:
                        print('Source code')
                # PDF file
                elif (filex.find('img', src=re.compile('pdf'))):
                    fileURL = filex.find('a').get('href') + '&redirect=1'
                    createFile(session, fileName, pathway, fileURL, 'pdf')
                # Subfolder
                elif filex.find('span', style="color: #000000;"):
                    createDir(cwd, sectionName, fileName)
                    pathway = cwd + '/' + sectionName + "/" + fileName

                else:
                    fileType = 'File to be supported'

                    print(fileType)


if __name__ == '__main__':
    main()
