from typing import Union
import requests
from dotenv import dotenv_values
from urllib3.exceptions import InsecureRequestWarning
from .debug_info import debug_info


class DataHubEngine:

    @debug_info('DataHubEngine', 'initialization')
    def __init__(self, token, secret, flag1=None, flag2=None, flag3=None):
        self._settings = {}
        self._token = token
        self._secret = secret
        self.flag1 = flag1
        self.flag2 = flag2
        self.flag3 = flag3

    @debug_info('DataHubEngine', 'reading configuration')
    def _get_caller_settings(self) -> None:
        settings = dotenv_values(".env")
        self._settings = {
            **self._get_default_settings(),
            **dotenv_values(".env"),
        }

    def _get_default_settings(self):
        return {
            'DATAHUB_DEFAULT_URL': 'http://localhost:5173/api/v2/datahub',
            'DATAHUB_VERIFY_CERT': 'no'
        }

    @debug_info('DataHubEngine', 'fetching data')
    def _retrieve_data(self) -> Union[list, dict, str]:
        request_params = {
            'token': self._token,
            'secret': self._secret,
            'flag1': self.flag1,
            'flag2': self.flag2,
            'flag3': self.flag3,
        }
        info = None
        verifyCert = True
        if self._settings.get('DATAHUB_VERIFY_CERT', 'yes') == 'no':
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            verifyCert = False
        else:
            verifyCert = True
        try:
            data = requests.post(
                url=self._settings.get('DATAHUB_DEFAULT_URL'),
                json=request_params,
                verify=verifyCert
            )
            info = data.json()
            return info
        except requests.exceptions.ConnectionError:
            print('\b'*32 + '!!! ConnectionError !!!'.ljust(32))
