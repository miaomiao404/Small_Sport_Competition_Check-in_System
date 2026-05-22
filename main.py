import sys
from PySide6.QtWidgets import QApplication
from models.data_manager import DataManager
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    print("正在載入資料庫...")
    dm = DataManager(data_dir="data")
    
    print("正在啟動主畫面...")
    main_ctrl = MainController(data_manager=dm)
    main_ctrl.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()