import sys
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer, QTime, QDate

# 載入您轉好的 UI 檔案
from ui_py.mainwindow import Ui_MainWindow
from models.data_manager import DataManager

class MainController:
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager
        
        # 初始化主視窗與 UI
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        # 設定預設的賽事名稱
        self.ui.match_name_l.setText("2026 大專盃羽球邀請賽")

        # 啟動系統時鐘 (每 1 秒觸發一次)
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock() # 程式剛開時先手動呼叫一次，避免第一秒沒畫面

        # 啟動賽事狀態監控器 (例如每 60 秒檢查一次賽程時間)
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_match_status)
        self.status_timer.start(60000)

        # 綁定底部功能按鈕
        self._bind_signals()

    def _bind_signals(self):
        """綁定 UI 按鈕的點擊事件"""
        self.ui.team_list_btn.clicked.connect(self.open_team_controller)
        self.ui.all_match_btn.clicked.connect(self.open_match_controller)

    def update_clock(self):
        """更新狀態列的系統時間"""
        current_time = QTime.currentTime().toString("HH:mm:ss")
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        # 顯示在您 UI 裡面的 statusbar
        self.ui.statusbar.showMessage(f"目前時間: {current_date} {current_time}")

    def update_match_status(self):
        """定期比對賽程時間，移動賽事卡片 (後續實作)"""
        # 這裡未來會向 DataManager 拿取 match 資料，比對時間後分類到三個 QGraphicsView 中
        pass

    def open_team_controller(self):
        """點擊「隊伍/選手名單」按鈕"""
        print("準備開啟隊伍管理介面...")
        # 這裡之後會呼叫 TeamController

    def open_match_controller(self):
        """點擊「所有賽事」按鈕"""
        print("準備開啟賽程管理介面...")
        # 這裡之後會呼叫 MatchController

    def show(self):
        """顯示主視窗"""
        self.window.show()