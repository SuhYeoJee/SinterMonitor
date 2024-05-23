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
            "stop":"",
            "mould_update":"",
            "message":"",
            "work_time":"",
            "now_date":""
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
            "total_time":""
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
            "magazine_l":"D5030",
            "start_l1":"D5520",
            "start_l2":"D80",
            "finish_l1":"D5522",
            "finish_l2":"D82",
            "magazine_r":"D5028",
            "start_r1":"D5521",
            "start_r2":"D81",
            "finish_r1":"D5524",
            "finish_r2":"D83",      
            "sint_magazine_l":"D86",
            "sint_magazine_r":"D87",
            "work_prg_no":"D5578",
            "work_count":"D5080"
        }],
        "mould_bottom":[{
            "turn_l1":"D5530",
            "height_l1":"D5532",
            "turn_r1":"D5534",
            "height_r1":"D5536",
            "prg_no1":"D5570",
            "turn_l2":"D5540",
            "height_l2":"D5542",
            "turn_r2":"D5544",
            "height_r2":"D5546",
            "prg_no2":"D5572",
            "turn_l3":"D5550",
            "height_l3":"D5552",
            "turn_r3":"D5554",
            "height_r3":"D5556",
            "prg_no3":"D5574",
            "turn_l4":"D5560",
            "height_l4":"D5562",
            "turn_r4":"D5564",
            "height_r4":"D5566",
            "prg_no4":"D5576",
            "turn_l5":"D5580",
            "height_l5":"D5582",
            "turn_r5":"D5584",
            "height_r5":"D5586",
            "prg_no5":"D5568",
            "turn_l6":"D5590",
            "height_l6":"D5592",
            "turn_r6":"D5594",
            "height_r6":"D5596",
            "prg_no6":"D5569"
        }]
        }
            self.is_new:bool = True
            self.save_data_to_excel() #make new file
    # -------------------------------------------------------------------------------------------
    def update_data(self,sheet_name:str,data:dict)->None:
        update_target = self.data.get(sheet_name,False)
        if not update_target:
            self.data[sheet_name]=[]
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
    