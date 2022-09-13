from datetime import datetime
from typing import Any, Optional
from urllib.parse import urljoin

import requests

# dev url & token
CONDUIT_API_URL = "https://api-dev.getconduit.app"
CONDUIT_API_TOKEN = " place api key here "


class ConduitAPI:
    @classmethod
    def get_token(cls, company_id: str):
        resp = cls._request(f'/link/company/{company_id}/')
        return resp['api_token']['token']

    @classmethod
    def get_companies(cls):
        resp = cls._request(f'/link/company/')
        return resp

    @classmethod
    def create_company(cls, company_id: str) -> None:
        data = {
            'id': company_id,
            'name': company_id,
            'page_enabled': True,
        }
        cls._request('/link/company/', data=data, method='POST')

    @staticmethod
    def _request(path, method: str = 'GET', data: dict[str, Any] = None):
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {CONDUIT_API_TOKEN}',
        }
        res = requests.request(method, urljoin(CONDUIT_API_URL, path), headers=headers, json=data)
        res.raise_for_status()
        return res.json()


class ConduitCompanyAPI:
    def __init__(self, token: str):
        self._token = token

    def get_credentials(self) -> list[dict[str, Any]]:
        resp = self._request('link/credentials/')
        return resp

    def get_ui_url(self) -> str:
        return urljoin(CONDUIT_API_URL, f'link/company/page/{self._token}/')

    def get_connect_url(self, integration_id: str) -> str:
        res = self._request(f'link/credentials/connect/{integration_id}/')
        return res['url']

    def get_data_urls(
            self,
            integration_id: str,
            date_from: datetime.date,
            date_to: datetime.date,
            account: Optional[str] = None,
    ) -> dict[str, list[str]]:
        data = {
            'integration': integration_id,
            'date_from': date_from.isoformat(),
            'date_to': date_to.isoformat(),
        }
        if account:
            data['account'] = account

        res = self._request('link/data_lake/', data)
        return res

    def _request(self, path: str, data: dict[str, Any] = None) -> Any:
        headers = {
            'accept': 'application/json',
        }
        data = data or {}
        data['token'] = self._token
        resp = requests.request('GET', urljoin(CONDUIT_API_URL, path), headers=headers, params=data)
        resp.raise_for_status()
        return resp.json()
