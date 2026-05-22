from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from models.data_manager import DataManager

class CheckInDialog(QDialog):
    def __init__(self, dm: DataManager, match_id: str, parent=None):
        super().__init__(parent)
        self.dm = dm
        self.match = self.dm.matches[match_id]
        
        # 取得隊伍資訊
        self.team1 = self.dm.teams.get(self.match.team1_id)
        self.team2 = self.dm.teams.get(self.match.team2_id)
        
        # 撈取隸屬於這兩支隊伍的所有選手
        self.team1_athletes = [a for a in self.dm.athletes.values() if a.team_id == self.match.team1_id]
        self.team2_athletes = [a for a in self.dm.athletes.values() if a.team_id == self.match.team2_id]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"賽事檢錄 - {self.match.match_id}")
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)

        games_str = "單局" if self.match.win_games == 1 else ("三戰兩勝" if self.match.win_games == 2 else "五戰三勝")
        rule_display = f"{self.match.match_category} ({games_str}{self.match.points_per_game}分)"

        info_label = QLabel(f"<b>賽制：</b>{rule_display}<br>"
                            f"<b>隊伍：</b>{self.team1.name} vs {self.team2.name}")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        players_needed = 2 if "雙" in self.match.match_category else 1
        
        gb1 = QGroupBox(f"{self.team1.name} 出賽名單")
        vbox1 = QVBoxLayout(gb1)
        self.t1_cboxes = []
        for i in range(players_needed):
            cb = QComboBox()
            cb.addItem("-- 請選擇選手 --", None)
            for ath in self.team1_athletes:
                cb.addItem(f"{ath.name} ({ath.student_id})", ath.athlete_id)
            self.t1_cboxes.append(cb)
            vbox1.addWidget(cb)
        layout.addWidget(gb1)

        gb2 = QGroupBox(f"{self.team2.name} 出賽名單")
        vbox2 = QVBoxLayout(gb2)
        self.t2_cboxes = []
        for i in range(players_needed):
            cb = QComboBox()
            cb.addItem("-- 請選擇選手 --", None)
            for ath in self.team2_athletes:
                cb.addItem(f"{ath.name} ({ath.student_id})", ath.athlete_id)
            self.t2_cboxes.append(cb)
            vbox2.addWidget(cb)
        layout.addWidget(gb2)

        # 確認按鈕
        btn_layout = QHBoxLayout()
        confirm_btn = QPushButton("確認檢錄並存檔")
        confirm_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addStretch()
        btn_layout.addWidget(confirm_btn)
        
        layout.addLayout(btn_layout)

    def validate_and_accept(self):
        """防呆機制與寫入名單"""
        t1_selected = [cb.currentData() for cb in self.t1_cboxes if cb.currentData() is not None]
        t2_selected = [cb.currentData() for cb in self.t2_cboxes if cb.currentData() is not None]

        # 防呆 1：名單未選滿
        if len(t1_selected) < len(self.t1_cboxes) or len(t2_selected) < len(self.t2_cboxes):
            QMessageBox.warning(self, "錯誤", "請完整選擇雙方的出賽選手！")
            return

        # 防呆 2：雙打選擇了同一個人
        if len(set(t1_selected)) != len(t1_selected) or len(set(t2_selected)) != len(t2_selected):
            QMessageBox.warning(self, "錯誤", "同一名選手不能在同一場賽事中重複排點！")
            return

        # 整理要寫入 CSV 的資料結構
        lineups_data = []
        for athlete_id in t1_selected:
            lineups_data.append({'team_id': self.match.team1_id, 'athlete_id': athlete_id})
        for athlete_id in t2_selected:
            lineups_data.append({'team_id': self.match.team2_id, 'athlete_id': athlete_id})
            
        # 呼叫 DataManager 進行寫入
        try:
            self.dm.save_match_lineup(self.match.match_id, lineups_data)
            self.accept() # 寫入成功後才關閉對話框並回傳 Accepted
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"名單寫入檔案失敗: {e}")