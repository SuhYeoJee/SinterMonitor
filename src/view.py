if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
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
        # --------------------------
        screen = QDesktopWidget().screenGeometry() # 화면 크기 조정
        self.resize(int(screen.width() * 0.5), int(screen.height() * 0.73))
        self.setWindowTitle("window_title")
        self.create_menu()
        # --------------------------
        self.layouts['main'] = self.get_main_layout()
        # --------------------------
        self.widgets['main'] = QWidget()
        self.widgets['main'].setLayout(self.layouts['main'])
        self.setCentralWidget(self.widgets['main'])

    # [menu] ===========================================================================================
    def create_menu(self):
        menubar = self.menuBar()
        # -------------------------------------------------------------------------------------------
        load_action = QAction('Load', self)
        self.menus["load_action"] = load_action
        close_action = QAction('Close', self)
        self.menus["close_action"] = load_action
        # --------------------------
        file_menu = menubar.addMenu('File')
        file_menu.addAction(load_action)
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

    def save_action_triggered(self):
        print('Save clicked')

# ===========================================================================================
    def get_top_layout(self)->QHBoxLayout:
        top_layout = QHBoxLayout()
        self.widgets['message'] = self.wb.get_label("")
        top_layout.addWidget(self.widgets['message'],4)
        top_layout.addStretch(1)
        top_layout.addLayout(self.wb.get_label_and_line_edit_layout("총 작업시간",self.widgets,"work_time"))
        top_layout.addWidget(self.wb.get_vline_widget())
        self.widgets['now_date'] = self.wb.get_line_edit_widget(300)
        top_layout.addWidget(self.widgets['now_date'],2)
        

        self.widgets['b1'] = self.wb.get_button("b1")
        self.widgets['b2'] = self.wb.get_button("b2")
        self.widgets['b3'] = self.wb.get_button("b3")
        top_layout.addWidget(self.widgets['b1'])
        top_layout.addWidget(self.widgets['b2'])
        top_layout.addWidget(self.widgets['b3'])

        return top_layout
    # -------------------------------------------------------------------------------------------
    #temp
    def get_scale_layout(self)->QHBoxLayout:
        graph_scale_layout = QHBoxLayout()
        graph_scale_layout.addWidget(self.wb.get_label("표 눈금"))
        return graph_scale_layout
    def get_legend_layout(self)->QHBoxLayout:
        graph_legend_layout = QHBoxLayout()
        graph_legend_layout.addWidget(self.wb.get_label("범례")) #temp
        return graph_legend_layout

    def get_graph_view_layout(self)->QVBoxLayout:
        
        # data3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,1, 2, 3, 4, 5, 6, 7, 8, 9, 10,1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # view = self.create_multi_line_graph(data1, data2, data3)
        self.table_spec['graph_form']={'init_size' : (3,7), 'slim_rows' : [],'slim_cols' : [],'text_items' : {
                (0,0):[(1,1),"PRG.NO", ['center']],
                (0,1):[(1,1),"STEP", ['center']],
                (0,2):[(1,1),"Current", ['center']],
                (0,3):[(1,1),"Pressure", ['center']],
                (0,4):[(1,1),"Temperature", ['center']],
                (0,5):[(1,1),"Time", ['center']],
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
        }
        
        graph_table = TablePlusWidget(form_data=self.table_spec['graph_form'], pos_data=self.table_spec['graph_pos'])
        graph_table_layout = QHBoxLayout()
        graph_table_layout.addWidget(graph_table)
        self.widgets['graph_table'] = graph_table
        # --------------------------
        graph_scale_layout = self.get_scale_layout()
        graph_legend_layout = self.get_legend_layout()
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.wb.get_box_frame_widget(graph_scale_layout),2)
        self.widgets['graph_view'] = QGraphicsView()
        self.widgets['graph_scene'] = QGraphicsScene()
        self.widgets['graph_view'].setScene(self.widgets['graph_scene'])
        graph_layout.addWidget(self.widgets['graph_view'],16)
        graph_layout.addWidget(self.wb.get_box_frame_widget(graph_legend_layout),1)
        # --------------------------
        graph_view_layout = QVBoxLayout()
        graph_view_layout.addLayout(graph_layout,8)
        graph_view_layout.addWidget(self.wb.get_box_frame_widget(graph_table_layout),2)
        return graph_view_layout
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
                        (0,1):[(1,1),"Current%", ['center']],
                        (0,2):[(1,1),"Press Kg/cm²", ['center']],
                        (0,3):[(1,1),"Temp' °C", ['center']],
                        (0,4):[(1,1),"Time(sec)", ['center']],
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
                        (11,1):[(1,1),"", ['center']],
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
        program_table = TablePlusWidget(form_data=self.table_spec['program_form'],pos_data=self.table_spec['program_pos'])
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
        self.table_spec['mould_bottom_form']={'init_size' : (6,6), 'slim_rows' : [],'slim_cols' : [],
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
    def get_main_layout(self):
        self.layouts['top_layout'] = self.get_top_layout()
        self.layouts['graph_view_layout'] = self.get_graph_view_layout()
        self.layouts['program_view_layout'] = self.get_program_view_layout()
        self.layouts['mould_view_layout'] = self.get_mould_view_layout()
        # --------------------------
        bottom_view_layout = QHBoxLayout()
        bottom_view_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['program_view_layout']),1)
        bottom_view_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['mould_view_layout']),1)
        # --------------------------
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.wb.get_box_frame_widget(self.layouts['top_layout']))
        main_layout.addLayout(self.layouts['graph_view_layout'],6)
        main_layout.addLayout(bottom_view_layout,4)
        return main_layout
    
    def show_connect_success_box(self):
        msg = self.wb.get_message_box('info','Success','Connection successful')
        QTimer.singleShot(3000, msg.accept)
        msg.exec_()

    def show_connect_failure_box(self):
        msg = self.wb.get_message_box('critical','Error','Connection failed')
        msg.exec_()

    def show_disconnect_success_box(self):
        msg = self.wb.get_message_box('info','Success','disConnection successful')
        QTimer.singleShot(3000, msg.accept)
        msg.exec_()

    # ===========================================================================================
    def set_value_by_label_and_text(self,table_name,datas:dict):
        pos_and_text = {v:datas[k] for k,v in self.table_spec[table_name.replace('_table','_pos')].items() if k in datas.keys()}
        self.widgets[table_name].fill_datas_position(pos_and_text)

    def set_graph(self,graph_raw_data:dict):
        scene:QGraphicsScene = self.widgets['graph_scene']
        view:QGraphicsView = self.widgets['graph_view']
        scene.clear()
        # -------------------------------------------------------------------------------------------
        def draw_line(scene, data, color):
            pen = QPen(color)
            pen.setWidth(2)
            for i in range(len(data) - 1):
                x1, y1 = i * 50, 300 - data[i] * 10
                x2, y2 = (i + 1) * 50, 300 - data[i + 1] * 10
                scene.addLine(x1, y1, x2, y2, pen)
            return scene
        # --------------------------
        for line_name, line_data in graph_raw_data.items():
            if 'current' in line_name:
                color = Qt.red
            elif 'press' in line_name:
                color = Qt.black
            else:
                color = Qt.blue
            draw_line(scene,line_data,color)
        # --------------------------
        def focus_on_right_end():
            scene_rect = view.scene().itemsBoundingRect()
            right_end = scene_rect.right()
            view.ensureVisible(QRectF(right_end, 0, 1, 1))
        focus_on_right_end()
        # self.widgets['graph_view'].fitInView(scene.sceneRect(), Qt.KeepAspectRatio) 

# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    v = View()
    v.show()
    app.exec_()
