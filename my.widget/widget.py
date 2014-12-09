import requests
import pickle
import logging
import urlparse
import json

LOCAL_PATH = 'my.widget'

class Widget:

    def __init__(self, widget_name):
        self.widget_name = widget_name
        pass

    def log(self, message):
        logging.basicConfig(filename='{}/{}/{}'.format(LOG_PATH, self.widget_name, 'widget.log'), level=logging.ERROR)
        logging.error(message)

    def parse_from_url(self, url, key):
        parsed_url = urlparse.urlparse(url)
        return parse_from_query(parsed_url.query)

    def parse_from_query(self, query, key):
        for param in query.split('&'):
            param_split = param.split('=')
            if param_split[0] == key:
                return param_split[1]

        return 'NOT_FOUND'

    def persist(self, key, value):
        pickle.dump(value, open("{}/{}.p".format(LOCAL_PATH, key), "wb"))

    def load_persisted(self, key):
        return pickle.load(open("{}/{}.p".format(LOCAL_PATH, key), "rb"))

    def get_response(self, url, method='GET', params={}, data={}, headers={}, content_type='application/json'):

        request_headers = {'Content-type': content_type}
        request_data = json.dumps(data) if (content_type == 'application/json') else data

        for header_name in headers:
            request_headers[header_name] = headers[header_name]

        response = requests.request(method, url, params=params, data=request_data, headers=request_headers)
        return response
