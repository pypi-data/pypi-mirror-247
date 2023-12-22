import os
from getpass import getpass
from base64 import b64encode

TOKEN_FILE_NAME = ".user_secret_token"

def save_account_token_at_local_file(): 
    # get the logged user from windows
    user = os.environ.get("USERNAME")

    # get the logged user domain from windows
    user_domain = os.environ.get("USERDOMAIN")
    password_from_user = getpass(f"Olá {user_domain}\{user}! Digite sua senha para recuperar o token:\n")

    token = b64encode(f"{user_domain}\{user}:{password_from_user}".encode("utf-8")).decode(
        "ascii"
    )

    vinci_auth_path = retrieve_folder_of_vinci_auth()  

    if not os.path.exists(vinci_auth_path):
        os.makedirs(vinci_auth_path)

    with open(f"{vinci_auth_path}\\{TOKEN_FILE_NAME}", 'w') as f:
        f.write(token)

def retrieve_authorization_header_value() -> str:
    vinci_auth_path = retrieve_folder_of_vinci_auth()

    token = ""
    with open(f"{vinci_auth_path}\\{TOKEN_FILE_NAME}", 'r') as f:
        token = f.readline()

    return f"Basic {token}"

def retrieve_folder_of_vinci_auth(user: str) -> str:
    return f"C:\\Users\\{user}\\.vinci_auth"