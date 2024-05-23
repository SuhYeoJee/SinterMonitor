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

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            self.data_generated.emit()  # 5초마다 메인스레드 함수 호출
            self.msleep(500) #temp

    def stop(self):
        self.running = False
# ===========================================================================================

class Controller(QObject):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.view = View()
        self.sint_data:SinterData = None
        self.worker = Worker()
        self.old_mould_update = None
        self.view.widgets['b1'].clicked.connect(self.start_monitoring)
        self.view.widgets['b2'].clicked.connect(self.stop_monitoring)
        # self.view.widgets['b1'].clicked.connect(self.view.show_connect_success_box)
        # self.view.widgets['b2'].clicked.connect(self.view.show_connect_failure_box)
        # self.view.widgets['b3'].clicked.connect(self.start_work)
        self.view.menus['load_action'].triggered.connect(self.load_data)

    # [update] ===========================================================================================
    @pyqtSlot()
    def update_and_save(self)->None: #every 1 sec
        def is_mould_changed():
            flag = common_data["mould_update"] is self.old_mould_update
            self.old_mould_update = common_data["mould_update"]
            return flag

        print('update_and_save')
        common_data = self._get_plc_data_and_update_sint_data("common")
        graph_data = self._get_plc_data_and_update_sint_data("graph")
        if is_mould_changed() == True:
            mould_top_data = self._get_plc_data_and_update_sint_data("mould_top")
            mould_bottom_data = self._get_plc_data_and_update_sint_data("mould_bottom")
        self.sint_data.save_data_to_excel()
        self.set_view()

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
        self.sint_data = None
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
        if self.sint_data:
            self.stop_monitoring()
        file_name = self.view.open_file_dialog()
        self.sint_data = SinterData(file_name)
        self.set_view()
# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()


if __name__ == "__main__":
    main()