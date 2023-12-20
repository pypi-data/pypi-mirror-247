import sys
import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogHandler(FileSystemEventHandler):
    def __init__(self, log_file_path, service_name, api_token):
        self.log_file_path = log_file_path
        self.service_name = service_name
        self.api_token = api_token

    def on_modified(self, event):
        with open(self.log_file_path, "r") as file:
            lines = file.readlines()
            last_line = lines[-1]
            self.send_log(last_line)

    def send_log(self, log_entry):
        headers = {"ApiToken": self.api_token}

        data = {
            "service_name": self.service_name,
            "message": log_entry,
        }

        print(data)

        response = requests.post(
            "https://observer.goltsev.net/api/v1/sendlog/",
            headers=headers,
            data=data,
        )
        print("Log sent, status code:", response.text)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        log_file_path, service_name, api_token = sys.argv[1], sys.argv[2], sys.argv[3]
        observer = Observer()
        observer.schedule(
            LogHandler(log_file_path, service_name, api_token),
            path="/var/log",
            recursive=False,
        )
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        raise ValueError(
            "You must provide path to the log file, service name, and API token as arguments."
        )
