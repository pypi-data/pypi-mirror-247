from typing import Any, Type, NamedTuple

from .abstracts import AbstractCodeVerify


Context = dict[str, Any]
Kwargs = dict[str, Any]
Code = Type[AbstractCodeVerify]


class TemplateFiles(NamedTuple):
    """Keeps mail templates file paths."""

    subject: str
    txt: str
    html: str
