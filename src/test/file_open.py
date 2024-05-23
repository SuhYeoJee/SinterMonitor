import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('File Dialog Example')
        self.setGeometry(100, 100, 600, 400)

        # 메뉴바 생성
        menubar = self.menuBar()
        file_menu = menubar.addMenu('파일')

        # 불러오기 메뉴 생성
        load_action = QAction('불러오기', self)
        load_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(load_action)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            print(f"선택한 파일 경로: {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
