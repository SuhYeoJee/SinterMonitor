if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from src.model import Model
from src.view import View    
from src.sinterdata import SinterData
from src.module.pyqt_imports import *
from src.module.exceptions import *
# ===========================================================================================

class Worker(QThread):
    data_generated = pyqtSignal()

    def __init__(self,time:int=5000):
        super().__init__()
        self.running = True
        self.time = time

    def run(self):
        while self.running:
            self.data_generated.emit()  # 5초마다 메인스레드 함수 호출
            self.msleep(self.time) #temp

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
        self.connect_view_func()
        self.check_connect_and_start_waiting()
        
    def connect_view_func(self):
        self.view.widgets['b1'].clicked.connect(self.start_monitoring)
        self.view.widgets['b2'].clicked.connect(self.stop_monitoring)
        self.view.menus['load_action'].triggered.connect(self.load_data)
        self.view.menus['close_action'].triggered.connect(self.close_data)
        self.view.menus['connect_action'].triggered.connect(self.connect_plc)
        self.view.menus['disconnect_action'].triggered.connect(self.disconnect_plc)

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
        if not self.observer.isRunning():
            self.observer = Worker(1000)  # observer가 주기적으로 check_start_signal 호출
            self.observer.data_generated.connect(self.check_start_signal)  
            self.observer.start()
    
    @pyqtSlot()
    def check_start_signal(self)->None: #every 1 sec
        [start] = self.model.get_plc_data_by_addr_names('common',['start'])
        def is_started()->bool:
            return True if start else False
        
        if is_started():
          self.stop_waiting_start_signal()
          self.start_monitoring()

    @pyqtSlot()
    def stop_waiting_start_signal(self):
        self.observer.stop()  # observer 스레드 종료

    def connect_plc(self):
        if not self.model.is_connected():
            self.model._connect_pymc() #연결
            self.check_connect_and_start_waiting() #시작신호 대기

    def disconnect_plc(self):
        self.stop_monitoring()
        self.model.disconnect_pymc() #연결 해제
        if not self.model.is_connected():
            self.view.show_disconnect_success_box()
    
    # [monitoring] ===========================================================================================
    @pyqtSlot()
    def update_and_save(self)->None: #every 1 sec
        def is_mould_changed()->bool:
            flag = common_data["mould_update"] is self.old_mould_update
            self.old_mould_update = common_data["mould_update"]
            return flag
        
        def is_stoped()->bool:
            return False if common_data["start"] else True

        print('update_and_save')
        common_data = self._get_plc_data_and_update_sint_data("common")
        graph_data = self._get_plc_data_and_update_sint_data("graph")
        if is_mould_changed():
            mould_top_data = self._get_plc_data_and_update_sint_data("mould_top")
            mould_bottom_data = self._get_plc_data_and_update_sint_data("mould_bottom")
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
        self.view.widgets["graph_scene"].clear()
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
        self.worker.stop()  # Worker 스레드 종료
        if self.sint_data:
            self.sint_data.save_data_to_excel()
        self.start_waiting_start_signal() # 시작신호 대기

    # [set data view] ===========================================================================================
    def set_view(self):
        if not self.sint_data:return
        self.view.set_value_by_label_and_text("graph_table",self.sint_data.data['graph'][-1])
        self.view.set_value_by_label_and_text("program_table",self.sint_data.data['program'][-1])
        if len(self.sint_data.data['mould_top']):
            self.view.set_value_by_label_and_text("mould_top_table",self.sint_data.data['mould_top'][-1])
        if len(self.sint_data.data['mould_bottom']):
            self.view.set_value_by_label_and_text("mould_bottom_table",self.sint_data.data['mould_bottom'][-1])
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