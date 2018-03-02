# KeatsScrape
Program which is used to download documents from KCL's learning environment, KEATS. It will download the documents into a their respected folder and not download file if it is already present.

## Requirements
Program is in python3. To download the required files using the following command

`pip3 install -r requirements.txt`

## Input
To run the program enter the following code with adding your username or password. The directory for the destination is optional. If not included it will use the current working directory.

Including a `-zp` tag will allow the download of zip files and source code

`python3 KeatsScrape -pw yourPassword -un yourUsername -wd directoryOfdestination(optional) -zp downloadZipFiles(optional)`


## Note
This branch as a ssl workaround currently in place, `verify=false`, for log in. this means that it should be used at own risk. Bug will be fixed when possible
