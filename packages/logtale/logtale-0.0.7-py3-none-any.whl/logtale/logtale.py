import logging
import pathlib
import sys
import threading
import toml
from typing import Optional

from logtale import formatter


class SingletonMeta(type):
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class LogTale(metaclass=SingletonMeta):
    _instance: Optional["LogTale"] = None
    _config = None
    _logger: logging.Logger
    
    _log_file_handler: logging.Handler
    _log_console_handler: logging.Handler

    @property
    def logger(self):
        return self._logger

    def __init__(self, software_name: str, config_file_path: str) -> None:
        self._config = self.initialize_log_config(config_file_path)
        if self._config is None:
            raise RuntimeError("logtale failed to initialize log config.")
        self._logger = self.initialize_logger(software_name)

    def initialize_log_config(self, config_file_path: str) -> dict:
        if not config_file_path:
            raise ValueError(f"invalid logtale config path provided: '{config_file_path}'")
        _cfg_instance: Optional[dict] = None
        try:
            with open(config_file_path, 'r') as log_cfg:
                _cfg_instance = toml.load(log_cfg)
        except IOError as io_exc:
            raise io_exc
        except TypeError as type_exc:
            raise type_exc
        except toml.TomlDecodeError as toml_exc:
            raise toml_exc
        return _cfg_instance

    def initialize_logger(self, software_name: str) -> logging.Logger:
        _log_file_dir: pathlib.Path = pathlib.Path.cwd() / (self._config["output"]["file"]["path"])

        # Enable file logging:
        _selected_file_level: str = self._config["output"]["file"]["level"]
        _enable_file_log = _selected_file_level.upper() != "NONE" and bool(self._config["output"]["file"]["enable"])
        if _enable_file_log:
            pathlib.Path.mkdir(_log_file_dir, parents=True, exist_ok=True)

        # Enable console logging:
        _selected_console_level: str = self._config["output"]["console"]["level"]
        _enable_console_log = _selected_console_level.upper() != "NONE" and bool(self._config["output"]["console"]["enable"])

        _logger = logging.getLogger(software_name)
        _logger.setLevel(logging.DEBUG)

        if _enable_file_log:
            file_handler = self.get_file_handler()
            if file_handler is not None:
                _logger.addHandler(file_handler)
                self._log_file_handler = file_handler
            else:
                raise RuntimeError("File log handler unable to initialize.")
        if _enable_console_log:
            console_handler = self.get_console_handler()
            if console_handler is not None:
                _logger.addHandler(console_handler)
                self._log_console_handler = console_handler
            else:
                raise RuntimeError("Console log handler unable to initialize.")

        if not _logger.hasHandlers():
            raise RuntimeError("No log handlers have been initialized.")

        # Make other loggers quiet unless there's a critical issue:
        for log_name in logging.Logger.manager.loggerDict.keys():
            if log_name != software_name:
                logging.getLogger(log_name).setLevel(logging.CRITICAL)

        return _logger

    def get_console_handler(self) -> Optional[logging.StreamHandler]:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self._config["output"]["console"]["level"])
        _logging_formatter = formatter.ConsoleLogFormatter(
            fmt=self._config["output"]["console"]["format"], 
            colors=self._config["output"]["colors"],
            use_colors=bool(self._config["output"]["console"]["use_colors"])
        )
        console_handler.setFormatter(_logging_formatter)
        return console_handler

    def get_file_handler(self) -> Optional[logging.FileHandler]:
        _logging_formatter = formatter.FileLogFormatter(fmt=self._config["output"]["file"]["format"])
        _log_name: str = self._config["output"]["file"]["name"]
        _log_location: pathlib.Path = pathlib.Path.cwd() / self._config["output"]["file"]["path"]
        _log_level: str = self._config["output"]["file"]["level"]
        _log_location_path: pathlib.Path = (_log_location / _log_name).resolve()

        file_handler = logging.FileHandler(filename=_log_location_path)
        file_handler.setLevel(_log_level)
        file_handler.setFormatter(_logging_formatter)
        return file_handler
