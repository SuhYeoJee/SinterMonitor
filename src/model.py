if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
import json
# ===========================================================================================
class Model():
    def __init__(self):
        self.config = self.get_config()
        self.data_spec = self.get_data_spec()
        ...
    def get_val(self):
        return self.config.get("text","val")
    
    def get_config(self,section:str="DEFAULT",config_path:str="config.txt",enc:str="utf-8"):
        config = ConfigParser()
        config.read(config_path,enc)
        return config[section]
    
    def get_data_spec(self):
        with open("./src/spec/data.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data     
# ===========================================================================================
if __name__ == "__main__":
    m = Model()
    print(m.get_val())
