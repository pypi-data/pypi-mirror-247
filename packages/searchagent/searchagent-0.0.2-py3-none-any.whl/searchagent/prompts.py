import json
import logging
import pathlib

class Prompts:
    '''Stores prompts so you dont have to.'''
    def __init__(self):
        self.name = "prompts"
        self.logger = logging.getLogger(f"{self.name}")
        self.logger.setLevel(logging.ERROR)
        self.file_path = pathlib.Path(__file__).parent.resolve()
        self.config_file = pathlib.Path(self.file_path) / f"{self.name}.json"
        self.data = self.load_json(self.config_file)

    def load_json(self,filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    
    def get_data(self):
        return self.data
