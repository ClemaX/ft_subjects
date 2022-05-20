#!/usr/bin/env python
from sys import argv, platform, exit
from os import environ, path, makedirs
import json


if len(argv) != 2:
    exit(f"Usage: {argv[0]} TERM")

term = argv[1]

if platform == "linux" or platform == "linux2":
	xdg_data_dir = environ.get('XDG_CACHE_DIR') or path.expanduser("~/.cache/")
	cache_dir = path.join(xdg_data_dir, "subjects")
elif platform == "darwin":
	cache_dir = path.expanduser("~/Library/Caches/fr.42lyon.chamada.subjects")
else:
    exit("This platform is not supported!")

if not path.exists(cache_dir):
	makedirs(cache_dir)

with open(path.join(cache_dir, 'db.json')) as db:
	subjects = json.load(db)

for name, url in subjects.items():
	if term in name:
		print(f'{name}\n\t{url}')
