if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from src.model import Model
from src.view import View    
from src.sinterdata import SinterData
from src.module.pyqt_imports import *
from src.module.exceptions import *
import pyqtgraph as pg
# ===========================================================================================

class Worker(QThread):
    data_generated = pyqtSignal()

    def __init__(self,time:int=500): #temp -> 5000
        super().__init__()
        self.running = True
        self.time = time

    def run(self):
        while self.running:
            self.data_generated.emit() #self.time 주기로 함수 호출
            self.msleep(self.time)

    def stop(self):
        self.running = False
# ===========================================================================================

class Controller(QObject):
    def __init__(self):
        super().__init__()
        self.model:Model = Model()
        self.view:View = View()
        self.sint_data:SinterData = None
        self.worker = Worker()
        self.observer = Worker()
        self.old_mould_update = None
        self.line = None
        self.is_monitoring:bool = False
        self.connect_view_func()
        # self.check_connect_and_start_waiting()
        
    def connect_view_func(self):
        self.view.menus['load_action'].triggered.connect(self.load_data)
        self.view.menus['close_action'].triggered.connect(self.close_data)
        self.view.menus['connect_action'].triggered.connect(self.connect_plc)
        self.view.menus['disconnect_action'].triggered.connect(self.disconnect_plc)
        self.view.widgets['graph'].scene().sigMouseClicked.connect(self.mouse_clicked)
        self.view.widgets['b1'].clicked.connect(lambda:self.view.set_xrange(0,100))
        self.view.widgets['b2'].clicked.connect(lambda:self.view.set_xrange(0,10))

    def mouse_clicked(self, event):
        pos = event.pos()
        view = self.view.widgets['graph'].plotItem.vb

        pos_data = view.mapSceneToView(pos)
        x_val = int(round(pos_data.x()))
        # -------------------------------------------------------------------------------------------
        if self.line:
            self.view.widgets['graph'].removeItem(self.line)
        self.line = pg.InfiniteLine(pos=x_val, pen='black', angle=90, movable=False)
        self.view.widgets['graph'].addItem(self.line)

        def get_table_data_by_index(idx,dataset_name)->dict:
            table_data = {k:'' for k in self.model.data_spec["plc_reg_addr"][dataset_name].keys()}
            if idx < 0: 
                return table_data        
            try:
                x = self.sint_data.data[dataset_name][idx]
                for k in self.model.data_spec["plc_reg_addr"][dataset_name]:
                    table_data[k] = x[k]
            except IndexError: ...
            except AttributeError: ...
            finally:
                return table_data
        
        clicked_pos_datas = get_table_data_by_index(x_val,'graph')
        self.view.set_value_by_label_and_text("graph_table",clicked_pos_datas)
        clicked_pos_datas = get_table_data_by_index(x_val,'mould_top')
        self.view.set_value_by_label_and_text("mould_top_table",clicked_pos_datas)
        clicked_pos_datas = get_table_data_by_index(x_val,'mould_bottom')
        self.view.set_value_by_label_and_text("mould_bottom_table",clicked_pos_datas)

    # [waiting] ===========================================================================================
    def check_connect_and_start_waiting(self):
        try:
            if self.model.is_connected():
                self.view.show_connect_success_box()
                self.start_waiting_start_signal()
            else: raise
        except:
            self.view.show_connect_failure_box()

    @pyqtSlot()
    def start_waiting_start_signal(self):
        self.view.setWindowTitle("waiting start signal")
        if not self.observer.isRunning():
            self.observer = Worker(1000)  # observer가 주기적으로 check_start_signal 호출
            self.observer.data_generated.connect(self.check_start_signal)  
            self.observer.start()
    
    @pyqtSlot()
    def check_start_signal(self)->None: #every 1 sec
        self.view.setWindowTitle("check start signal")
        if self.is_monitoring: 
            return
        start = self.model.get_plc_data_by_addr_names('common',['start'])
        def is_started()->bool:
            return True if start['start'] % 15 == 0 else False
        
        if is_started():
          self.stop_waiting_start_signal()
          self.start_monitoring()
          self.is_monitoring = True

    @pyqtSlot()
    def stop_waiting_start_signal(self):
        self.view.setWindowTitle("stop waiting start signal")
        self.observer.stop()  # observer 스레드 종료

    def connect_plc(self):
        if not self.model.is_connected():
            self.model._connect_pymc() #연결
        self.check_connect_and_start_waiting() #시작신호 대기

    def disconnect_plc(self):
        self.stop_monitoring()
        self.stop_waiting_start_signal()
        self.model.disconnect_pymc() #연결 해제
        if not self.model.is_connected():
            self.view.show_disconnect_success_box()
    
    # [monitoring] ===========================================================================================
    @pyqtSlot()
    def update_and_save(self)->None: #every 1 sec
        self.view.setWindowTitle("monitoring")
        def is_mould_changed()->bool:
            # flag = common_data["mould_update"] ! self.old_mould_update
            self.old_mould_update = common_data["mould_update"]
            return self.old_mould_update % 3 == 0
        
        def is_stoped()->bool:
            print(int(common_data["start"])%15)
            return False if int(common_data["start"])%15!=0 else True

        common_data = self._get_plc_data_and_update_sint_data("common")
        graph_data = self._get_plc_data_and_update_sint_data("graph")
        if is_mould_changed():
            mould_top_data = self._get_plc_data_and_update_sint_data("mould_top")
            mould_bottom_data = self._get_plc_data_and_update_sint_data("mould_bottom")
        else:
            self.sint_data.update_data("mould_top",self.sint_data.data['mould_top'][-1])
            self.sint_data.update_data("mould_bottom",self.sint_data.data['mould_bottom'][-1])
            
        self.sint_data.save_data_to_excel()
        self.set_view()
        if is_stoped():
            self.stop_monitoring()        
        
    def _get_plc_data_and_update_sint_data(self,dataset_name:str)->dict:
        data = self.model.get_plc_data_by_dataset_name(dataset_name)     
        self.sint_data.update_data(dataset_name,data)
        return data

    @pyqtSlot()
    def start_monitoring(self)->None:
        self.view.setWindowTitle("start monitoring")
        # self.view.widgets["graph_scene"].clear()
        # temp
        self.sint_data = SinterData()
        program_data = self._get_plc_data_and_update_sint_data("program")
        mould_top_data = self._get_plc_data_and_update_sint_data("mould_top")
        mould_bottom_data = self._get_plc_data_and_update_sint_data("mould_bottom")          
        if not self.worker.isRunning():
            self.worker = Worker()  # Worker가 주기적으로 update_and_save 호출
            self.worker.data_generated.connect(self.update_and_save)  
            self.worker.start()

    @pyqtSlot()
    def stop_monitoring(self)->None:
        self.view.setWindowTitle("stop monitoring")
        if self.is_monitoring:
            self.worker.stop()  # Worker 스레드 종료
            if self.sint_data:
                self.sint_data.save_data_to_excel()
            self.is_monitoring = False
            self.start_waiting_start_signal() # 시작신호 대기

    # [set data view] ===========================================================================================
    def set_view(self):
        if not self.sint_data:return
        def set_value_if_exist(dataset_name):
            try:
                self.view.set_value_by_label_and_text(f"{dataset_name}_table",self.sint_data.data[dataset_name][-1])
            except:
                ...
        set_value_if_exist('graph')
        set_value_if_exist('program')
        if len(self.sint_data.data['mould_top']):
            set_value_if_exist('mould_top')
        if len(self.sint_data.data['mould_bottom']):
            set_value_if_exist('mould_bottom')
        self._set_graph()

    def _set_graph(self):
        graph_data = {
            'current':[],'real_current':[],
            'press':[],'real_press':[],
            'temp':[],'real_temp':[]
        }
        for x in self.sint_data.data['graph']:
            for k in graph_data.keys():
                if x[k] != '':
                    graph_data[k].append(x[k])
        self.view.set_graph(graph_data)

    def load_data(self):
        if self.sint_data and self.sint_data.is_new:
            self.stop_monitoring()
        file_name = self.view.open_file_dialog()
        self.sint_data = SinterData(file_name)
        self.set_view()

    def close_data(self):
        if self.sint_data and not self.sint_data.is_new:
            self.sint_data = None
            # 화면 초기화

# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()


if __name__ == "__main__":
    main()