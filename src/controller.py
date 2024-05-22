if __debug__:
    import sys
    sys.path.append(r"D:\Github\SinterMonitor")
# -------------------------------------------------------------------------------------------
from src.model import Model
from src.view import View    
from src.module.pyqt_imports import *
from src.module.exceptions import *
# ===========================================================================================
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        # --------------------------
        self.set_lay1_from_model_val()
    # -------------------------------------------------------------------------------------------
    def set_lay1_from_model_val(self):
        model_val = self.model.get_val()
        self.view.change_main_text(model_val)


# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()

if __name__ == "__main__":
    main()