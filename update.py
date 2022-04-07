#!/usr/bin/env python
import os
import time
import requests
import json
from bs4 import BeautifulSoup

# TODO: Handle macos and XDG_DATA_DIR
cache_dir = os.path.expanduser("~/.cache/subjects")

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
