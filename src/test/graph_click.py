import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

class CustomPlotWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 왼쪽 y축 데이터 추가
        self.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50], pen='r')
        
        # 오른쪽 y축을 위한 추가 ViewBox 생성
        self.rightViewBox = pg.ViewBox()
        self.scene().addItem(self.rightViewBox)
        
        # 오른쪽 y축 추가
        self.getPlotItem().layout.addItem(self.rightViewBox, 2, 2)
        self.getPlotItem().scene().addItem(self.rightViewBox)
        self.getPlotItem().showAxis('right')
        self.getPlotItem().getAxis('right').linkToView(self.rightViewBox)
        self.rightViewBox.setXLink(self.getPlotItem())
        
        # 오른쪽 y축 데이터 추가
        right_plot = pg.PlotDataItem([1, 2, 3, 4, 5], [100, 200, 300, 400, 500], pen='b')
        self.rightViewBox.addItem(right_plot)
        
        # 업데이트 함수 설정
        self.getPlotItem().vb.sigResized.connect(self.updateViews)
        
    def updateViews(self):
        self.rightViewBox.setGeometry(self.getPlotItem().vb.sceneBoundingRect())
        self.rightViewBox.linkedViewChanged(self.getPlotItem().vb, self.rightViewBox.XAxis)
        
app = QtGui.QApplication([])
win = CustomPlotWidget()
win.show()
QtGui.QApplication.instance().exec_()
