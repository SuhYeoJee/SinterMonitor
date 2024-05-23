import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot

# 데이터 생성 및 메인 스레드로 신호를 보내기 위한 Worker 클래스 정의
class Worker(QThread):
    # 데이터 생성 시 발행할 신호 정의, 생성된 데이터를 전달할 수 있도록 int 타입의 인자를 가짐
    data_generated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = True  # 스레드 실행 여부를 확인하기 위한 플래그

    def run(self):
        # 무한 루프를 돌면서 데이터 생성
        while self.running:
            value = random.randint(1, 10)  # 1에서 10 사이의 랜덤 값을 생성
            self.data_generated.emit(value)  # 신호를 통해 메인 스레드로 데이터 전달
            self.msleep(1000)  # 1초 대기 (msleep은 QThread의 메서드로 1000ms 동안 대기)

    def stop(self):
        self.running = False  # 스레드 종료를 위해 플래그를 False로 설정

# 메인 윈도우 클래스 정의
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Data Update")  # 윈도우 제목 설정
        self.setGeometry(100, 100, 400, 300)  # 윈도우 크기와 위치 설정

        self.data = []  # 데이터 저장을 위한 리스트 초기화
        self.table_widget = QTableWidget(10, 1)  # 10행 1열의 테이블 위젯 생성
        self.start_button = QPushButton("Start")  # 시작 버튼 생성
        self.stop_button = QPushButton("Stop")  # 종료 버튼 생성

        # 레이아웃 설정
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Worker 객체 초기화
        self.worker = Worker()

        # 버튼 클릭 시 슬롯 연결
        self.start_button.clicked.connect(self.start_worker)
        self.stop_button.clicked.connect(self.stop_worker)

    # Worker 스레드를 시작하는 슬롯
    @pyqtSlot()
    def start_worker(self):
        if not self.worker.isRunning():
            self.worker = Worker()  # 새 Worker 객체 생성
            self.worker.data_generated.connect(self.update_table)  # Worker의 신호를 update_table 메서드에 연결
            self.worker.start()  # Worker 스레드를 시작

    # Worker 스레드를 종료하는 슬롯
    @pyqtSlot()
    def stop_worker(self):
        self.worker.stop()  # Worker 스레드 종료

    # 테이블 위젯을 업데이트하는 메서드
    @pyqtSlot(int)
    def update_table(self, value):
        self.data.append(value)  # 새로운 값을 데이터 리스트에 추가
        if len(self.data) > 10:
            self.data.pop(0)  # 리스트의 길이가 10을 초과하면 가장 오래된 값을 제거
        for i, val in enumerate(self.data):
            item = QTableWidgetItem(str(val))  # 리스트의 각 값을 QTableWidgetItem으로 변환
            self.table_widget.setItem(i, 0, item)  # 테이블 위젯의 각 행에 값을 설정

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    window = MainWindow()  # MainWindow 객체 생성
    window.show()  # 메인 윈도우 표시
    sys.exit(app.exec_())  # 이벤트 루프 실행
