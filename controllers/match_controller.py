from PySide6.QtWidgets import (QMainWindow, QDialog, QMessageBox, 
                               QGraphicsScene, QGraphicsTextItem)
from PySide6.QtCore import Qt

from models.data_manager import DataManager
from ui_py.matchlist import Ui_MainWindow as Ui_MatchList
# 名字打錯了，所以這裡是 Ui_court_court_edit
from ui_py.addmatch import Ui_court_court_edit as Ui_AddMatch

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
        self.window.show()

    def _bind_signals(self):
        """綁定「新增賽事」按鈕"""
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

        ui.match_type_cbox_2.clear()
        ui.match_type_cbox_2.addItems(["11分制", "21分制", "25分制", "31分制"])

        if dialog.exec() == QDialog.Accepted:
            match_num = str(ui.match_num_sbox.value())
            match_id = f"M{match_num.zfill(3)}"
            
            team1_id = ui.team_1_cbox.currentData()
            team2_id = ui.team_2_cbox.currentData()
            
            if team1_id == team2_id:
                QMessageBox.warning(self.window, "錯誤", "對戰隊伍不能相同！")
                return
            
            match_type = f"{ui.match_type_cbox.currentText()} ({ui.match_type_cbox_2.currentText()})"
            
            start_time = ui.start_time_dtedit.dateTime().toString("yyyy-MM-dd HH:mm")
            end_time = ui.end_time_dtedit.dateTime().toString("yyyy-MM-dd HH:mm")
            court = ui.remark_edit_2.text().strip()
            remark = ui.remark_edit.text().strip()

            try:
                self.dm.add_match(match_id, match_type, team1_id, team2_id, 
                                  court, start_time, end_time, "upcoming", remark)
                self._refresh_view()
                QMessageBox.information(self.window, "成功", f"賽事 {match_id} 已排定。")
            except Exception as e:
                QMessageBox.critical(self.window, "錯誤", f"儲存失敗: {e}")

    def _refresh_view(self):
        """更新賽事列表與底部統計數據"""
        self.scene.clear()
        y_offset = 0
        
        for match in self.dm.matches.values():
            t1_name = self.dm.teams[match.team1_id].name if match.team1_id in self.dm.teams else "未知隊伍"
            t2_name = self.dm.teams[match.team2_id].name if match.team2_id in self.dm.teams else "未知隊伍"
            
            display_text = f"[{match.match_id}] {match.start_time} | {t1_name} vs {t2_name} | {match.match_type} | 場地: {match.court}"
            text_item = QGraphicsTextItem(display_text)
            text_item.setPos(10, y_offset)
            self.scene.addItem(text_item)
            y_offset += 25
            
        total_matches = len(self.dm.matches)
        finished_matches = sum(1 for m in self.dm.matches.values() if m.status == "finished")
        
        self.ui.total_match_l.setText(f"賽事總數：{total_matches}")
        self.ui.already_matched_l.setText(f"已完成賽事數：{finished_matches}")
        self.ui.total_match_l_3.setText(f"未完成賽事數：{total_matches - finished_matches}")