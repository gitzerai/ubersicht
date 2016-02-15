#!/usr/bin/python
import sys, os
import json
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import Widget

widget = Widget('github')

GITHUB_PRIVATE_TOKEN = 'YOUR_GITHUB_PRIVATE_TOKEN'
GITHUB_BASE_URL = 'YOUR_GITHUB_URL'
GITHUB_USERNAME = 'YOUR_GITHUB_USERNAME'

USER_REPOSITORIES_URL = '{}/api/v3/users/{}/repos?type=all'.format(GITHUB_BASE_URL, GITHUB_USERNAME)
ALL_REPOSITORIES_URL = '{}/api/v3/repositories'.format(GITHUB_BASE_URL)

data = {}
local_repos = {}
auth = {'access_token': GITHUB_PRIVATE_TOKEN}

try:
    repos = widget.get_response(USER_REPOSITORIES_URL, 'GET', auth).json()

    for repo in repos:
        local_repos[repo['url']] = repo['full_name']

    for url, name in local_repos.items():
        requests = widget.get_response('{}/pulls'.format(url), 'GET', auth).json()

        data[name] = {}
        data[name]['requests'] = 0
        data[name]['comments'] = 0

        if requests:
            data[name]['requests'] = len(requests)

            for request in requests:
                comments_url = '{}/pulls/{}/comments'.format(url, request['number'])
                comments = widget.get_response(comments_url, 'GET', auth).json()
                data[name]['comments'] = len(comments)

except requests.ConnectionError as ce:
    data['error'] = 'Cannot connect to {}'.format(GITHUB_BASE_URL)

print json.dumps(data) if isinstance(data, (dict, list, tuple, set)) else data.encode('utf-8')

sys.exit()
