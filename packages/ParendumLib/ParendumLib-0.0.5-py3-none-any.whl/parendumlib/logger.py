import requests
import logging
import hashlib
import hmac
import time


class Logger:

    def __init__(self, domain: str, api_key: str, api_secret: str, port: int = 5626, ssl: bool = True, log_file: str = None):
        self.protocol = "https" if ssl else "http"
        self.endpoint = f"{self.protocol}://{domain}:{port}"
        self.api_key = api_key
        self.api_secret = api_secret.encode()

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        if log_file:
            self.file_handler = logging.FileHandler(log_file)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

    def _generate_signature(self, timestamp: str) -> str:
        """
        Generate HMAC signature using the provided timestamp.

        Args:
            timestamp (str): The timestamp to be used in signature generation.

        Returns:
            str: The generated HMAC signature.
        """
        return hmac.new(self.api_secret, timestamp.encode(), digestmod=hashlib.sha256).hexdigest()

    def _get_hmac_headers(self) -> dict:
        """
        Generate the HMAC headers required for API requests.

        Returns:
            dict: A dictionary containing the required headers.
        """
        timestamp = str(int(time.time()))
        return {
            "X-Signature": self._generate_signature(timestamp),
            "X-Timestamp": timestamp,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _do_post(self, url: str, body: dict = None) -> dict:
        """
        Make a POST request to the specified URL.

        Args:
            url (str): The URL to make the request to.
            body (dict, optional): The body of the request. Defaults to None.

        Returns:
            dict: The API response.
        """
        try:
            response = requests.request("POST", url, headers=self._get_hmac_headers(), json=body)
            if response.status_code == 200:
                return response.json()
            return dict(code=response.status_code, error=response.json())
        except Exception as e:
            return dict(code=500, error=str(e))

    def log(self, level: str, function: str, message: str, status_code: int, elapsed_time: int,
            arguments: list[str] = None, content: dict = None):
        _new_log = dict(
            function=function,
            message=message,
            level=level.lower(),
            status_code=status_code,
            elapsed_time=elapsed_time
        )
        if arguments:
            _new_log["arguments"] = arguments
        if content:
            _new_log["content"] = content
        if hasattr(logging, level):
            getattr(logging, level)(f"[{function}] {message}")
        else:
            logging.info(f"[{level}:{function}] {message}")
        self._do_post(f"{self.endpoint}/logs/new", body=_new_log)
