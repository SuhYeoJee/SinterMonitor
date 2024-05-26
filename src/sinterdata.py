if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from datetime import datetime
import pandas as pd
from os import path, makedirs
# ===========================================================================================
class SinterData:
    def __init__(self,file_name:str=None):
        if file_name: #load data
            self.file_name = file_name
            self.read_data_from_excel(file_name)
            self.is_new:bool = False
        else: # new SinterData
            self.file_name = datetime.now().strftime("./result/%Y-%m-%d_%H-%M-%S.xlsx")
            self.data = {
        "common": [{
            "start":"",
            "mould_update":"",
            "message":"",
            "work_time":"",
            "total_alarm":""
        }],
        "graph":[{
            "prg_no":"",
            "step":"",
            "current":"",
            "real_current":"",
            "press":"",
            "real_press":"",
            "temp":"",
            "real_temp":"",
            "time":"",
            "real_time":"",
            "total_time":"",
            "elec_distance":"",
            "date":''
        }],
        "program":[{
            "prg_no":"",
            "use_step":"",
            "prg_name":"",
            "step1_current":"",
            "step1_press":"",
            "step1_temp":"",
            "step1_time":"",
            "step2_current":"",
            "step2_press":"",
            "step2_temp":"",
            "step2_time":"",
            "step3_current":"",
            "step3_press":"",
            "step3_temp":"",
            "step3_time":"",
            "step4_current":"",
            "step4_press":"",
            "step4_temp":"",
            "step4_time":"",
            "step5_current":"",
            "step5_press":"",
            "step5_temp":"",
            "step5_time":"",
            "step6_current":"",
            "step6_press":"",
            "step6_temp":"",
            "step6_time":"",
            "step7_current":"",
            "step7_press":"",
            "step7_temp":"",
            "step7_time":"",
            "step8_current":"",
            "step8_press":"",
            "step8_temp":"",
            "step8_time":"",
            "step9_current":"",
            "step9_press":"",
            "step9_temp":"",
            "step9_time":"",
            "step10_current":"",
            "step10_press":"",
            "step10_temp":"",
            "step10_time":"",                              
            "step11_press":"",
            "step11_time":"",      
            "step12_press":"",
            "step12_temp":"",
            "step12_time":"",
            "sint_dim":"",
            "min_current":""
        }],
        "mould_top":[{
            "magazine_l":"",
            "start_l1":"",
            "start_l2":"",
            "finish_l1":"",
            "finish_l2":"",
            "magazine_r":"",
            "start_r1":"",
            "start_r2":"",
            "finish_r1":"",
            "finish_r2":"",      
            "sint_magazine_l":"",
            "sint_magazine_r":"",
            "work_prg_no":"",
            "work_count":""
        }],
        "mould_bottom":[{
            "turn_l1":"",
            "height_l1":"",
            "turn_r1":"",
            "height_r1":"",
            "prg_no1":"",
            "turn_l2":"",
            "height_l2":"",
            "turn_r2":"",
            "height_r2":"",
            "prg_no2":"",
            "turn_l3":"",
            "height_l3":"",
            "turn_r3":"",
            "height_r3":"",
            "prg_no3":"",
            "turn_l4":"",
            "height_l4":"",
            "turn_r4":"",
            "height_r4":"",
            "prg_no4":"",
            "turn_l5":"",
            "height_l5":"",
            "turn_r5":"",
            "height_r5":"",
            "prg_no5":"",
            "turn_l6":"",
            "height_l6":"",
            "turn_r6":"",
            "height_r6":"",
            "prg_no6":""
        }],
        "alarm": [{
                    "date":"",
                    "state":"",
                    "info":"",
                }],        
        }
            self.is_new:bool = True
            # self.save_data_to_excel() #make new file
    # -------------------------------------------------------------------------------------------
    def update_data(self,sheet_name:str,data:dict)->None:
        update_target = self.data.get(sheet_name,False)
        if not update_target:
            self.data[sheet_name]=[]
        if sheet_name == "graph":
            e_d = data["elec_distance"]
            e_d = e_d / 100
            data["elec_distance"] = e_d
            
        new_value = {k:v for k,v in self.data[sheet_name][-1].items()}
        new_value.update(data)
        update_target.append(new_value)
    # --------------------------
    def save_data_to_excel(self):
        if not path.exists('result'): makedirs('result')
        with pd.ExcelWriter(self.file_name) as writer:
            for sheet_name, sheet_data in self.data.items():
                df = pd.DataFrame(sheet_data[1:])
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    # --------------------------
    def read_data_from_excel(self,file_name):
        if not path.exists(file_name):
            print(f"no file: {file_name}")
            return
        else:
            self.file_name = file_name

        excel_data = {}
        try:
            xls = pd.ExcelFile(file_name)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_name, sheet_name=sheet_name)
                excel_data[sheet_name] = df.to_dict(orient='records')
        except Exception as e:
            print("file read error:", str(e))

        self.data = excel_data
        return excel_data
    