import logging
import requests
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)


class APIHandler(logging.Handler):
    def __init__(self, url, api_key, service_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.api_key = api_key
        self.service_name = service_name
        self.is_sending = False

    def emit(self, record):
        if self.is_sending:
            return
        self.is_sending = True
        log_entry = {
            "service_name": self.service_name,
            "log_level": record.levelname,
            "message": record.getMessage(),
        }

        headers = {"ApiToken": self.api_key}

        def send_log():
            try:
                response = requests.post(self.url, headers=headers, data=log_entry)
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except Exception as err:
                print(f"Error occurred: {err}")
            finally:
                self.is_sending = False

        executor.submit(send_log)
