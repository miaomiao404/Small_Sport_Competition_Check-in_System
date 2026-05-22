from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QMessageBox, QTabWidget, QWidget, QSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from models.data_manager import DataManager

class ScoreDialog(QDialog):
    def __init__(self, dm: DataManager, match_id: str, parent=None):
        super().__init__(parent)
        self.dm = dm
        self.match = self.dm.matches[match_id]
        self.team1 = self.dm.teams.get(self.match.team1_id)
        self.team2 = self.dm.teams.get(self.match.team2_id)
        
        # 取得已儲存的分數
        self.existing_scores = self.dm.get_match_scores(match_id)
        
        # 計算最大局數 (例如 三戰兩勝 -> 3局)
        self.max_games = (self.match.win_games * 2) - 1
        
        # 判定是否為團體賽 (定義點數名稱)
        self.is_team_match = "團體" in self.match.match_category
        self.point_names = ["男單", "女單", "男雙", "女雙", "混雙"] if self.is_team_match else ["主賽"]

        # 儲存 SpinBox 的參照以便後續取值: dict[point_name][game_index] = (spin1, spin2)
        self.score_inputs = {}

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"賽事計分 - {self.match.match_id}")
        self.setMinimumWidth(450)
        main_layout = QVBoxLayout(self)

        # 頂部資訊
        info_font = QFont("Arial", 12, QFont.Bold)
        info_label = QLabel(f"{self.team1.name} vs {self.team2.name}")
        info_label.setFont(info_font)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(info_label)

        # 建立分頁元件 (個人賽只有 1 頁，團體賽有 5 頁)
        self.tab_widget = QTabWidget()
        
        for point_name in self.point_names:
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            self.score_inputs[point_name] = {}
            
            # 產生對應局數的輸入框
            for g_idx in range(1, self.max_games + 1):
                row_layout = QHBoxLayout()
                
                game_label = QLabel(f"第 {g_idx} 局:")
                game_label.setFixedWidth(60)
                
                # 隊伍1 分數輸入
                spin1 = QSpinBox()
                spin1.setRange(0, 99)
                spin1.setStyleSheet("font-size: 16px; padding: 5px;")
                
                vs_label = QLabel(" - ")
                vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # 隊伍2 分數輸入
                spin2 = QSpinBox()
                spin2.setRange(0, 99)
                spin2.setStyleSheet("font-size: 16px; padding: 5px;")

                # 若有舊資料，則預先填入
                old_score = next((s for s in self.existing_scores if s.point_name == point_name and s.game_index == g_idx), None)
                if old_score:
                    spin1.setValue(old_score.team1_score)
                    spin2.setValue(old_score.team2_score)

                row_layout.addWidget(game_label)
                row_layout.addWidget(spin1)
                row_layout.addWidget(vs_label)
                row_layout.addWidget(spin2)
                
                self.score_inputs[point_name][g_idx] = (spin1, spin2)
                tab_layout.addLayout(row_layout)
                
            tab_layout.addStretch()
            self.tab_widget.addTab(tab, point_name)
            
        main_layout.addWidget(self.tab_widget)

        # 底部按鈕
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 儲存比分")
        save_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; font-weight: bold;")
        save_btn.clicked.connect(self.validate_and_save)
        
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        main_layout.addLayout(btn_layout)

    def validate_and_save(self):
        """簡單合理性檢查與儲存"""
        scores_data = []
        target_score = self.match.points_per_game

        for point_name in self.point_names:
            for g_idx in range(1, self.max_games + 1):
                s1, s2 = self.score_inputs[point_name][g_idx]
                val1 = s1.value()
                val2 = s2.value()
                
                # 若雙方皆為 0，視為尚未進行該局，跳過不存
                if val1 == 0 and val2 == 0:
                    continue
                    
                # 簡單合理性檢查：如果有人贏了該局，分數差至少要 2，且最高分必須大於等於目標分數
                if val1 >= target_score or val2 >= target_score:
                    if abs(val1 - val2) < 2 and val1 != 30 and val2 != 30: # 假設 30 分為羽球 Deuce 上限
                        reply = QMessageBox.warning(
                            self, "分數警告", 
                            f"【{point_name} - 第 {g_idx} 局】\n分數為 {val1}:{val2}。\n羽球規則中，達標後須領先 2 分才算勝出。\n您確定要強制儲存這個比分嗎？",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply == QMessageBox.StandardButton.No:
                            return

                scores_data.append({
                    'point_name': point_name,
                    'game_index': g_idx,
                    'team1_score': val1,
                    'team2_score': val2
                })

        try:
            self.dm.save_match_scores(self.match.match_id, scores_data)
            QMessageBox.information(self, "成功", "比分已儲存！")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"儲存失敗: {e}")