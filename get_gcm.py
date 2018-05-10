# download Google Camera apk from https://www.celsoazevedo.com/files/android/google-camera/
import os
import re
import subprocess
from bs4 import BeautifulSoup

name='index.html'
url='https://www.celsoazevedo.com/files/android/google-camera/'
cmd='wget -O %s %s' % (name,url)
subprocess.call(cmd,shell=True)

soup = BeautifulSoup(open('index.html'))
for line in soup.find_all(href=re.compile('.apk$')):
    url = "https://www.celsoazevedo.com" + line["href"]
    print url
    cmd='wget %s' % url
    subprocess.call(cmd,shell=True)
