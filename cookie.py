import re
import sys

import connect


DEFAULT_COOKIE = "0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX"


# Verifies if the cookie is valid server-side.
# This check is slower than the basic cookie verification, but it is 100% reliable.
def verify_expiration(cookie) -> bool:
    if not verify_structure(cookie): return False
    return '<div id="j_id' in connect.first_request(cookie).text


# Quick client-side cookie verification.
# Checks if the structure of the cookie matches '0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX'.
def verify_structure(cookie) -> bool:
    return re.compile(r'^0000.{23}:1.{8}$').match(cookie) is not None and cookie != DEFAULT_COOKIE


if __name__ == "__main__":
    try:
        if not verify_structure(sys.argv[1]):
            print("Invalid cookie structure.")
            exit(1)
        if not verify_expiration(sys.argv[1]):
            print("Expired or invalid cookie.")
            exit(3)
        print("Valid cookie.")
        exit(0)
    except Exception:
        print("Usage: python3 cookie.py <cookie>")
        exit(2)
