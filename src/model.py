if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
import json
import pymcprotocol
# ===========================================================================================

DEBUG = True

class Model():
    def __init__(self):
        self.config = self.get_config()
        self.data_spec = self.get_data_spec()
        self.pymc3e = self.connect_pymc()
    # -------------------------------------------------------------------------------------------
    def get_config(self,section:str="DEFAULT",config_path:str="config.txt",enc:str="utf-8"):
        config = ConfigParser()
        config.read(config_path,enc)
        return config[section]
    # --------------------------
    def get_data_spec(self):
        with open("./src/spec/data.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data     
    # --------------------------
    def ensure_connected(func):
        def wrapper(self, *args, **kwargs):
            if not self.pymc3e._is_connected:
                self.pymc3e = self.connect_pymc()
            if DEBUG or self.pymc3e._is_connected:
                return func(self, *args, **kwargs)
            else:
                return False #연결실패시 False 반환
        return wrapper

    def connect_pymc(self)->pymcprotocol.Type3E:
        pymc3e = pymcprotocol.Type3E()
        if DEBUG:return pymc3e
        try:
            pymc3e.connect("192.168.0.142", 1400)
        except: #연결실패
            print("pymc3e.connect.fail")
        return pymc3e
    # -------------------------------------------------------------------------------------------
    @ensure_connected
    def get_plc_data_by_addrs(self,words=[]):
        if DEBUG:return ['_'+x for x in words]
        return self.pymc3e.randomread(word_devices=words,dword_devices=[])
    # --------------------------
    def get_plc_data_by_dataset_name(self,dataset_name:str):
        dataset:dict = self.data_spec["plc_reg_addr"].get(dataset_name,{})
        revers_dataset = {v:k for k,v in dataset.items()}
        addrs = list(dataset.values())
        values = self.get_plc_data_by_addrs(addrs)

        return {revers_dataset[addrs[i]]:v for i,v in enumerate(values)}
    # --------------------------
    def get_plc_data_by_addr_names(self,dataset_name:str,addr_names:list):
        dataset:dict = {k:v for k,v in self.data_spec["plc_reg_addr"].get(dataset_name,{}).items() if k in addr_names}
        revers_dataset = {v:k for k,v in dataset.items()}
        addrs = list(dataset.values())
        values = self.get_plc_data_by_addrs(addrs)
        return {revers_dataset[addrs[i]]:v for i,v in enumerate(values)}
    # -------------------------------------------------------------------------------------------

# ===========================================================================================
if __name__ == "__main__":
    m = Model()
    print(m.get_plc_data_by_dataset_name("graph"))
    print(m.get_plc_data_by_addr_names("mould",["complete_l1"]))