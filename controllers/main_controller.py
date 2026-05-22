import sys
import datetime
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsProxyWidget, QMessageBox
from PySide6.QtCore import QTimer, QTime, QDate, Qt

from ui_py.mainwindow import Ui_MainWindow
from models.data_manager import DataManager
from components.match_card import MatchCardWidget
from controllers.team_controller import TeamController
from controllers.match_controller import MatchController
from controllers.checkin_dialog import CheckInDialog
class MainController:
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager
        
        # 初始化主視窗與 UI
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        # 設定賽事名稱
        self.ui.match_name_l.setText("115年農院盃羽球賽")

        # 為三個看板區塊建立各自的 QGraphicsScene
        self.progress_scene = QGraphicsScene()
        self.prep_scene = QGraphicsScene()
        self.upcoming_scene = QGraphicsScene()

        self.ui.match_in_progress_view.setScene(self.progress_scene)
        self.ui.match_in_preperation_view.setScene(self.prep_scene)
        self.ui.match_upcoming_view.setScene(self.upcoming_scene)

        # 為了計算閃爍，設定全域的閃爍計數器與狀態旗標
        self.flash_counter = 0
        self.flash_1s_on = True
        self.flash_2s_on = True

        # 卡片內部快取，避免重複建立 Widget 造成畫面閃爍
        # 格式: { match_id: (QGraphicsProxyWidget, MatchCardWidget) }
        self.card_cache = {}

        # 啟動系統核心時鐘與閃爍心跳 (每 0.5 秒觸發一次)
        self.heartbeat_timer = QTimer()
        self.heartbeat_timer.timeout.connect(self.system_heartbeat)
        self.heartbeat_timer.start(500)
        
        # 立即執行一次初始狀態分配
        self.system_heartbeat()

        # 綁定底部功能按鈕
        self._bind_signals()

    def _bind_signals(self):
        """綁定主畫面按鈕事件"""
        self.ui.team_list_btn.clicked.connect(self.open_team_controller)
        self.ui.all_match_btn.clicked.connect(self.open_match_controller)

    def system_heartbeat(self):
        """系統全域心跳：每 0.5 秒更新一次時間、計時器狀態與外框閃爍"""
        current_dt = datetime.datetime.now()
        
        # 更新狀態列時間顯示
        current_time_str = current_dt.strftime("%H:%M:%S")
        current_date_str = current_dt.strftime("%Y-%m-%d")
        self.ui.statusbar.showMessage(f"目前時間: {current_date_str} {current_time_str}")

        # 閃爍頻率加倍
        self.flash_counter = (self.flash_counter + 1) % 4
        
        # 0.5 秒閃爍
        self.flash_1s_on = not self.flash_1s_on
        
        # 1.0 秒閃爍
        if self.flash_counter % 2 == 0:
            self.flash_2s_on = not self.flash_2s_on

        # 驅動賽事狀態機與介面重新排序
        self.update_match_dashboard(current_dt)

    def update_match_dashboard(self, current_dt: datetime.datetime):
        """核心邏輯：比對時間、分配賽事到不同區塊，並進行垂直排序"""
        
        # 將未結束的賽事依照「比賽開始時間」進行升冪排序（由早到晚直排）
        active_matches = [m for m in self.dm.matches.values() if m.status != "finished"]
        try:
            active_matches.sort(key=lambda x: datetime.datetime.strptime(x.start_time, "%Y-%m-%d %H:%M"))
        except ValueError:
            pass # 預防時間格式錯誤

        # 分類容器
        progress_list = []
        prep_list = []
        upcoming_list = []

        # 時間判定基準 (將先前 MatchCardWidget 內的邏輯在此進行宏觀分類)
        fmt = "%Y-%m-%d %H:%M"
        for match in active_matches:
            if match.match_id not in self.card_cache:
                t1_name = self.dm.teams[match.team1_id].name if match.team1_id in self.dm.teams else "未知"
                t2_name = self.dm.teams[match.team2_id].name if match.team2_id in self.dm.teams else "未知"
                
                # 將分離的資料重新組合成顯示字串
                games_str = "單局" if match.win_games == 1 else ("三戰兩勝" if match.win_games == 2 else "五戰三勝")
                rule_display = f"{match.match_category} ({games_str}{match.points_per_game}分)"
                
                # 建立實體 Widget (替換原本的 match.match_type 為 rule_display)
                card_widget = MatchCardWidget(
                    match_id=match.match_id, court=match.court, stage="分組循環賽",
                    team1_name=t1_name, team2_name=t2_name, match_rule=rule_display,
                    start_time=match.start_time, end_time=match.end_time, status=match.status
                )
                proxy = QGraphicsProxyWidget()
                proxy.setWidget(card_widget)
                self.card_cache[match.match_id] = (proxy, card_widget)

                card_widget.checkin_clicked.connect(self.handle_checkin)
                card_widget.start_clicked.connect(self.handle_start_match)
                card_widget.finish_clicked.connect(self.handle_finish_match)
            
            proxy, card_widget = self.card_cache[match.match_id]
            
            # 同步更新 Model 的最新狀態至 UI
            card_widget.status = match.status 
            # 通知卡片根據全域時間與閃爍旗標更新外框顏色
            card_widget.update_state(current_dt, self.flash_1s_on, self.flash_2s_on)

            # 根據狀態與時間差距分流至三大看版
            try:
                start_dt = datetime.datetime.strptime(match.start_time, fmt)
                diff_start_mins = (start_dt - current_dt).total_seconds() / 60.0
            except ValueError:
                diff_start_mins = 9999

            if match.status == "in_progress":
                progress_list.append(proxy)
            elif match.status == "checked_in":
                prep_list.append(proxy)
            elif match.status == "upcoming":
                # 符合「準備進行」的時間條件：小於10分鐘，或是時間已到但未檢錄
                if diff_start_mins <= 10:
                    prep_list.append(proxy)
                elif diff_start_mins <= 60:
                    upcoming_list.append(proxy)
                else:
                    # 超過1小時的賽事暫不顯示在主畫面上，先移出場景
                    if proxy.scene():
                        proxy.scene().removeItem(proxy)

        # 4. 重新繪製並垂直排列各個 Scene
        self._arrange_scene(self.progress_scene, progress_list)
        self._arrange_scene(self.prep_scene, prep_list)
        self._arrange_scene(self.upcoming_scene, upcoming_list)

    def _arrange_scene(self, scene: QGraphicsScene, proxy_list: list):
        """將指定的 Proxy 清單由上至下垂直直排擺放，並自動調整場景大小"""
        # 先將所有代理物件移出場景，避免殘留
        for proxy in list(scene.items()):
            if isinstance(proxy, QGraphicsProxyWidget):
                scene.removeItem(proxy)

        y_offset = 10
        card_spacing = 15  # 卡片與卡片之間的垂直間距

        for proxy in proxy_list:
            scene.addItem(proxy)
            # 居中對齊：計算 X 軸使其在視圖寬度內水平置中 (預設寬度約 220-240)
            proxy.setPos(10, y_offset)
            # 累加高度 (MatchCardWidget 固定高度為 260)
            y_offset += 260 + card_spacing

        # 更新場景邊界，確保滾動條正常運作
        scene.setSceneRect(0, 0, 240, max(y_offset, 500))

    # ==========================================
    # 賽事操作邏輯 (狀態機轉移)
    # ==========================================
    def handle_checkin(self, match_id: str):
        """處理點擊「檢錄」按鈕"""
        dialog = CheckInDialog(self.dm, match_id, self.window)
        if dialog.exec() == CheckInDialog.Accepted:
            # 檢錄成功，更改狀態並存檔
            self.dm.matches[match_id].status = "checked_in"
            self.dm._save_matches()
            QMessageBox.information(self.window, "檢錄完成", f"賽事 {match_id} 檢錄完畢，等待進場。")
            # 立即手動觸發一次心跳以更新畫面排列
            self.system_heartbeat()

    def handle_start_match(self, match_id: str):
        """處理點擊「開始賽事」按鈕"""
        reply = QMessageBox.question(self.window, "確認", f"確定要開始賽事 {match_id} 嗎？\n場地將被標記為佔用。",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.dm.matches[match_id].status = "in_progress"
            self.dm._save_matches()
            self.system_heartbeat()

    def handle_finish_match(self, match_id: str):
        """處理點擊「結束賽事」按鈕"""
        reply = QMessageBox.question(self.window, "確認", f"確定要結束賽事 {match_id} 嗎？\n這將把賽事移出主畫面。",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.dm.matches[match_id].status = "finished"
            self.dm._save_matches()
            # 結束的賽事直接從快取跟場景中移除
            if match_id in self.card_cache:
                proxy, _ = self.card_cache.pop(match_id)
                if proxy.scene():
                    proxy.scene().removeItem(proxy)
            self.system_heartbeat()

    # ==========================================
    # 視窗導覽切換
    # ==========================================
    def open_team_controller(self):
        if not hasattr(self, 'team_ctrl') or not self.team_ctrl.window.isVisible():
            self.team_ctrl = TeamController(self.dm)
            self.team_ctrl.show()
        else:
            self.team_ctrl.window.raise_()
            self.team_ctrl.window.activateWindow()

    def open_match_controller(self):
        if not hasattr(self, 'match_ctrl') or not self.match_ctrl.window.isVisible():
            self.match_ctrl = MatchController(self.dm)
            self.match_ctrl.show()
        else:
            self.match_ctrl.window.raise_()
            self.match_ctrl.window.activateWindow()

    def show(self):
        self.window.show()