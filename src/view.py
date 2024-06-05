if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
import pyqtgraph as pg
import numpy as np
# --------------------------
from src.module.pyqt_imports import *
from src.module.window_builder import WindowBuilder
from src.module.table_plus_widget import TablePlusWidget
# ===========================================================================================
class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wb = WindowBuilder()
        self.widgets = {}
        self.layouts = {}
        self.dialogs = {}        
        self.menus = {}        
        self.table_spec = {}
        self.xrange_size:int = 60
        self.graph_size:int = 0
        # --------------------------
        screen = QDesktopWidget().screenGeometry() # 화면 크기 조정
        self.resize(int(screen.height() * 0.7 * 2.3), int(screen.height() * 0.7))
        self.setWindowTitle("Sinter Monitor")
        self.create_menu()
        # --------------------------
        self.layouts['main'] = self.get_main_layout()
        # --------------------------
        self.widgets['main'] = QWidget()
        self.widgets['main'].setLayout(self.layouts['main'])
        self.setCentralWidget(self.widgets['main'])

    def clear_view(self):
        self.widgets['graph'].clear()
        self.widgets['graph_table'].fill_form()
        self.widgets['program_table'].fill_form()
        self.widgets['mould_top_table'].fill_form()
        self.widgets['mould_bottom_table'].fill_form()

    # [menu] ===========================================================================================
    def create_menu(self):
        menubar = self.menuBar()
        # -------------------------------------------------------------------------------------------
        load_action = QAction('Load', self)
        self.menus["load_action"] = load_action
        close_action = QAction('Close', self)
        self.menus["close_action"] = close_action
        capture_action = QAction('Capture', self)
        self.menus["capture_action"] = capture_action        
        print_action = QAction('Print', self)
        self.menus["print_action"] = print_action
        # --------------------------
        file_menu = menubar.addMenu('File')
        file_menu.addAction(load_action)
        file_menu.addAction(capture_action)
        file_menu.addAction(print_action)
        file_menu.addAction(close_action)
        # -------------------------------------------------------------------------------------------
        connect_action = QAction('Connect', self)
        self.menus["connect_action"] = connect_action
        disconnect_action = QAction('Disconnect', self)
        self.menus["disconnect_action"] = disconnect_action
        # --------------------------
        connection_menu = menubar.addMenu('Connection')
        connection_menu.addAction(connect_action)
        connection_menu.addAction(disconnect_action)
    # -------------------------------------------------------------------------------------------
    def open_file_dialog(self)->str:
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "./result", "Excel Files (*.xlsx)", options=options)
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = ''
        return self.file_path

    # -------------------------------------------------------------------------------------------
    def get_top_layout(self)->QHBoxLayout:
        top_layout = QHBoxLayout()
        self.widgets['message'] = self.wb.get_label("")
        top_layout.addWidget(self.widgets['message'],4)
        top_layout.addStretch(1)
        top_layout.addLayout(self.wb.get_label_and_line_edit_layout("Work Time",self.widgets,"work_time"))
        top_layout.addWidget(self.wb.get_vline_widget())
        self.widgets['date'] = self.wb.get_line_edit_widget(300)
        top_layout.addWidget(self.widgets['date'],2)

        self.widgets['b1'] = self.wb.get_button("full")
        self.widgets['b2'] = self.wb.get_button("5mins")
        self.widgets['b3'] = self.wb.get_button("10mins")
        top_layout.addWidget(self.widgets['b1'])
        top_layout.addWidget(self.widgets['b2'])
        top_layout.addWidget(self.widgets['b3'])

        return top_layout
    # -------------------------------------------------------------------------------------------
    def get_graph_view_layout(self)->QVBoxLayout:
        self.table_spec['graph_form']={'init_size' : (3,7), 'slim_rows' : [],'slim_cols' : [],'text_items' : {
                (0,0):[(1,1),"PRG.NO", ['center']],
                (0,1):[(1,1),"STEP", ['center']],
                (0,2):[(1,1),"Current (%)", ['center']],
                (0,3):[(1,1),"Pressure (Kg/cm²)", ['center']],
                (0,4):[(1,1),"Temperature (°C)", ['center']],
                (0,5):[(1,1),"Time (sec)", ['center']],
                (0,6):[(1,1),"Total Time", ['center']],
                (1,0):[(2,1),"", ['center']],
                (1,1):[(2,1),"", ['center']],
        },}
        self.table_spec['graph_pos']={
            "prg_no":(1,0),
            "step":(1,1),
            "current":(1,2),
            "real_current":(2,2),
            "press":(1,3),
            "real_press":(2,3),
            "temp":(1,4),
            "real_temp":(2,4),
            "time":(1,5),
            "real_time":(2,5),
            "total_time":(1,6),
            "elec_distance":(2,6),
        }
        self.table_spec['graph_unit']={
            "current":'%',
            "real_current":'A',
            "press":'00kg',
            "real_press":'00kg',
            "temp":'°C',
            "real_temp":'°C',
            "time":'sec',
            "real_time":'sec',
            "total_time":'sec',
            "elec_distance":'mm',
        }        
        # --------------------------
        self.widgets['graph'] = pg.PlotWidget()
        self.widgets['graph'].showGrid(x=True, y=True)
        self.widgets['graph'].setBackground('w')
        self.widgets['graph'].getViewBox().setMouseEnabled(x=True, y=False)
        self.widgets['graph'].setYRange(-2000,60000, padding=0.03)
        self.widgets['graph'].getPlotItem().showAxis('right')
        # --------------------------
        right_axis = self.widgets['graph'].getPlotItem().getAxis('right')
        right_ticks = [(-2000, '  %,  mm'), (0, '  0,   60'), (6000, ' 12,  66'), (12000, ' 24,  72'), (18000, ' 36,  78'), (24000, ' 48,  84'), (30000, ' 60,  90'), \
                       (36000, ' 72,  96'), (42000, ' 84, 102'), (48000, ' 96, 108'), (54000, '108, 114'), (60000, '120, 120')]
        right_axis.setTicks([right_ticks])
        right_axis.setWidth(130)
        right_axis.setTextPen(pg.mkPen('k'))
        # --------------------------
        left_axis = self.widgets['graph'].getPlotItem().getAxis('left')
        left_ticks = [(-2000, 'Kg/cm²,   °C'), (0, '0,  300'), (6000, '6000,  400'), (12000, '12000,  500'), (18000, '18000,  600'), (24000, '24000,  700'), (30000, '30000,  800'), \
                      (36000, '36000,  900'), (42000, '42000, 1000'), (48000, '48000, 1100'), (54000, '54000, 1200'), (60000, '60000, 1300')]
        left_axis.setTicks([left_ticks])
        left_axis.setWidth(130)
        left_axis.setTextPen(pg.mkPen('k'))
        # --------------------------
        legend = self.widgets['graph'].addLegend(offset=(0,1)) # 범례
        # --------------------------
        self.widgets['graph_table'] = TablePlusWidget(form_data=self.table_spec['graph_form'], pos_data=self.table_spec['graph_pos'],unit_data=self.table_spec['graph_unit'])
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.widgets['graph'],8)
        graph_layout.addWidget(self.widgets['graph_table'],2)
        # --------------------------
        return self.wb.get_box_frame_layout(graph_layout)
    # -------------------------------------------------------------------------------------------
    def get_program_view_layout(self)->QVBoxLayout:
        program_top_layout = QHBoxLayout()
        program_top_layout.addLayout(self.wb.get_label_and_line_edit_layout("PRG.NO",self.widgets,'prg_no'))
        program_top_layout.addLayout(self.wb.get_label_and_line_edit_layout("STEP",self.widgets,'use_step'))
        program_top_layout.addLayout(self.wb.get_label_and_line_edit_layout("PRG.NAME",self.widgets,'prg_name'))
        # --------------------------
        self.table_spec['program_form']={'init_size' : (12,6), 'slim_rows' : [],'slim_cols' : [],
                    'text_items' : {
                        (0,0):[(1,1),"STEP", ['center']],
                        (0,1):[(1,1),"Current (%)", ['center']],
                        (0,2):[(1,1),"Press (Kg/cm²)", ['center']],
                        (0,3):[(1,1),"Temp' (°C)", ['center']],
                        (0,4):[(1,1),"Time (sec)", ['center']],
                        (0,5):[(1,1),"12", ['center']],
                        (1,0):[(1,1),"1", ['center']],
                        (1,1):[(1,1),"", ['center']],
                        (1,2):[(1,1),"", ['center']],
                        (1,3):[(1,1),"", ['center']],
                        (1,4):[(1,1),"", ['center']],
                        (1,5):[(1,1),"Cooling", ['center']],
                        (2,0):[(1,1),"2", ['center']],
                        (2,1):[(1,1),"", ['center']],
                        (2,2):[(1,1),"", ['center']],
                        (2,3):[(1,1),"", ['center']],
                        (2,4):[(1,1),"", ['center']],
                        (2,5):[(1,1),"Press Kg/cm²", ['center']],                        
                        (3,0):[(1,1),"3", ['center']],
                        (3,1):[(1,1),"", ['center']],
                        (3,2):[(1,1),"", ['center']],
                        (3,3):[(1,1),"", ['center']],
                        (3,4):[(1,1),"", ['center']],
                        (3,5):[(1,1),"", ['center']],
                        (4,0):[(1,1),"4", ['center']],
                        (4,1):[(1,1),"", ['center']],
                        (4,2):[(1,1),"", ['center']],
                        (4,3):[(1,1),"", ['center']],
                        (4,4):[(1,1),"", ['center']],
                        (4,5):[(1,1),"Cool Time sec", ['center']],      
                        (5,0):[(1,1),"5", ['center']],
                        (5,1):[(1,1),"", ['center']],
                        (5,2):[(1,1),"", ['center']],
                        (5,3):[(1,1),"", ['center']],
                        (5,4):[(1,1),"", ['center']],
                        (5,5):[(1,1),"", ['center']],          
                        (6,0):[(1,1),"6", ['center']],
                        (6,1):[(1,1),"", ['center']],
                        (6,2):[(1,1),"", ['center']],
                        (6,3):[(1,1),"", ['center']],
                        (6,4):[(1,1),"", ['center']],
                        (6,5):[(1,1),"END Temp' °C", ['center']],           
                        (7,0):[(1,1),"7", ['center']],
                        (7,1):[(1,1),"", ['center']],
                        (7,2):[(1,1),"", ['center']],
                        (7,3):[(1,1),"", ['center']],
                        (7,4):[(1,1),"", ['center']],
                        (7,5):[(1,1),"", ['center']],             
                        (8,0):[(1,1),"8", ['center']],
                        (8,1):[(1,1),"", ['center']],
                        (8,2):[(1,1),"", ['center']],
                        (8,3):[(1,1),"", ['center']],
                        (8,4):[(1,1),"", ['center']],
                        (8,5):[(1,1),"SINT DIM.mm", ['center']],           
                        (9,0):[(1,1),"9", ['center']],
                        (9,1):[(1,1),"", ['center']],
                        (9,2):[(1,1),"", ['center']],
                        (9,3):[(1,1),"", ['center']],
                        (9,4):[(1,1),"", ['center']],
                        (9,5):[(1,1),"", ['center']],                
                        (10,0):[(1,1),"10", ['center']],
                        (10,1):[(1,1),"", ['center']],
                        (10,2):[(1,1),"", ['center']],
                        (10,3):[(1,1),"", ['center']],
                        (10,4):[(1,1),"", ['center']],
                        (10,5):[(1,1),"MinCurrent%", ['center']],          
                        (11,0):[(1,1),"11", ['center']],
                        (11,1):[(1,1),"Holding", ['center']],
                        (11,2):[(1,1),"", ['center']],
                        (11,3):[(1,1),"", ['center']],
                        (11,4):[(1,1),"", ['center']],
                        (11,5):[(1,1),"", ['center']],                                                                                                                                                     
                    },}
        self.table_spec['program_pos']={
            "step1_current":(1,1),
            "step1_press":(1,2),
            "step1_temp":(1,3),
            "step1_time":(1,4),
            "step2_current":(2,1),
            "step2_press":(2,2),
            "step2_temp":(2,3),
            "step2_time":(2,4),
            "step3_current":(3,1),
            "step3_press":(3,2),
            "step3_temp":(3,3),
            "step3_time":(3,4),
            "step4_current":(4,1),
            "step4_press":(4,2),
            "step4_temp":(4,3),
            "step4_time":(4,4),
            "step5_current":(5,1),
            "step5_press":(5,2),
            "step5_temp":(5,3),
            "step5_time":(5,4),
            "step6_current":(6,1),
            "step6_press":(6,2),
            "step6_temp":(6,3),
            "step6_time":(6,4),
            "step7_current":(7,1),
            "step7_press":(7,2),
            "step7_temp":(7,3),
            "step7_time":(7,4),
            "step8_current":(8,1),
            "step8_press":(8,2),
            "step8_temp":(8,3),
            "step8_time":(8,4),
            "step9_current":(9,1),
            "step9_press":(9,2),
            "step9_temp":(9,3),
            "step9_time":(9,4),
            "step10_current":(10,1),
            "step10_press":(10,2),
            "step10_temp":(10,3),
            "step10_time":(10,4),
            "step11_press":(11,2),
            "step11_time":(11,4),
            "step12_press":(3,5),
            "step12_temp":(5,5),
            "step12_time":(7,5),
            "sint_dim":(9,5),
            "min_current":(11,5),
        }        
        self.table_spec['program_unit']={
            "step1_press":'00',
            "step2_press":'00',
            "step3_press":'00',
            "step4_press":'00',
            "step5_press":'00',
            "step6_press":'00',
            "step7_press":'00',
            "step8_press":'00',
            "step9_press":'00',
            "step10_press":'00',
            "step11_press":'00',
            "step12_press":'00',

        }            
        program_table = TablePlusWidget(form_data=self.table_spec['program_form'],pos_data=self.table_spec['program_pos'],unit_data=self.table_spec['program_unit'])
        self.widgets['program_table'] = program_table
        program_view_layout = QVBoxLayout()
        program_view_layout.addLayout(program_top_layout)
        program_view_layout.addWidget(program_table)
        return program_view_layout
    # -------------------------------------------------------------------------------------------
    def get_mould_view_layout(self)->QVBoxLayout:
        self.table_spec['mould_top_form'] ={'init_size' : (5,6), 'slim_rows' : [],'slim_cols' : [],
                    'text_items' : {
                        (0,0):[(1,1),"Magazine", ['center']],
                        (1,0):[(1,1),"Start", ['center']],
                        (3,0):[(1,1),"Finish", ['center']],
                        (0,3):[(2,1),"sintering Magazine", ['center']],
                        (0,4):[(2,1),"", ['center']],
                        (0,5):[(2,1),"", ['center']],
                        (2,3):[(1,2),"work prg.no", ['center']],
                        (3,3):[(1,2),"work set count", ['center']], #영문명 확인필 temp
                        (4,3):[(1,2),"work count", ['center']],
                    }}
        self.table_spec['mould_top_pos']={
            "magazine_l":(0,1),
            "start_l1":(1,1),
            "start_l2":(2,1),
            "finish_l1":(3,1),
            "finish_l2":(4,1),
            "magazine_r":(0,2),
            "start_r1":(1,2),
            "start_r2":(2,2),
            "finish_r1":(3,2),
            "finish_r2":(4,2),
            "sint_magazine_l":(0,4),
            "sint_magazine_r":(0,5),
            "work_prg_no":(2,5),
            "work_set_count":(3,5),                            
            "work_count":(4,5),                            
        }
        mould_top_table = TablePlusWidget(form_data=self.table_spec['mould_top_form'],pos_data=self.table_spec['mould_top_pos'])
        self.widgets['mould_top_table'] = mould_top_table
        # --------------------------
        self.table_spec['mould_bottom_form']={'init_size' : (7,6), 'slim_rows' : [],'slim_cols' : [],
                    'text_items' : {
                        (0,1):[(1,1),"Turn", ['center']],
                        (0,2):[(1,1),"Height", ['center']],
                        (0,3):[(1,1),"Turn", ['center']],
                        (0,4):[(1,1),"Height", ['center']],
                        (0,5):[(1,1),"prg.no", ['center']],
                        (1,0):[(1,1),"1", ['center']],
                        (2,0):[(1,1),"2", ['center']],
                        (3,0):[(1,1),"3", ['center']],
                        (4,0):[(1,1),"4", ['center']],
                        (5,0):[(1,1),"5", ['center']],
                        (6,0):[(1,1),"6", ['center']],
                    }}
        self.table_spec['mould_bottom_pos']={
            "turn_l1":(1,1),
            "height_l1":(1,2),
            "turn_r1":(1,3),
            "height_r1":(1,4),
            "prg_no1":(1,5),
            "turn_l2":(2,1),
            "height_l2":(2,2),
            "turn_r2":(2,3),
            "height_r2":(2,4),
            "prg_no2":(2,5),
            "turn_l3":(3,1),
            "height_l3":(3,2),
            "turn_r3":(3,3),
            "height_r3":(3,4),
            "prg_no3":(3,5),
            "turn_l4":(4,1),
            "height_l4":(4,2),
            "turn_r4":(4,3),
            "height_r4":(4,4),
            "prg_no4":(4,5),
            "turn_l5":(5,1),
            "height_l5":(5,2),
            "turn_r5":(5,3),
            "height_r5":(5,4),
            "prg_no5":(5,5),
            "turn_l6":(6,1),
            "height_l6":(6,2),
            "turn_r6":(6,3),
            "height_r6":(6,4),
            "prg_no6":(6,5),
        }
        mould_bottom_table = TablePlusWidget(form_data=self.table_spec['mould_bottom_form'],pos_data=self.table_spec['mould_bottom_pos'])
        self.widgets['mould_bottom_table'] = mould_bottom_table
        # --------------------------
        mould_view_layout = QVBoxLayout()
        mould_view_layout.addWidget(mould_top_table,5)
        mould_view_layout.addWidget(mould_bottom_table,6)
        return mould_view_layout
    # -------------------------------------------------------------------------------------------
    def get_main_layout(self)->QHBoxLayout:
        self.layouts['top_layout'] = self.get_top_layout()
        self.layouts['graph_view_layout'] = self.get_graph_view_layout()
        self.layouts['program_view_layout'] = self.get_program_view_layout()
        self.layouts['mould_view_layout'] = self.get_mould_view_layout()
        self.layouts['alarm_view_layout'] = self.get_alarm_view_layout()
        self.layouts['config_view_layout'] = self.get_config_view_layout()
        # --------------------------
        bottom_view_layout = QHBoxLayout()
        bottom_view_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['program_view_layout']),1)
        bottom_view_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['mould_view_layout']),1)
        # --------------------------
        side_view_layout = QVBoxLayout()
        side_view_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['alarm_view_layout']),4)
        side_view_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['config_view_layout']),2)
        side_view_layout.addStretch(1)
        # --------------------------
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['top_layout']))
        main_layout.addLayout(self.layouts['graph_view_layout'],6)
        main_layout.addLayout(bottom_view_layout,4)
        # --------------------------
        layout = QHBoxLayout()
        layout.addLayout(main_layout,8)
        layout.addLayout(side_view_layout,2)
        return layout
    # -------------------------------------------------------------------------------------------
    def get_alarm_view_layout(self)->QHBoxLayout:
        alarm_view_layout = QHBoxLayout()
        # --------------------------
        alarm_table = TablePlusWidget()
        self.widgets['alarm_table'] = alarm_table
        alarm_view_layout.addWidget(alarm_table)
        return alarm_view_layout

    def get_config_view_layout(self)->QHBoxLayout:
        config_view_layout = QHBoxLayout()
        self.table_spec['config_form'] ={'init_size' : (3,4), 'slim_rows' : [],'slim_cols' : [],
                    'text_items' : {
                        (0,0):[(1,1),"mode", ['center']],
                        (1,0):[(1,1),"ip change", ['center']],
                        (2,0):[(1,1),"connection", ['center']],
                        (3,0):[(1,1),"state", ['center']],
                        (0,1):[(1,3),"", ['center']],
                        (1,1):[(1,3),"", ['center']],
                        (2,1):[(1,3),"", ['center']],
                        (3,1):[(1,3),"", ['center']],
                    }}
        self.table_spec['config_pos']={
            "mode":(0,1),
            "ip_change":(1,1),
            "connection":(2,1),
            "state":(3,1),
        }
        config_table = TablePlusWidget(form_data=self.table_spec['config_form'],pos_data=self.table_spec['config_pos'])
        self.widgets['config_table'] = config_table
        config_view_layout.addWidget(config_table)
        return config_view_layout
    # -------------------------------------------------------------------------------------------
    def show_connect_success_box(self):
        msg = self.wb.get_message_box('info','Success','Connection successful')
        QTimer.singleShot(3000, msg.accept)
        msg.exec_()

    def show_connect_failure_box(self):
        msg = self.wb.get_message_box('critical','Error','Connection failed')
        msg.exec_()

    def show_disconnect_success_box(self):
        msg = self.wb.get_message_box('info','Success','Disconnection successful')
        QTimer.singleShot(3000, msg.accept)
        msg.exec_()

    # ===========================================================================================
    def set_value_by_label_and_text(self,table_name,datas:dict):
        #line_edit
        if 'common' in table_name:
            self.widgets['work_time'].setText(str(datas.get('work_time','')))
            return
        if 'graph' in table_name:
            self.widgets['date'].setText(str(datas.get('date','')))
        elif 'program' in table_name:
            self.widgets['prg_no'].setText(str(datas.get('prg_no','')))
            self.widgets['use_step'].setText(str(datas.get('use_step','')))
            self.widgets['prg_name'].setText(str(datas.get('prg_name','')))
        # --------------------------
        # table
        pos_and_text = {v:str(datas[k])+self.widgets[table_name].unit_data.get(k,'') for k,v in self.table_spec[table_name.replace('_table','_pos')].items() if k in datas.keys()}
        self.widgets[table_name].fill_datas_position(pos_and_text)


    def set_graph(self,graph_raw_data:dict):
        self.widgets['graph'].clear()
        # -------------------------------------------------------------------------------------------
        for line_name, line_data in graph_raw_data.items():
            if line_name == "current":
                color, data_min, data_max = (0, 255, 0),0,120
                # color, data_min, data_max = (150, 200, 150),0,120
            elif line_name == "real_current":
                color, data_min, data_max = (0, 255, 0),0,120
            elif line_name == "press":
                color, data_min, data_max = (150, 150, 200),0,60000
                line_data = [x*100 for x in line_data]
            elif line_name == "real_press":
                color, data_min, data_max = (0, 0, 255),0,60000
                line_data = [x*100 for x in line_data]
            elif line_name == "temp":
                color, data_min, data_max = (200, 150, 150),300,1300
            elif line_name == "real_temp":
                color, data_min, data_max = (255, 0, 0),300,1300
            elif line_name == "elec_distance":
                color, data_min, data_max = 'orange',60,120
            else:
                continue
            scaled_data = np.interp(line_data, (data_min,data_max), (0, 60000))
            self.widgets['graph'].plot(scaled_data, pen=pg.mkPen(color=color, width=2), name=line_name)
        # --------------------------
        self.graph_size = len(graph_raw_data.get("press",[]))
        self.set_xrange()
        self.set_xlabel()

    def set_xrange(self,xrange_size=None):
        if xrange_size:
            try:
                self.xrange_size = int(xrange_size)
            except:
                self.xrange_size = self.graph_size     
        x_range1 = self.graph_size  - self.xrange_size
        x_range1 = x_range1 if x_range1 > 0 else 0
        x_range2 = self.graph_size  + 2 if x_range1 > 0 else self.xrange_size + 2
        self.widgets['graph'].setXRange(x_range1,x_range2, padding=0) 

    def set_xlabel(self):
        bottom_axis = self.widgets['graph'].getPlotItem().getAxis('bottom')
        step = 6 #30초간격
        bottom_axis.setTicks([[(idx,str(idx*5)) for idx in range(0,self.graph_size,step)]])       
        bottom_axis.setTextPen(pg.mkPen('k'))


# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    v = View()
    v.set_graph({"current":[0,0,0,150,200,250,],"elec_distance":[]})
    v.show()
    app.exec_()
