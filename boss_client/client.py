import datetime
import time

import httpx

from urllib.parse import urljoin


class BossClient:
    def __init__(self, login_url, api_url, client_id, client_secret, base_url):
        self.login_url = login_url
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url

        self.access_token = None
        self.token_type = None
        self.access_token_expiration = None
        self.client = None

        self._ensure_access_token()

    @property
    def authorization_header(self):
        if not self.access_token or not self.token_type:
            return None
        return f"{self.token_type} {self.access_token}"

    def _is_access_token_expired(self):
        if self.access_token_expiration is None:
            return True
        return datetime.datetime.utcnow() >= self.access_token_expiration

    def _ensure_access_token(self):
        if self.access_token is None or self._is_access_token_expired():
            self.hent_access_token()

    def _ensure_http_client(self):
        if self.client is not None:
            self.client.close()

        headers = {}
        if self.authorization_header is not None:
            headers['Authorization'] = self.authorization_header

        self.client = httpx.Client(headers=headers)

    def hent_access_token(self):
        body = (
            f"grant_type=client_credentials&client_id={self.client_id}&scope={self.api_url}&client_secret={self.client_secret}"
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = httpx.post(self.login_url, content=body, headers=headers)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data.get('access_token')
        self.token_type = token_data.get('token_type', 'Bearer')

        expires_in = token_data.get('expires_in')
        if expires_in is not None:
            expires_in = int(expires_in)
            buffer_seconds = max(expires_in - 20, 0)
            self.access_token_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=buffer_seconds)
        else:
            self.access_token_expiration = None

        self._ensure_http_client()
        return response

    def dan_gracerapport(self):
        self._ensure_access_token()

        response = None
        max_attempts = 12
        attempt = 0

        while attempt < max_attempts:
            response = self.client.get(
                f"{self.base_url}/api/GraceReport/GenerateGraceReports"
            )
            if response.status_code == 200:
                return response

            attempt += 1
            time.sleep(300)

        if response is not None:
            response.raise_for_status()

        raise RuntimeError("Failed to get a 200 response from GenerateGraceReports within one hour.")
        

    def hent_systemer(self):
        self._ensure_access_token()
        response = self.client.get(
            f"{self.base_url}/api/rpa/SystemsToBeClosed"
        )

        if response.status_code == 200:
            return response.json()
        
        if response is not None:
            response.raise_for_status()
        return response.json()

    def marker_bruger_som_slettet(self, user_id : str):
        self._ensure_access_token()
        
        response = self.client.get(
            f"{self.base_url}/api/rpa/MarkSystemAsClosedForUser/{user_id}"
        )
        if response .status_code == 200:
            return response
        
        if response is not None:
            response.raise_for_status()
        return response