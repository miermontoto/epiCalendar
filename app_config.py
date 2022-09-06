import os

CLIENT_ID = "250353b2-562b-4e19-83ff-6abc7ce3e925"
AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_PATH = "/getAToken"
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
SCOPE = ["User.Read.All"]
SESSION_TYPE = "filesystem"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_SECRET:
   raise ValueError("Need to define CLIENT_SECRET environment variable")