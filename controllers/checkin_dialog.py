from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox, QPushButton, QMessageBox, QGroupBox, QScrollArea, QWidget)
from PySide6.QtCore import Qt
from models.data_manager import DataManager

# 🟢 核心配置：定義各賽事的點數與對應性別需求
MATCH_RULES = {
    "男單": [{"point": "主賽", "genders": ["男"]}],
    "女單": [{"point": "主賽", "genders": ["女"]}],
    "男雙": [{"point": "主賽", "genders": ["男", "男"]}],
    "女雙": [{"point": "主賽", "genders": ["女", "女"]}],
    "混雙": [{"point": "主賽", "genders": ["男", "女"]}],
    "團體": [
        {"point": "男單", "genders": ["男"]},
        {"point": "女單", "genders": ["女"]},
        {"point": "男雙", "genders": ["男", "男"]},
        {"point": "女雙", "genders": ["女", "女"]},
        {"point": "混雙", "genders": ["男", "女"]}
    ]
}

class CheckInDialog(QDialog):
    def __init__(self, dm: DataManager, match_id: str, parent=None):
        super().__init__(parent)
        self.dm = dm
        self.match = self.dm.matches[match_id]
        
        self.team1 = self.dm.teams.get(self.match.team1_id)
        self.team2 = self.dm.teams.get(self.match.team2_id)
        
        self.team1_athletes = [a for a in self.dm.athletes.values() if a.team_id == self.match.team1_id]
        self.team2_athletes = [a for a in self.dm.athletes.values() if a.team_id == self.match.team2_id]

        # 🟢 根據賽事類型載入規則 (支援子字串搜尋，例如 "男雙" 可匹配 "男雙 (21分)")
        cat = self.match.match_category
        self.rules = next((v for k, v in MATCH_RULES.items() if k in cat), [{"point": "主賽", "genders": ["男"]}])

        # 儲存下拉選單以便取值 (結構: { point_name: [cb1, cb2] })
        self.t1_cboxes = {} 
        self.t2_cboxes = {}

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"賽事檢錄 - {self.match.match_id}")
        self.setMinimumSize(600, 500) # 給予較大的初始視窗以容納團體賽
        main_layout = QVBoxLayout(self)

        # --- 1. 頂部資訊 ---
        games_str = "單局" if self.match.win_games == 1 else ("三戰兩勝" if self.match.win_games == 2 else "五戰三勝")
        rule_display = f"{self.match.match_category} ({games_str}{self.match.points_per_game}分)"

        info_label = QLabel(f"<b>賽制：</b>{rule_display}<br><b>隊伍：</b>{self.team1.name} vs {self.team2.name}")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        main_layout.addWidget(info_label)

        # --- 2. 建立滾動區域 (解決團體賽表單過長的問題) ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 🟢 依據規則動態產生表單
        for rule in self.rules:
            point_name = rule["point"]
            genders = rule["genders"]
            
            gb_title = f"【{point_name}】出賽名單" if point_name != "主賽" else "出賽名單"
            gb = QGroupBox(gb_title)
            gb.setStyleSheet("QGroupBox { font-weight: bold; }")
            gb_layout = QHBoxLayout(gb)
            
            # 隊伍 1 區塊
            vbox1 = QVBoxLayout()
            vbox1.addWidget(QLabel(f"🛡️ {self.team1.name}"))
            self.t1_cboxes[point_name] = []
            for g in genders:
                cb = QComboBox()
                cb.addItem(f"-- 請選擇選手 ({g}) --", None)
                # 性別過濾機制
                for ath in self.team1_athletes:
                    if ath.gender == g:
                        cb.addItem(f"{ath.name} ({ath.student_id})", ath.athlete_id)
                self.t1_cboxes[point_name].append(cb)
                vbox1.addWidget(cb)
            
            # 隊伍 2 區塊
            vbox2 = QVBoxLayout()
            vbox2.addWidget(QLabel(f"🛡️ {self.team2.name}"))
            self.t2_cboxes[point_name] = []
            for g in genders:
                cb = QComboBox()
                cb.addItem(f"-- 請選擇選手 ({g}) --", None)
                # 性別過濾機制
                for ath in self.team2_athletes:
                    if ath.gender == g:
                        cb.addItem(f"{ath.name} ({ath.student_id})", ath.athlete_id)
                self.t2_cboxes[point_name].append(cb)
                vbox2.addWidget(cb)
            
            gb_layout.addLayout(vbox1)
            gb_layout.addLayout(vbox2)
            scroll_layout.addWidget(gb)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # --- 3. 底部確認按鈕 ---
        btn_layout = QHBoxLayout()
        confirm_btn = QPushButton("✅ 確認檢錄並存檔")
        confirm_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px; font-weight: bold; font-size: 14px;")
        confirm_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addStretch()
        btn_layout.addWidget(confirm_btn)
        
        main_layout.addLayout(btn_layout)

    def validate_and_accept(self):
        """檢查選單合法性並整理資料"""
        lineups_data = []

        for rule in self.rules:
            point_name = rule["point"]
            
            # 取得該點選中的選手 ID
            t1_selected = [cb.currentData() for cb in self.t1_cboxes[point_name] if cb.currentData() is not None]
            t2_selected = [cb.currentData() for cb in self.t2_cboxes[point_name] if cb.currentData() is not None]

            # 防呆 1：確保該點的每個位置都有選人
            if len(t1_selected) < len(self.t1_cboxes[point_name]) or len(t2_selected) < len(self.t2_cboxes[point_name]):
                QMessageBox.warning(self, "錯誤", f"請完整選擇【{point_name}】雙方的出賽選手！")
                return

            # 防呆 2：同點雙打不能選同一個人 (不同點可重複出賽)
            if len(set(t1_selected)) != len(t1_selected) or len(set(t2_selected)) != len(t2_selected):
                QMessageBox.warning(self, "錯誤", f"【{point_name}】中，同一名選手不能自己跟自己搭檔！")
                return

            # 將資料組裝為寫入格式
            for athlete_id in t1_selected:
                lineups_data.append({'point_name': point_name, 'team_id': self.match.team1_id, 'athlete_id': athlete_id})
            for athlete_id in t2_selected:
                lineups_data.append({'point_name': point_name, 'team_id': self.match.team2_id, 'athlete_id': athlete_id})
            
        # 呼叫 DataManager 進行寫入
        try:
            self.dm.save_match_lineup(self.match.match_id, lineups_data)
            self.accept() 
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"名單寫入檔案失敗: {e}")