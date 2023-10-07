import json, os

class Config:
    def __init__(self, json: dict):
        if 'edition_url' in json:
            self.edition_url = str(json['edition_url'])
        else:
            self.edition_url = None

        if 'start_date' in json:
            self.start_date = str(json['start_date'])
        else:
            self.start_date = None

        if 'end_date' in json:
            self.end_date = str(json['end_date'])
        else:
            self.end_date = None

        if 'edition_name' in json:
            self.edition_name = str(json['edition_name'])
        else:
            self.edition_name = None

        if 'generated_path' in json:
            self.generated_path = str(json['generated_path'])
        else:
            self.generated_path = './generated/'

        if 'assets_path' in json:
            self.assets_path = str(json['assets_path'])
        else:
            self.assets_path = './assets/'

        if 'sizes' in json:
            self.sizes = list(json['sizes'])
        else:
            self.sizes = [1920]

        if 'size' in json:
            self.sizes = [int(json['size'])]

        if 'telegram_token' in json:
            self.telegram_token = str(json['telegram_token'])
        else:
            self.telegram_token = None

        if 'telegram_channel' in json:
            self.telegram_channel = str(json['telegram_channel'])
        else:
            self.telegram_channel = None

        if 'info_json_url' in json:
            self.info_json_url = str(json['info_json_url'])
        else:
            self.info_json_url = None

        if 'banner_image_url' in json:
            self.banner_image_url = str(json['banner_image_url'])
        else:
            self.banner_image_url = None

    

def load_config(path) -> Config:
    if path == "[ENV]":
        return load_config_from_env()
    with open(path) as f:
        return Config(json.load(f))
    

def load_config_from_env() -> Config:
    d = dict()
    env = os.environ

    if 'EDITION_URL' in env:
        d["edition_url"] = str(env['EDITION_URL'])

    if 'START_DATE' in env:
        d["start_date"] = str(env['START_DATE'])

    if 'END_DATE' in env:
        d["end_date"] = str(env['END_DATE'])

    if 'EDITION_NAME' in env:
        d["edition_name"] = str(env['EDITION_NAME'])

    if 'GENERATED_PATH' in env:
        d["generated_path"] = str(env['GENERATED_PATH'])

    if 'ASSETS_PATH' in env:
        d["assets_path"] = str(env['ASSETS_PATH'])

    if 'SIZES' in env:
        d["sizes"] = env['SIZES'].split(',')

    if 'SIZE' in env:
        d["size"] = int(env['SIZE'])

    if 'TELEGRAM_TOKEN' in env:
        d["telegram_token"] = str(env['TELEGRAM_TOKEN'])

    if 'TELEGRAM_CHANNEL' in env:
        d["telegram_channel"] = str(env['TELEGRAM_CHANNEL'])

    if 'INFO_JSON_URL' in env:
        d["info_json_url"] = str(env['INFO_JSON_URL'])

    if 'BANNER_IMAGE_URL' in env:
        d["banner_image_url"] = str(env['BANNER_IMAGE_URL'])

    return Config(d)