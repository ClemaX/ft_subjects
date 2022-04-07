#!/usr/bin/env python
from sys import platform, exit
import os
import time
import requests
import json
from bs4 import BeautifulSoup

if platform == "linux" or platform == "linux2":
    xdg_data_dir = os.environ['XDG_CACHE_DIR'] or os.path.expanduser("~/.cache/")
    cache_dir = os.path.join(xdg_data_dir, subjects)
elif platform == "darwin":
    cache_dir = os.path.expanduser("~/Library/Caches/fr.42lyon.chamada.subjects")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
else:
    exit("This platform is not supported!")

with open(os.path.join(cache_dir, 'token')) as token_file:
	token = token_file.readline()

cookies = {
    '_intra_42_session_production': token,
}

projects_url = 'https://projects.intra.42.fr/projects'

response = requests.get(f'{projects_url}/list', cookies=cookies)

soup = BeautifulSoup(response.content, 'html.parser')
projects = soup.find_all('li', class_='project-item')

subjects = {}

for project in projects:
	name = project['data-name']
	response = requests.get(f'{projects_url}/{name}', cookies=cookies)
	project_soup = BeautifulSoup(response.content, 'html.parser')
	attachments = project_soup.find('div', class_='project-attachments-list')
	if attachments:
		subject = attachments.find('a', text='subject.pdf')
		if subject:
			subjects[name] = subject['href']
	time.sleep(0.5)

print(subjects)

with open(os.path.join(cache_dir, 'db.json'), 'w') as db:
	json.dump(subjects, db)
