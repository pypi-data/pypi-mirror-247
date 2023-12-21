import threading
import requests
import logging
import hashlib
import inspect
import hmac
import time


class Logger:

    def __init__(self, domain: str, api_key: str, api_secret: str, port: int = 5626, ssl: bool = True, log_file: str = None):
        self.protocol = "https" if ssl else "http"
        self.endpoint = f"{self.protocol}://{domain}:{port if not ssl else 443}"
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
            response = requests.request("POST", url, headers=self._get_hmac_headers(), json=body, timeout=2)
            if response.status_code == 200:
                return response.json()
            return dict(code=response.status_code, error=response.json())
        except Exception as e:
            return dict(code=500, error=str(e))

    def _log(self, level: str, function: str, message: str, status_code: int, elapsed_time: int = None,
             arguments: list = None, content: dict = None):
        _new_log = dict(
            function=function,
            message=message,
            level=level.lower(),
            status_code=status_code or 0,
            elapsed_time=elapsed_time
        )
        if arguments:
            _new_log["arguments"] = arguments
        if content:
            _new_log["content"] = content
        if hasattr(self.logger, level):
            getattr(self.logger, level)(f"[{function}] {message}")
        else:
            self.logger.info(f"[{level}:{function}] {message}")
        thread = threading.Thread(target=self._do_post, args=(f"{self.endpoint}/api/logs/new", _new_log, ))
        thread.start()

    def debug(self, message: str):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._log('debug', f"{caller_name}():{caller_line_no}", message, 100)

    def info(self, message: str):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._log('info', f"{caller_name}():{caller_line_no}", message, 200)

    def warning(self, message: str):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._log('warning', f"{caller_name}():{caller_line_no}", message, 400)

    def error(self, message: str):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._log('error', f"{caller_name}():{caller_line_no}", message, 500)

    def exception(self, message: str):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._log('exception', f"{caller_name}():{caller_line_no}", message, 600)
