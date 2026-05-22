import datetime
from PySide6.QtWidgets import QMainWindow, QDialog, QMessageBox, QGraphicsScene, QGraphicsProxyWidget, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from models.data_manager import DataManager
from ui_py.matchlist import Ui_MainWindow as Ui_MatchList
from ui_py.addmatch import Ui_court_court_edit as Ui_AddMatch
from components.match_card import MatchCardWidget
from controllers.score_dialog import ScoreDialog

class MatchController:
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager
        
        self.window = QMainWindow()
        self.ui = Ui_MatchList()
        self.ui.setupUi(self.window)
        
        self.scene = QGraphicsScene()
        self.ui.match_list_view.setScene(self.scene)
        
        self._bind_signals()
        self._refresh_view()

    def show(self):
        self._refresh_view() # 每次顯示時重新整理畫面，確保資料同步
        self.window.show()

    def _bind_signals(self):
        self.ui.add_match_btn.clicked.connect(self.open_add_match_dialog)

    def open_add_match_dialog(self):
        teams = self.dm.get_all_teams()
        if len(teams) < 2:
            QMessageBox.warning(self.window, "提示", "請先建立至少兩支隊伍才能排定賽程。")
            return

        dialog = QDialog()
        ui = Ui_AddMatch()
        ui.setupUi(dialog)

        for team in teams:
            ui.team_1_cbox.addItem(team.name, userData=team.team_id)
            ui.team_2_cbox.addItem(team.name, userData=team.team_id)

        # ✅ 更新局數與分數選項
        ui.match_type_cbox_2.clear()
        ui.match_type_cbox_2.addItems([
            "單局11分", "單局15分", "單局21分", "單局25分",
            "三戰兩勝11分", "三戰兩勝15分", "三戰兩勝21分", "三戰兩勝25分",
            "五戰三勝11分", "五戰三勝21分"
        ])

        if dialog.exec() == QDialog.Accepted:
            match_num = str(ui.match_num_sbox.value())
            match_id = f"M{match_num.zfill(3)}"
            
            team1_id = ui.team_1_cbox.currentData()
            team2_id = ui.team_2_cbox.currentData()
            
            if team1_id == team2_id:
                QMessageBox.warning(self.window, "錯誤", "對戰隊伍不能相同！")
                return
                
            match_category = ui.match_type_cbox.currentText()
            selected_rule = ui.match_type_cbox_2.currentText()
            
            # ✅ 將字串轉換為數字邏輯
            if "單局" in selected_rule:
                win_games = 1
                points_per_game = int(selected_rule.replace("單局", "").replace("分", ""))
            elif "三戰兩勝" in selected_rule:
                win_games = 2
                points_per_game = int(selected_rule.replace("三戰兩勝", "").replace("分", ""))
            elif "五戰三勝" in selected_rule:
                win_games = 3
                points_per_game = int(selected_rule.replace("五戰三勝", "").replace("分", ""))
            else:
                win_games, points_per_game = 1, 21

            start_time = ui.start_time_dtedit.dateTime().toString("yyyy-MM-dd HH:mm")
            end_time = ui.end_time_dtedit.dateTime().toString("yyyy-MM-dd HH:mm")
            court = ui.remark_edit_2.text().strip()
            remark = ui.remark_edit.text().strip()

            try:
                self.dm.add_match(match_id, match_category, win_games, points_per_game, team1_id, team2_id, 
                                  court, start_time, end_time, "upcoming", remark)
                self._refresh_view()
                QMessageBox.information(self.window, "成功", f"賽事 {match_id} 已排定。")
            except Exception as e:
                QMessageBox.critical(self.window, "錯誤", f"儲存失敗: {e}")

    def _refresh_view(self):
        """實作時間軸網格佈局演算法"""
        self.scene.clear()
        
        # 1. 將賽事依據「開始時間」進行分組 (Grouping)
        time_groups = {}
        for match in self.dm.matches.values():
            if match.start_time not in time_groups:
                time_groups[match.start_time] = []
            time_groups[match.start_time].append(match)
            
        # 2. 將時間鍵值進行升冪排序，形成 X 軸的順序
        try:
            sorted_times = sorted(time_groups.keys(), key=lambda t: datetime.datetime.strptime(t, "%Y-%m-%d %H:%M"))
        except ValueError:
            sorted_times = sorted(time_groups.keys())

        # 佈局常數設定
        x_offset = 10
        card_width = 190
        card_height = 250
        spacing_x = 20
        spacing_y = 15
        header_height = 40
        max_y = 0

        # 3. 繪製網格
        for time_str in sorted_times:
            matches_in_slot = time_groups[time_str]
            
            # 建立頂部時間標籤 (X 軸標頭)
            time_hm = time_str.split(" ")[1] if " " in time_str else time_str
            time_text = QGraphicsTextItem(f"🕒 {time_hm}")
            time_text.setFont(QFont("Arial", 16, QFont.Bold))
            time_text.setPos(x_offset, 10)
            self.scene.addItem(time_text)
            
            y_offset = 10 + header_height
            
            # 垂直堆疊該時段內的所有賽事 (Y 軸)
            # 垂直堆疊該時段內的所有賽事 (Y 軸)
            for match in matches_in_slot:
                t1_name = self.dm.teams[match.team1_id].name if match.team1_id in self.dm.teams else "未知"
                t2_name = self.dm.teams[match.team2_id].name if match.team2_id in self.dm.teams else "未知"

                # 將分離的資料重新組合成顯示字串
                games_str = "單局" if match.win_games == 1 else ("三戰兩勝" if match.win_games == 2 else "五戰三勝")
                rule_display = f"{match.match_category} ({games_str}{match.points_per_game}分)"
                
                # 建立實體 Widget (替換原本的 match.match_type 為 rule_display)
                card = MatchCardWidget(
                    match_id=match.match_id, court=match.court, stage="分組循環賽",
                    team1_name=t1_name, team2_name=t2_name, match_rule=rule_display,
                    start_time=match.start_time, end_time=match.end_time, status=match.status
                )
                
                card.score_clicked.connect(self.handle_score)

                # 在總表視圖中隱藏操作按鈕，純作為資訊展示
                card.btn_checkin.hide()
                card.btn_start.hide()
                card.btn_finish.hide()
                card.set_winner_ui(self.dm.get_match_winner(match.match_id))
                card.setFixedSize(card_width, card_height - 40) # 扣除按鈕區的高度
                
                # 依據賽事狀態標示外框顏色 (靜態顯示，無閃爍)
                current_dt = datetime.datetime.now()
                card.update_state(current_dt, flash_1s_on=True, flash_2s_on=True)
                
                proxy = QGraphicsProxyWidget()
                proxy.setWidget(card)
                proxy.setPos(x_offset, y_offset)
                self.scene.addItem(proxy)
                
                y_offset += (card_height - 40) + spacing_y
            
            x_offset += card_width + spacing_x
            max_y = max(max_y, y_offset)
            
        # 更新場景邊界，確保橫向與縱向滾動條能正確覆蓋所有範圍
        self.scene.setSceneRect(0, 0, x_offset, max_y + 20)
        
        # 更新底部統計數據
        total_matches = len(self.dm.matches)
        finished_matches = sum(1 for m in self.dm.matches.values() if m.status == "finished")
        
        self.ui.total_match_l.setText(f"賽事總數：{total_matches}")
        self.ui.already_matched_l.setText(f"已完成賽事數：{finished_matches}")
        self.ui.total_match_l_3.setText(f"未完成賽事數：{total_matches - finished_matches}")

    def handle_score(self, match_id: str):
        dialog = ScoreDialog(self.dm, match_id, self.window)
        if dialog.exec() == QDialog.Accepted:
            self._refresh_view()