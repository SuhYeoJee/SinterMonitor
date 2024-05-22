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
    # -------------------------------------------------------------------------------------------
    def get_lay1(self,val:str=''):
        lay1 = QVBoxLayout()
        self.widgets['main_text'] = self.wb.get_label(f"new project: {val}")
        lay1.addWidget(self.widgets['main_text'])
        return lay1
    
    def change_main_text(self,val:str=''):
        self.widgets['main_text'].setText(val)
    # [menu] ===========================================================================================
    def create_menu(self):
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_action_triggered)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_action_triggered)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        # --------------------------
        menubar = self.menuBar()
        file_menu = menubar.addMenu('불러오기')
        afe = menubar.addMenu('실시간모니터')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
    # -------------------------------------------------------------------------------------------
    def open_action_triggered(self):
        print('Open clicked')

    def save_action_triggered(self):
        print('Save clicked')
    # ===========================================================================================

    #temp
    def create_multi_line_graph(self,data1, data2, data3):
        def draw_line(scene, data, color):
            # 선을 그리기 위한 펜 설정
            pen = QPen(color)
            pen.setWidth(2)

            # 선 그리기
            for i in range(len(data) - 1):
                x1, y1 = i * 50, 300 - data[i] * 10
                x2, y2 = (i + 1) * 50, 300 - data[i + 1] * 10
                scene.addLine(x1, y1, x2, y2, pen)

            return scene
        # QGraphicsView 및 QGraphicsScene 생성
        view = QGraphicsView()
        scene = QGraphicsScene()
        view.setScene(scene)
        # 각 데이터에 대한 선 그리기
        draw_line(scene, data1, Qt.red)
        draw_line(scene, data2, Qt.green)
        draw_line(scene, data3, Qt.blue)
        return view

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
        
        # data1 = [3, 5, 7, 9, 6, 8, 4, 2, 1, 3,3, 5, 7, 9, 6, 8, 4, 2, 1, 3,3, 5, 7, 9, 6, 8, 4, 2, 1, 3]
        # data2 = [8, 6, 4, 2, 5, 7, 9, 1, 3, 2,8, 6, 4, 2, 5, 7, 9, 1, 3, 2,8, 6, 4, 2, 5, 7, 9, 1, 3, 2]
        # data3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,1, 2, 3, 4, 5, 6, 7, 8, 9, 10,1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # view = self.create_multi_line_graph(data1, data2, data3)
        graph_table_form={'init_size' : (3,7), 'slim_rows' : [],'slim_cols' : [],'text_items' : {
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
        graph_table_pos={
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
        
        graph_table = TablePlusWidget(form_data=graph_table_form, pos_data=graph_table_pos)
        graph_table_layout = QHBoxLayout()
        graph_table_layout.addWidget(graph_table)
        self.widgets['graph_table'] = graph_table
        # --------------------------
        graph_scale_layout = self.get_scale_layout()
        graph_legend_layout = self.get_legend_layout()
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.wb.get_box_frame_widget(graph_scale_layout),2)
        self.widgets['graph_view'] = QGraphicsView()
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
        program_table_form={'init_size' : (12,6), 'slim_rows' : [],'slim_cols' : [],
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
        program_table_pos={
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
        program_table = TablePlusWidget(form_data=program_table_form,pos_data=program_table_pos)
        self.widgets['program_table'] = program_table
        program_view_layout = QVBoxLayout()
        program_view_layout.addLayout(program_top_layout)
        program_view_layout.addWidget(program_table)
        return program_view_layout
    # -------------------------------------------------------------------------------------------
    def get_mould_view_layout(self)->QVBoxLayout:
        mould_top_table_form ={'init_size' : (5,6), 'slim_rows' : [],'slim_cols' : [],
                    'text_items' : {
                        (0,0):[(1,1),"Magazine", ['center']],
                        (1,0):[(1,1),"Start", ['center']],
                        (3,0):[(1,1),"Finish", ['center']],
                        (1,3):[(2,1),"sintering Magazine", ['center']],
                        (1,4):[(2,1),"", ['center']],
                        (1,5):[(2,1),"", ['center']],
                        (3,3):[(1,2),"work prg.no", ['center']],
                        (4,3):[(1,2),"work count", ['center']],
                    }}
        mould_top_table_pos={
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
            "sint_magazine_l":(1,4),
            "sint_magazine_r":(1,5),
            "work_prg_no":(3,5),
            "work_count":(4,5),                            
        }
        mould_top_table = TablePlusWidget(form_data=mould_top_table_form,pos_data=mould_top_table_pos)
        self.widgets['mould_top_table'] = mould_top_table
        # --------------------------
        mould_bottom_table_form={'init_size' : (6,6), 'slim_rows' : [],'slim_cols' : [],
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
        mould_bottom_table_pos={
            "step1_current":(1,1),
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
        mould_bottom_table = TablePlusWidget(form_data=mould_bottom_table_form,pos_data=mould_bottom_table_pos)
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

# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    window = View()
    window.show()
    app.exec_()
