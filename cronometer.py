
import os
import requests
import json
from datetime import datetime, timedelta

class CronometerClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = "https://cronometer.com"

    def login(self):
        login_url = f"{self.base_url}/login"
        credentials = {'username': self.username, 'password': self.password}
        response = self.session.post(login_url, data=credentials)
        response.raise_for_status()

    def get_servings(self, start_date, end_date):
        cache_file = 'cronometer_cache.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            cache_date = datetime.strptime(cache_data['date'], '%Y-%m-%d').date()
            if cache_date == datetime.today().date():
                return cache_data['servings']

        self.login()
        servings_url = f"{self.base_url}/api/v2/reports/servings"
        params = {'date_range': f'{start_date.isoformat()},{end_date.isoformat()}'}
        response = self.session.get(servings_url, params=params)
        response.raise_for_status()
        servings = response.json()

        with open(cache_file, 'w') as f:
            json.dump({'date': datetime.today().strftime('%Y-%m-%d'), 'servings': servings}, f)

        return servings
