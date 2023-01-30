import re
import sys

import connect

__version__ = "1.2"


# Verifies if the cookie is valid server-side.
# This check is slower than the basic cookie verification, but it is 100% reliable.
def verifyCookieExpiration(jsessionid) -> bool:
    if not verifyCookieStructure(jsessionid): return False
    return '<div id="j_id' in connect.firstRequest(jsessionid).text


# Quick cookie verification.
# Checks if the structure of the cookie matches '0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX'.
def verifyCookieStructure(cookie) -> bool:
    return re.compile(r'^0000.{23}:1.{8}$').match(cookie) is not None and cookie != "0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX"


if __name__ == "__main__":
    try:
        result = verifyCookieExpiration(sys.argv[1])
        print(result)
        exit(0 if result else 1)
    except Exception:
        print("Usage: python3 utils.py <cookie>")
        exit(2)
