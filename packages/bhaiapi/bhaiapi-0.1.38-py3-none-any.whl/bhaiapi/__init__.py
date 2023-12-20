# Copyright 2023 Minwoo Park, MIT License.

from os import environ
from bhaiapi.core import Bhai
from bhaiapi.chat import BhaiChat
from bhaiapi.core_async import BhaiAsync
from bhaiapi.core_cookies import BhaiCookies, BhaiAsyncCookies
from bhaiapi.constants import (
    SESSION_HEADERS,
    ALLOWED_LANGUAGES,
    DEFAULT_LANGUAGE,
    SEPARATOR_LINE,
    USER_PROMPT,
    IMG_UPLOAD_HEADERS,
    Tool,
)
from bhaiapi.utils import (
    extract_links,
    upload_image,
    extract_bhai_cookie,
    max_token,
    max_sentence,
)
from bhaiapi.chatbot import *
# Get the API key from the environment variable
bhai_api_key = environ.get("_BARD_API_KEY")

__all__ = [
    "Bhai",
    "BhaiChat",
    "BhaiAsync",
    "BhaiCookies",
    "BhaiAsyncCookies",
    "SESSION_HEADERS",
    "ALLOWED_LANGUAGES",
    "DEFAULT_LANGUAGE",
    "IMG_UPLOAD_HEADERS",
    "SEPARATOR_LINE",
    "USER_PROMPT",
    "extract_links",
    "upload_image",
    "extract_bhai_cookie",
    "max_token",
    "max_sentence",
    "Tool",
]
__version__ = "0.1.0"
__author__ = "Hk4crprasad <hotahara12@gmail.com>"
