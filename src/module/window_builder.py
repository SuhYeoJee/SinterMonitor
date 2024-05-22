from src.module.pyqt_imports import *

class WindowBuilder():
    def __init__(self):
        ...
    def get_button(self,button_text:str = None, clicked_func = lambda: None, *args):
        button = QPushButton(button_text)
        button.clicked.connect(lambda: clicked_func(*args))
        return button
    
    def get_label(self,label_text:str):
        return QLabel(label_text)

    def get_vline_widget(self):
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        return vline

    def get_hline_widget(self):
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        return hline

    def get_box_frame_widget(self,layout):
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLayout(layout)
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        return frame
    
    def get_box_frame_layout(self,layout):
        # 용례 : widget.setLayout(self.wb.get_box_frame_layout(layout))
        framed_layout = QHBoxLayout()
        framed_layout.addWidget(self.get_box_frame_widget(layout))
        return framed_layout

    def get_combo_box_widget(self, items, combo_func=lambda: None):
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.currentIndexChanged.connect(combo_func)
        # combo_box.setStyleSheet("QComboBox { text-align: center; }")
        return combo_box

    def get_line_edit_widget(self, size=100):
        lineEdit = QLineEdit()
        lineEdit.setFixedWidth(size) 
        return lineEdit
    
    def get_label_and_line_edit_layout(self, label_text,widgets:dict={}, key:str='', domains:list=[])->QHBoxLayout:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # --------------------------
        line_edit = QLineEdit()
        line_edit.setFixedWidth(200)

        if domains:
            completer = QCompleter([' ' + str(x) for x in domains])
            line_edit.setCompleter(completer)

        if not key:
            key = label_text
        widgets[key] = line_edit
        # --------------------------
        [layout.addWidget(x) for x in [QLabel(label_text), line_edit]]
        layout.addStretch(1)
        return layout

