import configparser

class AppConfigurations:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
    def get_value(self, section, key):
        return self.config[section][key]
