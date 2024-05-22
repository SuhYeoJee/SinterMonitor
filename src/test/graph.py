import sys
from PyQt5.QtWidgets import QGraphicsLineItem, QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()

        # QGraphicsView 및 QGraphicsScene 생성
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()

        # 세로축 높이 및 눈금 크기
        vertical_height = 300
        tick_size = 50

        # 그래프 시작 지점 (왼쪽 상단)
        start_x, start_y = 0, 0

        # x 축 그리기
        self.scene.addLine(start_x, start_y + vertical_height, start_x + 300, start_y + vertical_height)

        # y 축 그리기 및 눈금 추가
        self.scene.addLine(start_x, start_y, start_x, start_y + vertical_height)
        for i in range(0, vertical_height + 1, tick_size):
            tick = QGraphicsLineItem(start_x - 5, start_y + vertical_height - i, start_x + 5, start_y + vertical_height - i)
            self.scene.addItem(tick)
            text = self.scene.addText(str(i))
            text.setFont(QFont("Arial", 8))
            text.setPos(start_x - 30, start_y + vertical_height - i - 5)

        # 그래프 그리기
        data_points = [0, 50, 150, 100,  200, 300, 250]  # 예시 데이터 포인트
        for i in range(len(data_points) - 1):
            x1 = start_x + i * 50
            y1 = start_y + vertical_height - data_points[i]
            x2 = start_x + (i + 1) * 50
            y2 = start_y + vertical_height - data_points[i + 1]
            self.scene.addLine(x1, y1, x2, y2)

        # QGraphicsView에 scene 설정
        self.view.setScene(self.scene)

        # Layout 설정
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraphWidget()
    window.setWindowTitle('꺾은선 그래프')
    window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec_())
