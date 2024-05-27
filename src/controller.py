if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from datetime import datetime
from src.model import Model
from src.view import View    
from src.sinterdata import SinterData
from src.module.pyqt_imports import *
from src.module.exceptions import *
import pyqtgraph as pg
# ===========================================================================================

class Worker(QThread):
    data_generated = pyqtSignal()

    def __init__(self,time:int=5000): #temp -> 5000
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
        self.sint_data:SinterData = SinterData()
        self.timer = Worker()
        self.worker = Worker()
        self.observer = Worker()
        self.alarmer = Worker()
        self.line = None
        self.is_monitoring:bool = False
        self.recent_alarms = []
        self.connect_view_func()
        self.set_config_values(True,'viewer','')
        # self.check_connect_and_start_waiting()

    def update_and_show_alarms(self):
        # 세부 알람 코드 가져오기
        now_alarms = self.model.get_alarms()
        # alarms에 시간과 매핑
        self.recent_alarms
        # alarms 의 변동 확인
        new_alarms = list(set(now_alarms) - set(self.recent_alarms))
        deleted_alarms = list(set(self.recent_alarms) - set(now_alarms))        
        # --------------------------
        for x in new_alarms:
            alarm_str = self.model.data_spec["alarm"].get(x,'unknown alarm')
            date_str = datetime.now().strftime("%H:%M:%S")
            alarm_info = {"date":date_str,"state":"on","info":alarm_str}
            self.sint_data.data['alarm'].append(alarm_info)
        for x in deleted_alarms:
            alarm_str = self.model.data_spec["alarm"].get(x,'unknown alarm')
            date_str = datetime.now().strftime("%H:%M:%S")
            alarm_info = {"date":date_str,"state":"off","info":alarm_str}
            self.sint_data.data['alarm'].append(alarm_info)
        # --------------------------
        self.view.widgets['alarm_table'].init_and_fill_data_sequence(self.sint_data.data['alarm'][1::-1],False)
        # table_show
        # --------------------------
        self.recent_alarms = new_alarms #최신 알람상황 갱신

    def connect_view_func(self):
        self.view.menus['load_action'].triggered.connect(self.load_data)
        self.view.menus['close_action'].triggered.connect(self.close_data)
        self.view.menus['connect_action'].triggered.connect(self.connect_plc)
        self.view.menus['disconnect_action'].triggered.connect(self.disconnect_plc)
        self.view.widgets['graph'].scene().sigMouseClicked.connect(self.mouse_clicked)
        self.view.widgets['b1'].clicked.connect(lambda:self.view.set_xrange('all')) # 1당5초, 전체뷰
        self.view.widgets['b2'].clicked.connect(lambda:self.view.set_xrange(60))  # 5분뷰? 10분에 120
        self.view.widgets['b3'].clicked.connect(lambda:self.view.set_xrange(120))  # 10분뷰? 10분에 120

    def set_config_values(self,connect=False, mode='',state=''):
        # self.set_config_values('mode','state')
        if connect:
            adapter_name, ip_addr = self.model.find_adapter_name_and_ip()
            adapter_name = str(adapter_name) if adapter_name else 'adapter not found'
            ip_addr = str(ip_addr) if ip_addr else ''
            connection = 'Connect' if self.model.is_connected() else 'Disconnect'
            self.view.widgets['config_table'].fill_datas_position_label({'ip_change':f'{adapter_name}\n{ip_addr}','connection': connection})
        self.view.widgets['config_table'].fill_datas_position_label({'mode': mode,'state': state})

    def mouse_clicked(self, event):
        pos = event.pos()
        pos.setX(pos.x() + 130)
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
            if 'graph' in dataset_name:
                table_data['date'] = ''
            if idx < 0: 
                return table_data        
            try:
                x = self.sint_data.data[dataset_name][idx]
                for k in x.keys():
                    table_data[k] = x[k]
            except IndexError: ...
            except AttributeError: ...
            finally:
                return table_data
        clicked_pos_datas = get_table_data_by_index(x_val,'common')
        self.view.set_value_by_label_and_text("common",clicked_pos_datas)
        clicked_pos_datas = get_table_data_by_index(x_val,'graph')
        self.view.set_value_by_label_and_text("graph_table",clicked_pos_datas)
        clicked_pos_datas = get_table_data_by_index(x_val,'mould_top')
        self.view.set_value_by_label_and_text("mould_top_table",clicked_pos_datas)
        clicked_pos_datas = get_table_data_by_index(x_val,'mould_bottom')
        self.view.set_value_by_label_and_text("mould_bottom_table",clicked_pos_datas)

    # [waiting] ===========================================================================================
    def check_connect_and_start_waiting(self):
        print('&check_connect_and_start_waiting')
        try:
            if self.model.is_connected():
                # self.view.show_connect_success_box()
                self.start_waiting_start_signal()
            else: raise
        except:
            self.view.show_connect_failure_box()

    @pyqtSlot()
    def start_waiting_start_signal(self):
        print('&start_waiting_start_signal')
        self.set_config_values(True,'monitoring','waiting start signal')
        self.view.setWindowTitle("waiting start signal")
        if not self.observer.isRunning():
            self.observer = Worker(1000)  # observer가 주기적으로 check_start_signal 호출
            self.observer.data_generated.connect(self.check_start_signal)  
            self.observer.start()
    
    def is_running(self)->bool:
        print('&is_running')
        # return True # debug
        start_signal = self.model.get_plc_bool_by_addr_name("start")
        print('running',start_signal)
        return start_signal

    @pyqtSlot()
    def check_start_signal(self)->None: #every 1 sec
        print('&check_start_signal')
        self.set_config_values(False,'monitoring','stop waiting start signal')
        self.view.setWindowTitle("check start signal")
        if self.is_monitoring: 
            return

        if self.is_running():
          self.stop_waiting_start_signal()
          self.start_monitoring()
          self.is_monitoring = True

    @pyqtSlot()
    def stop_waiting_start_signal(self):
        print('&stop_waiting_start_signal')
        self.set_config_values(True,'monitoring','stop waiting start signal')
        self.view.setWindowTitle("stop waiting start signal")
        self.observer.stop()  # observer 스레드 종료
        self.observer.wait()  # observer 스레드 종료

    def connect_plc(self):
        print('&connect_plc')
        self.view.clear_view()
        if not self.model.is_connected():
            self.model._connect_pymc() #연결
        self.check_connect_and_start_waiting() #시작신호 대기

    def disconnect_plc(self):
        print('&disconnect_plc')
        self.stop_monitoring()
        self.stop_waiting_start_signal()
        self.model.disconnect_pymc() #연결 해제
        if not self.model.is_connected():
            self.view.show_disconnect_success_box()
            self.set_config_values(True,'view','')
    
    # [monitoring] ===========================================================================================
    @pyqtSlot()
    def update_and_save(self)->None: #every 5 sec
        print('&update_and_save')
        # self.set_config_values(False,'monitoring','monitoring')
        self.view.setWindowTitle("monitoring")
        def is_mould_changed()->bool:
            module_signal = self.model.get_plc_bool_by_addr_name("mould_update")
            print('module',module_signal)
            return module_signal
        def is_alarm_exist()->bool:
            alarm_signal = self.model.get_plc_bool_by_addr_name("total_alarm")
            print('alarm',alarm_signal)
            return alarm_signal

        common_data = self._get_plc_data_and_update_sint_data("common")
        graph_data = self._get_plc_data_and_update_sint_data("graph")
        program_data = self._get_plc_data_and_update_sint_data("program")
        if is_mould_changed():
            mould_top_data = self._get_plc_data_and_update_sint_data("mould_top")
            mould_bottom_data = self._get_plc_data_and_update_sint_data("mould_bottom")
        else:
            self.sint_data.update_data("mould_top",self.sint_data.data['mould_top'][-1])
            self.sint_data.update_data("mould_bottom",self.sint_data.data['mould_bottom'][-1])
        if is_alarm_exist():
            self.update_and_show_alarms()

        self.sint_data.save_data_to_excel()
        self.set_view()
        if not self.is_running():
            self.stop_monitoring()        
        
    def _get_plc_data_and_update_sint_data(self,dataset_name:str)->dict:
        print('&_get_plc_data_and_update_sint_data')
        data = self.model.get_plc_data_by_dataset_name(dataset_name)
        if 'program' in dataset_name and data.get('prg_name',None):
            prg_name_start_addr = self.model.data_spec['plc_reg_addr']['program']['prg_name']
            data['prg_name']  = self.model.get_plc_str_data_by_start_addr(prg_name_start_addr).strip().replace(' ','')
        # if 'graph' in dataset_name:
        data['date'] = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        self.sint_data.update_data(dataset_name,data)
        return data

    @pyqtSlot()
    def show_now(self):
        print('&show_now')
        current_datetime = QDateTime.currentDateTime()
        display_text = current_datetime.toString('yyyy-MM-dd hh:mm:ss')
        if self.is_monitoring:
            self.view.widgets['date'].setText(display_text)      

    @pyqtSlot()
    def start_monitoring(self)->None:
        print('&start_monitoring')
        self.set_config_values(False,'monitoring','start_monitoring')
        self.view.setWindowTitle("start monitoring")
        # self.view.widgets["graph_scene"].clear()
        # temp
        self.sint_data = SinterData()
        program_data = self._get_plc_data_and_update_sint_data("program")
        mould_top_data = self._get_plc_data_and_update_sint_data("mould_top")
        mould_bottom_data = self._get_plc_data_and_update_sint_data("mould_bottom")
        
        if not self.timer.isRunning():
            self.timer = Worker(1000)  # timer 주기적으로 show_now 호출
            self.timer.data_generated.connect(self.show_now)  
            self.timer.start()        
      
        if not self.worker.isRunning():
            self.worker = Worker()  # Worker가 주기적으로 update_and_save 호출
            self.worker.data_generated.connect(self.update_and_save)  
            self.worker.start()

    @pyqtSlot()
    def stop_monitoring(self)->None:
        print('&stop_monitoring')
        # self.set_config_values(False,'monitoring','stop_monitoring')
        self.view.setWindowTitle("stop monitoring")
        if self.is_monitoring:
            self.timer.stop()  # timer 스레드 종료
            self.worker.stop()  # Worker 스레드 종료
            self.timer.wait()  # timer 스레드 종료
            self.worker.wait()  # Worker 스레드 종료
            if self.sint_data:
                self.sint_data.save_data_to_excel()
            self.is_monitoring = False
            self.check_connect_and_start_waiting() # 시작신호 대기

    # [set data view] ===========================================================================================
    def set_view(self):
        print('&set_view')
        if not self.sint_data:return
        def set_value_if_exist(dataset_name):
            # try:
            self.view.set_value_by_label_and_text(f"{dataset_name}_table",self.sint_data.data[dataset_name][-1])
            # except:...
        set_value_if_exist('common')
        set_value_if_exist('graph')
        set_value_if_exist('program')
        if len(self.sint_data.data['mould_top']):
            set_value_if_exist('mould_top')
        if len(self.sint_data.data['mould_bottom']):
            set_value_if_exist('mould_bottom')
        
        if self.sint_data.data.get('alarm'):
            self.view.widgets['alarm_table'].init_and_fill_data_sequence(self.sint_data.data['alarm'],False) # show alarms
        self._set_graph()

    def _set_graph(self):
        print('&_set_graph')
        graph_data = {
            'current':[],
            # 'real_current':[], # 실제 전류값 비표시
            'press':[],'real_press':[],
            'temp':[],'real_temp':[],
            'elec_distance':[], 'date':[]
        }
        for x in self.sint_data.data['graph']:
            for k in graph_data.keys():
                if x[k] != '':
                    graph_data[k].append(x[k])

        self.view.set_graph(graph_data)

    def load_data(self):
        print('&load_data')
        if self.sint_data and self.sint_data.is_new:
            self.stop_monitoring()
        file_name = self.view.open_file_dialog()
        self.view.setWindowTitle(f"load data - {file_name}")
        self.set_config_values(False,'viewer',file_name)
        self.sint_data = SinterData(file_name)
        self.set_view()

    def close_data(self):
        print('&close_data')
        if self.sint_data and not self.sint_data.is_new:
            self.sint_data = None
        self.set_config_values(False,'viewer','')
        self.view.clear_view()

# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()


if __name__ == "__main__":
    main()