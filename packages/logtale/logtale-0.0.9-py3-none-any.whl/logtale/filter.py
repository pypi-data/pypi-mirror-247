import logging
from typing import Optional


class LogFilter(logging.Filter):
    def __init__(self, name: str = "", prepend_text: Optional[str] = None, postpend_text: Optional[str] = None) -> None:
        super().__init__(name)
        self._prepend = prepend_text
        self._postpend = postpend_text

    def filter(self, record: logging.LogRecord):
        record.msg = \
            f"{'['+self._prepend+']::' if self._prepend is not None else ''}" + \
            record.msg + \
            f"{'::['+self._postpend+']' if self._postpend is not None else ''}"
        return True
