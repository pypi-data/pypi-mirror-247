import datetime
import google.protobuf.message
import google.protobuf.json_format
import logging
import logging.handlers
import os
import pathlib
import re
import signal
import socket


class Application:
    _terminating = False
    _logger = None

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_terminating() -> bool:
        """Return true if the user asks the application to terminate

        Returns:
            bool: True if application is terminating
        """
        return Application._terminating

    @staticmethod
    def _set_terminating(*args):
        Application._terminating = True

    @staticmethod
    def read_config(
        file: os.PathLike,
        config: google.protobuf.message,
    ):
        """Read json-based config file into protobuf message

        Args:
            file (os.PathLike): Config file to read
            config (google.protobuf.message): Protobuf message to merge into
        """
        configFile = pathlib.Path(file)
        with configFile.open(mode="r") as configStream:
            configText = configStream.read()
            return google.protobuf.json_format.Parse(
                configText, config, ignore_unknown_fields=True
            )

    @staticmethod
    def write_config(
        file: os.PathLike,
        config: google.protobuf.message,
    ):
        """Write json-based config file from protobuf message

        Args:
            file (os.PathLike): Config file to write
            config (google.protobuf.message): Protobuf message to write
        """
        configText = google.protobuf.json_format.MessageToJson(
            config,
            including_default_value_fields=True,
        )
        configFile = pathlib.Path(file)
        configFile.parent.mkdir(parents=True, exist_ok=True)
        with configFile.open(mode="w") as configFile:
            configFile.write(configText)

    @staticmethod
    def create_logger(
        file_name: os.PathLike = None,
        file_size: int = 10,
        file_count: int = 30,
        syslog_address: str = None,
        syslog_sockettype: socket.SocketKind = socket.SOCK_DGRAM,
    ):
        """Create logger with the specified handlers

        Args:
            file_name (os.PathLike, optional): File name of file handler. Do not create a file handler if set to None. Defaults to None.
            file_size (int, optional): Rotation size of file handler in MB. Defaults to 10.
            file_count (int, optional): Rotation count of file handler. Defaults to 30.
            syslog_address (str, optional): Address of syslog server. Do not create a syslog handler if set to None. Defaults to None.
            syslog_sockettype (socket.SocketKind, optional): Socket type of syslog server. Defaults to socket.SOCK_DGRAM.

        Returns:
            Logger: Logger created with specified handlers
        """
        assert Application._logger is None
        Application._logger = logging.getLogger()
        Application._logger.setLevel(logging.DEBUG)
        if file_name:
            pathlib.Path(file_name).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                file_name,
                maxBytes=1048756 * file_size,
                backupCount=file_count,
                encoding="UTF-8",
            )
            file_handler.setLevel(logging.NOTSET)
            file_formatter = _LevelFormatter()
            file_handler.setFormatter(file_formatter)
            Application._logger.addHandler(file_handler)
        if syslog_address:
            syslog_handler = logging.handlers.SysLogHandler(
                Application._split_address(syslog_address),
                socktype=syslog_sockettype,
            )
            syslog_handler.setLevel(logging.INFO)
            Application._logger.addHandler(syslog_handler)
        return Application._logger

    @staticmethod
    def get_logger():
        """Return the logger of current application. Logger must be created by create_logger() first.

        Returns:
            Logger: Logger of current application
        """
        assert Application._logger is not None
        return Application._logger

    @staticmethod
    def _split_address(address: str):
        match = re.match(r"^(.+):(\d+)$", address)
        if match:
            host = match.group(1)
            port = int(match.group(2))
        else:
            host = address
            port = None
        return (host, port)


class _DateTimeFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def formatTime(self, record, datefmt=None) -> str:
        ct = datetime.datetime.fromtimestamp(
            record.created, datetime.datetime.now().astimezone().tzinfo
        )
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime(self.default_time_format)
        return s


class _LevelFormatter(logging.Formatter):
    default_formatter = _DateTimeFormatter
    default_notset_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_debug_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_info_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_warning_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_error_format = (
        "%(levelname).1s %(asctime)s | %(message)s (%(module)s:%(lineno)d)"
    )
    default_critical_format = (
        "%(levelname).1s %(asctime)s | %(message)s (%(module)s:%(lineno)d)"
    )

    def __init__(self, formats=None, **kwargs):
        if "fmt" in kwargs:
            raise ValueError("format string must be passed by formats")
        if formats:
            if not isinstance(formats, dict):
                raise ValueError("formats must be a level to format string dictionary")
            self.formatters = {}
            for loglevel in formats:
                self.formatters[loglevel] = self.default_formatter(
                    fmt=formats[loglevel], **kwargs
                )
        else:
            self.formatters = {
                logging.NOTSET: self.default_formatter(
                    fmt=self.default_notset_format, **kwargs
                ),
                logging.DEBUG: self.default_formatter(
                    fmt=self.default_debug_format, **kwargs
                ),
                logging.INFO: self.default_formatter(
                    fmt=self.default_info_format, **kwargs
                ),
                logging.WARNING: self.default_formatter(
                    fmt=self.default_warning_format, **kwargs
                ),
                logging.ERROR: self.default_formatter(
                    fmt=self.default_error_format, **kwargs
                ),
                logging.CRITICAL: self.default_formatter(
                    fmt=self.default_critical_format, **kwargs
                ),
            }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self.formatters.get(
            record.levelno, self.formatters.get(logging.NOTSET)
        )
        return formatter.format(record)


signal.signal(signal.SIGINT, Application._set_terminating)
signal.signal(signal.SIGTERM, Application._set_terminating)
