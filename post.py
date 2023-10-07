from config import Config
import requests

def __get_smile(diff: int):
    if diff == 0:
        return ":D"
    
    if diff < 0:
        return "D':"
    
    if diff < 50:
        return ":)"
    
    if diff < 100:
        return ":|"
    
    if diff < 150:
        return ":/"
    
    if diff < 200:
        return ":("
    
    if diff < 250:
        return ":c"
    
    if diff < 300:
        return "D:"
    
    return "D':"

def format_message(info: dict):
    ed = info['edition']
    msg = info['message']
    smile = __get_smile(info['diff'])
    
    return f'{ed}: {msg} {smile}'

def format_yes_no(info: dict):
    smile = __get_smile(info['diff'])
    return ('Yes' if info['diff'] == 0 else 'No') + ' ' + smile

class Post:
    def __init__(self, cfg: Config):
        self.config = cfg
    
    async def post(self, img_url: str, message: str):
        pass
