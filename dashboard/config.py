import tomllib

class Config:
    def __init__(self, filename='config.toml'):
        self.filename = filename

        with open(filename, 'rb') as f:
            self.data = tomllib.load(f)
