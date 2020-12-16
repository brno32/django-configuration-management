import os
import re
from getpass import getpass
from pathlib import Path

import yaml
from cryptography.fernet import Fernet
from dotenv import load_dotenv


def load_env(environment):
    env_path = Path(".") / f".env-{environment}"
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path, verbose=True)
        return

    print(
        f"env not found: {env_path}. This file is required and must contain your ENC_KEY"
    )
    exit(1)


def yml_to_dict(environment: str):
    try:
        with open(f"{environment}-config.yaml", "r") as yml:
            loaded: dict = yaml.safe_load(yml)
    except FileNotFoundError:
        loaded = {}
    return loaded


def dict_to_yml(data: dict, environment: str) -> str:
    with open(f"{environment}-config.yaml", "w+") as yml:
        dumped = yaml.dump(data, yml)
    return dumped


def gather_user_input():
    key_name = input("Enter key name: ")

    is_valid = re.search("^[A-Z]+(?:_[A-Z]+)*$", key_name)

    assert (
        is_valid
    ), f"Invalid key name. Keys must consist only of uppercase letters and underscore"

    key_value = getpass("Enter key value: ")

    return key_name, _encrypt_value(key_value)


def _encrypt_value(value: str, encoding="utf-8"):
    fernet = Fernet(os.getenv("ENC_KEY"))

    encrypted = fernet.encrypt(bytes(value, encoding))

    return encrypted.decode(encoding)


def decrypt_value(value: str, encoding="utf-8"):
    fernet = Fernet(os.getenv("ENC_KEY"))

    decrypted = fernet.decrypt(bytes(value, encoding))

    return decrypted.decode(encoding)


def generate_fernet_key():
    key = Fernet.generate_key()

    return key.decode("utf-8")