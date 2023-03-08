import json

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

def load_config(path) -> Config:
    with open(path) as f:
        return Config(json.load(f))