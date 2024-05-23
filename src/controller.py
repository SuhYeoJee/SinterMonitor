if __debug__:
    import sys
    sys.path.append(r"C:\Users\USER\Desktop\SinterMonitor")
# -------------------------------------------------------------------------------------------
from datetime import datetime
import pandas as pd
from threading import Timer
from os import path, makedirs
# --------------------------
from src.model import Model
from src.view import View    
from src.module.pyqt_imports import *
from src.module.exceptions import *
# ===========================================================================================

class SinterData:
    def __init__(self):
        self.filename = datetime.now().strftime("./result/%Y-%m-%d_%H-%M-%S.xlsx")
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
        # self.read_data_from_excel("./result/2024-05-22_23-50-17.xlsx")
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
        with pd.ExcelWriter(self.filename) as writer:
            for sheet_name, sheet_data in self.data.items():
                df = pd.DataFrame(sheet_data[1:])
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    # --------------------------
    def read_data_from_excel(self,file_name:str):
        if not path.exists(file_name):
            print(f"no file: {file_name}")
            return

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
    
# ===========================================================================================
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.sint_data:SinterData = None
        self.timer:Timer = None

        self.view.widgets['b1'].clicked.connect(self.start_monitoring)
        self.view.widgets['b2'].clicked.connect(self.stop_monitoring)
        self.view.widgets['b3'].clicked.connect(self.load_data)


    # [update] ===========================================================================================
    def update_and_save(self)->None: #every 1 sec
        print('update_and_save')
        common_data = self.get_plc_data_and_update_sint_data("common")
        graph_data = self.get_plc_data_and_update_sint_data("graph")
        if common_data["mould_update"] == True:
            mould_top_data = self.get_plc_data_and_update_sint_data("mould_top")
            mould_bottom_data = self.get_plc_data_and_update_sint_data("mould_bottom")
        # self.view.update_graph(graph_data)
        self.sint_data.save_data_to_excel()
        self.set_view()
        self.timer = Timer(1,self.update_and_save)
        self.timer.start()
    
    def get_plc_data_and_update_sint_data(self,dataset_name:str)->dict:
        data = self.model.get_plc_data_by_dataset_name(dataset_name)     
        self.sint_data.update_data(dataset_name,data)
        return data

    def start_monitoring(self)->None:
        self.view.widgets["graph_scene"].clear()
        self.sint_data = SinterData()
        program_data = self.get_plc_data_and_update_sint_data("program")
        mould_top_data = self.get_plc_data_and_update_sint_data("mould_top")
        mould_bottom_data = self.get_plc_data_and_update_sint_data("mould_bottom")          
        self.update_and_save() #set timer every 1 sec

    def stop_monitoring(self)->None:
        if self.sint_data:
            self.sint_data.save_data_to_excel()
        self.sint_data = None
        if self.timer:
            self.timer.cancel()
        self.timer = None
    # [set data view] ===========================================================================================
    def set_view(self):
        if not self.sint_data:return
        self.view.set_value_by_label_and_text("graph_table",self.sint_data.data['graph'][-1])
        self.view.set_value_by_label_and_text("program_table",self.sint_data.data['program'][-1])
        if len(self.sint_data.data['mould_top']):
            self.view.set_value_by_label_and_text("mould_top_table",self.sint_data.data['mould_top'][-1])
        if len(self.sint_data.data['mould_bottom']):
            self.view.set_value_by_label_and_text("mould_bottom_table",self.sint_data.data['mould_bottom'][-1])
        self.set_graph()

    def set_graph(self):
        graph_data = {
            'current':[],
            'real_current':[],
            'press':[],
            'real_press':[],
            'temp':[],
            'real_temp':[]
        }
        for x in self.sint_data.data['graph']:
            for k in graph_data.keys():
                if x[k] != '':
                    graph_data[k].append(x[k])
        self.view.set_graph(graph_data)

    def load_data(self):
        if self.sint_data and self.timer:
            self.stop_monitoring()
        self.sint_data = SinterData()
        file_name = self.view.get_load_file_name()
        self.sint_data.read_data_from_excel(file_name)
        self.set_view()
# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()


if __name__ == "__main__":
    main()