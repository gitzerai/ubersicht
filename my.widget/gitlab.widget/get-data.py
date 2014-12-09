#!/usr/bin/python
import sys, os
import json
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import Widget

widget = Widget('gitlab')

GITLAB_PRIVATE_TOKEN = 'YOUR_PRIVATE_TOKEN'
GITLAB_BASE_URL = 'GITLAB_BASE_URL'

data = {}
local_projects = {}
auth = {'private_token': GITLAB_PRIVATE_TOKEN}

try:
    projects = widget.get_response(GITLAB_BASE_URL + '/api/v3/projects', 'GET', auth).json()

    for project in projects:
        local_projects[project['id']] = project['name_with_namespace']

    for id, name in local_projects.items():
        merge_requests = widget.get_response(GITLAB_BASE_URL + '/api/v3/projects/{}/merge_requests?state=opened'.format(id), 'GET', auth).json()
        data[name] = {}
        for merge_request in merge_requests:
            merge_request_comments = widget.get_response(GITLAB_BASE_URL + '/api/v3/projects/{}/merge_request/{}/comments'.format(id, merge_request['id']), 'GET', auth).json()
            data[name]['requests'] = len(merge_requests)
            data[name]['comments'] = len(merge_request_comments)

except requests.ConnectionError as ce:
    data['Error'] = 'Cannot connect to GitLab'

print json.dumps(data) if isinstance(data, (dict, list, tuple, set)) else data.encode('utf-8')
sys.exit()
