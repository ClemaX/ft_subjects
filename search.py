#!/usr/bin/env python
import os
import sys
import json


if len(sys.argv) != 2:
	sys.exit(f'Usage: {sys.argv[0]} TERM')

term = sys.argv[1]

# TODO: Handle macos and XDG_DATA_DIR
cache_dir = os.path.expanduser("~/.cache/subjects")

with open(os.path.join(cache_dir, 'db.json')) as db:
	subjects = json.load(db)

for name, url in subjects.items():
	if term in name:
		print(f'{name}\n\t{url}')
