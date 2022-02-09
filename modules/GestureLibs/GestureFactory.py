from configparser import ConfigParser

parser = ConfigParser
class GestureFactory:
    
    def __init__(self, config: str) -> None:
        self.config_file = config    
        
    def read_config(self):
        parser.read(str(self.config_file))
        for config in parser.sections:
            name = parser[config][name]
            action = parser[config][action]
            fingers_up = parser[config][fingers_up]
            direction = parser[config][direction] 
            
        
            
    
    def write_config(self, name, fingers_up, direction, action):
        self.config.add_section(name)
        self.config.set(fingers_up, direction,action)
        with open(self.config_file) as configfile:
            parser.write(configfile)
