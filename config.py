import json
import logging

class Config:
    def __init__(self, filename):
        self.name: str = None
        self.defaults: dict = {}
        self.controllers: list = []

        self.json = self.load_config(filename)
        if self.json is None:
            return

        self.parse_controllers()

        logging.info(f"Parsed config")

    @staticmethod
    def load_config(filename):
        try:
            with open(filename) as f:
                data = json.load(f)
            logging.info("Loaded config file")
            return data
        except OSError:
            logging.critical(f"Couldn't load config file: {filename}")
            return None

    def parse_controllers(self):
        if "controllers" in self.json and isinstance(self.json["controllers"], list):
            for controller in self.json["controllers"]:
                self.controllers.append(ControllerConfig(controller, self))
        elif "controllers" not in self.json:
            logging.error('No "controllers" list in config file')
        elif not isinstance(self.json["controllers"], list):
            logging.error('"controllers" object in config file is not a list')

class ControllerConfig:
    def __init__(self, json, parent):
        self.type: str = None
        self.params: dict = []

        self.json = json
        self.parent = parent

        self.parse()

        logging.info(f"Parsed config for {self.type} controller")
    
    def parse(self):
        if "type" in self.json:
            self.type = self.json["type"]
        else:
            logging.error("No type specified for one of the controllers")

        if "params" in self.json and isinstance(self.json["params"], list):
            for param in self.json["params"]:
                self.params.append(ParamConfig(param, self))
        elif "params" not in self.json:
            logging.error(f'No "params" list in config for {self.type} controller')
        elif not isinstance(self.json["params"], list):
            logging.error(f'"params" object in config for {self.type} controller is not a list')

class ParamConfig:
    def __init__(self, json, parent):
        self.type: str = None
        self.name: str = None

        self.json = json
        self.parent: ControllerConfig = parent
        
        self.parse()

        logging.info(f"Parsed config for {self.name} parameter")      

    def parse(self):
        if "type" in self.json:
            self.type = self.json["type"]
        else:
            logging.error(f"No type specified for one of the params in {self.parent.type} controller")

        if "name" in self.json:
            self.name = self.json["name"]
        else:
            logging.error(f"No name specified for one of the params in {self.parent.type} controller")
