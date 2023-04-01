import requests
from flask import Flask, request, Response
import json
import time
from datetime import datetime
import pytz
app = Flask(__name__)
import logging
import os
from datetime import timedelta

log_to_file = True
log_directory = "/var/log/grafana_proxy/"

if log_to_file:
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = os.path.join(log_directory, "grafana_proxy.log")
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)

token_url = "IP:8080/api/1/login/"
target_api_base_url = "IP:8080/api/1/"
username = "your_user"
password = "your_password"

token_data = {
    'access_token': None,
    'created_at': 0,
    'expires_in': 0
}

def get_access_token():
    response = requests.post(token_url, params={'username': username, 'password': password})
    if response.status_code == 200:
        response_data = response.json()
        expires_datetime = datetime.strptime(response_data['expires'], '%Y-%m-%d %H:%M:%S.%f')
        token_data = {
            'access_token': response_data['token'],
            'created_at': time.time(),
            'expires_in': int(expires_datetime.timestamp()) - int(time.time())
        }
        return token_data
    else:
        raise Exception(f"Error obtaining access token. Status code: {response.status_code}, Response text: {response.text}")

def refresh_token_if_needed():
    global token_data
    current_time = time.time()
    token_age = current_time - token_data['created_at']
    if token_age >= token_data['expires_in'] - 60:
        token_data = get_access_token()

def convert_to_timezone(date_str, from_timezone, to_timezone):
    from_tz = pytz.timezone(from_timezone)
    to_tz = pytz.timezone(to_timezone)
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    date_obj = from_tz.localize(date_obj)
    date_obj = date_obj.astimezone(to_tz)
    
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    refresh_token_if_needed()
    target_url = target_api_base_url + path
    headers = {'x-access-token': token_data['access_token']}
    
    # Convert the 'from' and 'to' timestamps to the desired timezone
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if from_date and to_date:
        # Apply -2 hours shift
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S") - timedelta(hours=4)
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S") - timedelta(hours=4)

        from_date = from_date_obj.strftime("%Y-%m-%d %H:%M:%S")
        to_date = to_date_obj.strftime("%Y-%m-%d %H:%M:%S")

        from_date = convert_to_timezone(from_date, "UTC", "Europe/Oslo")
        to_date = convert_to_timezone(to_date, "UTC", "Europe/Oslo")
    
    # Update the 'from' and 'to' arguments in the request
    request.args = request.args.copy()
    request.args['from'] = from_date
    request.args['to'] = to_date

    # Log the timestamps being sent to the server
    logging.debug(f"Timestamps sent to server: from={from_date}, to={to_date}")

    response = requests.request(request.method, target_url, headers=headers, params=request.args)

    return Response(response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    token_data = get_access_token()
    app.run(host='0.0.0.0', port=8081, debug=True)