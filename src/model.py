if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
import json
import pymcprotocol
# ===========================================================================================

DEBUG = True # pymc3e return randint(1,10)
# DEBUG = False


class Model():
    def __init__(self):
        self.config = self.get_config()
        self.data_spec = self.get_data_spec()
        self.pymc3e = self._connect_pymc()

    def __del__(self):
        self.disconnect_pymc()

    # [파일 데이터 읽기] ===========================================================================================
    def get_config(self,section:str="DEFAULT",config_path:str="config.txt",enc:str="utf-8"):
        config = ConfigParser()
        config.read(config_path,enc)
        return config[section]
    # --------------------------
    def get_data_spec(self):
        with open("./src/spec/data.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data     
    # [이더넷 IP 변경] ===========================================================================================
    def _find_adapter_name_by_mac(self,mac_address):
        import psutil
        for name, addresses in psutil.net_if_addrs().items():
            for address in addresses:
                if address.address.lower() == mac_address.lower():
                    return name
        return None

    def _change_ip(self):
        adapter_name = self._find_adapter_name_by_mac(self.config.get("plc_mac_address",""))
        import subprocess
        try:
            cmd = f'''netsh interface ip set address name="{adapter_name}" \
                  static {self.config.get('pc_ip_address',"192.168.0.200")} \
                    {self.config.get('subnet_mask',"255.255.255.0")} \
                    {self.config.get('ip_gateway',"192.168.0.1")}'''
            subprocess.run(cmd, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"오류 발생: {e}")
            return False    
    # [PLC 연결] -------------------------------------------------------------------------------------------
    def _ensure_connected(func):
        def wrapper(self, *args, **kwargs):
            if not self.is_connected():
                self.pymc3e = self._connect_pymc()
            if self.is_connected():
                return func(self, *args, **kwargs)
            else:
                return False #연결실패시 False 반환
        return wrapper

    def _connect_pymc(self)->pymcprotocol.Type3E:
        pymc3e = pymcprotocol.Type3E()
        if DEBUG:return pymc3e
        try:
            self._change_ip()
            pymc3e.connect(self.config.get('plc_ip_address',"192.168.0.142"),int(self.config.get('plc_mcprotocol_port',1400)))
            print("pymc3e.connect.ok")
        except: #연결실패
            print("pymc3e.connect.fail")
        return pymc3e
    
    def disconnect_pymc(self)->None:
        if self.is_connected():
            try:
                self.pymc3e.close()
            except AttributeError:# AttributeError: 'Type3E' object has no attribute '_sock'
                ... #temp #when debug

    def is_connected(self)->bool:
        if DEBUG or (self.pymc3e and self.pymc3e._is_connected):
            return True
        else:
            return False


    # [PLC 데이터 접근] -------------------------------------------------------------------------------------------
    @_ensure_connected
    def _get_plc_data_by_addrs(self,words=[])->dict:
        if DEBUG:
            from random import randint
            return [randint(1,10) for x in range(len(words))],[]
        return self.pymc3e.randomread(word_devices=words,dword_devices=[])
    # --------------------------
    def get_plc_data_by_dataset_name(self,dataset_name:str)->dict:
        dataset:dict = self.data_spec["plc_reg_addr"].get(dataset_name,{})
        revers_dataset = {v:k for k,v in dataset.items()}
        addrs = list(dataset.values())
        values = self._get_plc_data_by_addrs(addrs)[0] #temp

        return {revers_dataset[addrs[i]]:v for i,v in enumerate(values)}
    # --------------------------
    def get_plc_data_by_addr_names(self,dataset_name:str,addr_names:list)->dict:
        dataset:dict = {k:v for k,v in self.data_spec["plc_reg_addr"].get(dataset_name,{}).items() if k in addr_names}
        revers_dataset = {v:k for k,v in dataset.items()}
        addrs = list(dataset.values())
        values = self._get_plc_data_by_addrs(addrs)
        return {revers_dataset[addrs[i]]:v for i,v in enumerate(values)}
    # -------------------------------------------------------------------------------------------
    def get_plc_str_data_by_start_addr(self,start_addr,size:int=9)->str:
        if DEBUG:
            str_raw_data = [13401, 21300, 8224, 8224, 8224, 8224, 8224, 8224, 8224]
        else:
            str_raw_data = self.pymc3e.batchread_wordunits(headdevice=start_addr, readsize=size)

        result = ''
        for raw in str_raw_data:
            raw_hex = int(hex(raw), 16)
            result = result+ chr(raw_hex & 0xFF) + chr((raw_hex >> 8) & 0xFF) 
        return result

# ===========================================================================================
if __name__ == "__main__":
    m = Model()
    a = m._get_plc_data_by_addrs(["D348"])
    print(a)
    print(m.get_plc_data_by_dataset_name("graph"))
    a = m.get_plc_str_data_by_start_addr("")
    print(a)
    # print(m.get_plc_data_by_addr_names("mould",["complete_l1"]))
