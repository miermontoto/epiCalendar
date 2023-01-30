import re
import sys

import connect

__version__ = "1.3"


# Verifies if the cookie is valid server-side.
# This check is slower than the basic cookie verification, but it is 100% reliable.
def verifyExpiration(cookie) -> bool:
    if not verifyStructure(cookie): return False
    return '<div id="j_id' in connect.firstRequest(cookie).text


# Quick client-side cookie verification.
# Checks if the structure of the cookie matches '0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX'.
def verifyStructure(cookie) -> bool:
    return re.compile(r'^0000.{23}:1.{8}$').match(cookie) is not None and cookie != "0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX"


if __name__ == "__main__":
    try:
        if not verifyStructure(sys.argv[1]):
            print("Invalid cookie structure.")
            exit(1)
        if not verifyExpiration(sys.argv[1]):
            print("Expired cookie.")
            exit(1)
        print("Valid cookie.")
        exit(0)
    except Exception:
        print("Usage: python3 utils.py <cookie>")
        exit(2)
