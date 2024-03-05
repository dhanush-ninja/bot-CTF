import json
import time

def get_config(key):
    # get config from file JSON
    with open('/home/Dhanushliebe/discord_bot/config.json') as config_file:
        config = json.load(config_file)
        # close file
        config_file.close()

    if key in config:
        return config[key]
    else:
        raise Exception('Key not found in config file')

def time_ago(past_time):
    diff = int(time.time() - past_time)
    if diff < 1:
        return 'Just now'
    elif diff < 60:
        return str(diff) + ' seconds ago'
    elif diff < 3600:
        return str(int(diff / 60)) + ' minutes ago'
    elif diff < 86400:
        return str(int(diff / 3600)) + ' hours ago'
    elif diff < 604800:
        return str(int(diff / 86400)) + ' days ago'
    elif diff < 2419200:
        return str(int(diff / 604800)) + ' weeks ago'
    elif diff < 29030400:
        return str(int(diff / 2419200)) + ' months ago'
    else:
        return str(int(diff / 29030400)) + ' years ago'
    
def mask_key(key):
    return '*******' + key[-4:]