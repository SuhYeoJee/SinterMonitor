import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QTimer, Qt
from random import randint

def create_graph_view():
    # QGraphicsView 및 QGraphicsScene 생성
    view = QGraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)
    view.setGeometry(0,0, 600, 400)
    return view, scene

def update_graph(scene, data):
    # 이전 그래프 삭제
    scene.clear()

    # 파란색 펜 생성
    pen = QPen(Qt.blue, 2)

    # 그래프 그리기
    for i in range(len(data) - 1):
        x1, y1 = i * 50, 600-data[i] * 10
        x2, y2 = (i + 1) * 50, 600-data[i + 1] * 10
        scene.addLine(x1, y1, x2, y2, pen)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-time Line Graph Example")

        # QGraphicsView 생성
        self.view, self.scene = create_graph_view()
        self.setCentralWidget(self.view)

        # 데이터 초기화 및 QTimer 시작
        self.data = [0]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # 1초마다 데이터 업데이트

    def update_data(self):
        # 1에서 10 사이의 랜덤 값을 추가
        self.data.append(randint(1, 10))
        update_graph(self.scene, self.data)

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
