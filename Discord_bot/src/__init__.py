import json
import time
import random
import hashlib
import uuid
def get_config(key):
    config_file = "/home/Mystery700/discord_bot/bot-CTF/Discord_bot/src/config.json" # always use absolute path, not relative path
    file = open(config_file, "r")
    config = json.loads(file.read())
    file.close()
    
    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))

def generate_api_key():
    # Generate a random UUID as a string to be used as an API key
    api_key = str(uuid.uuid4())
    return api_key
