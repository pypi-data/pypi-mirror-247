from collections.abc import Mapping
import logging
from typing import Any, Dict, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from logging import _FormatStyle


class FileLogFormatter(logging.Formatter):
    def __init__(self, 
                 fmt: str | None = None, 
                 datefmt: str | None = None, 
                 style: "_FormatStyle" = "%", 
                 validate: bool = True, *, 
                 defaults: Mapping[str, Any] | None = None) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

class ConsoleLogFormatter(logging.Formatter):
    RESET: str = "\033[0m" # "\x1b[0m"
    LEVELS: Dict[int, str] = {}

    test = {
        "test": "\x1b[36:36m"
    }

    def __init__(
        self,
        fmt: Union[str, None] = None,
        datefmt: Union[str, None] = None,
        style: "_FormatStyle" = "%",
        validate: bool = True,
        use_colors: bool = True,
        colors: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate)
        self._use_colors = use_colors
        if self._use_colors and colors is not None and fmt is not None:
            for level, color in colors.items():
                log_level = logging._nameToLevel[level]
                self.LEVELS[log_level] = color.encode("utf-8").decode("unicode-escape")

    def format(self, record: logging.LogRecord):
        log_fmt = self._fmt
        if self._use_colors:
            all_logging_levels: Dict[str, int] = logging.getLevelNamesMapping()
            for level_name, _ in all_logging_levels.items():
                if record.levelname == level_name:
                    log_color = self.LEVELS.get(record.levelno)
                    log_fmt = log_color + log_fmt + self.RESET
        return log_fmt % record.__dict__
