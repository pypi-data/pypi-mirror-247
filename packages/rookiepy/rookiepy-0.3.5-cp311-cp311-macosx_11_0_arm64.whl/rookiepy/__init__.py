from sys import platform
from typing import List
import http.cookiejar
from .rookiepy import (
    firefox,
    firefox_based,
    brave, 
    edge, 
    chrome, 
    chromium_based, 
    chromium, 
    opera, 
    vivaldi,
    opera_gx,
    libre_wolf,
    load,
    any_browser
)

__all__ = [
    "firefox",
    "libre_wolf",
    "brave",
    "edge",
    "chrome",
    "chromium",
    "opera",
    "opera_gx",
    "vivaldi",
    "chromium_based",
    "firefox_based",
    "to_dict",
    "to_cookiejar",
    "create_cookie",
    "load",
    "any_browser"
]


# Windows
if platform == "win32":
    from .rookiepy import internet_explorer, octo_browser
    __all__.extend([
        "internet_explorer",
        "octo_browser"
    ])

# MacOS
if platform == "darwin":
    from .rookiepy import safari
    __all__.extend([
        "safari"
    ])


def create_cookie(host, path, secure, expires, name, value, http_only):
    """Shortcut function to create a cookie"""
    # HTTPOnly flag goes in _rest, if present (see https://github.com/python/cpython/pull/17471/files#r511187060)
    return http.cookiejar.Cookie(0, name, value, None, False, host, host.startswith('.'), host.startswith('.'), path,
                                 True, secure, expires, False, None, None,
                                 {'HTTPOnly': ''} if http_only else {})

def to_cookiejar(cookies: List[dict]):
    cj = http.cookiejar.CookieJar()
    
    for cookie_obj in cookies:
        c = create_cookie(
            cookie_obj['domain'],
            cookie_obj['path'],
            cookie_obj['secure'],
            cookie_obj['expires'],
            cookie_obj['name'],
            cookie_obj['value'],
            cookie_obj['http_only'],

        )
        cj.set_cookie(c)
    return cj