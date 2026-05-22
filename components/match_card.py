import datetime
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

UPCOMING_MINUTES = 60
PREP_MINUTES = 10

class MatchCardWidget(QFrame):
    # 定義自訂信號，當按鈕被點擊時，會將自己的 match_id 傳送出去給 Controller
    checkin_clicked = Signal(str)
    start_clicked = Signal(str)
    finish_clicked = Signal(str)

    def __init__(self, match_id: str, court: str, stage: str, team1_name: str, 
                 team2_name: str, match_rule: str, start_time: str, end_time: str, status: str):
        super().__init__()
        self.match_id = match_id
        self.court = court
        self.stage = stage
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.match_rule = match_rule
        self.start_time = start_time
        self.end_time = end_time
        self.status = status 

        self.init_ui()
        
    def init_ui(self):
        # 稍微增加卡片高度以容納按鈕
        self.setFixedSize(220, 290) 
        self.setObjectName("MatchCard")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- 1. 頂部標題列 (與先前相同) ---
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        self.id_label = QLabel(self.match_id)
        self.id_label.setStyleSheet("color: white; background-color: #2b2b2b; padding: 5px; font-weight: bold; font-size: 16px;")
        self.id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.court_label = QLabel(f"場地 {self.court}")
        self.court_label.setStyleSheet("color: black; background-color: white; padding: 5px; font-weight: bold; font-size: 16px;")
        self.court_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(self.id_label, 1)
        header_layout.addWidget(self.court_label, 1)
        
        # --- 2. 主資訊區 (與先前相同) ---
        body_widget = QWidget()
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(10, 5, 10, 5)
        
        stage_label = QLabel(self.stage)
        stage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        team1_label = QLabel(self.team1_name)
        team1_label.setFont(QFont("Arial", 16, QFont.Bold))
        team1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        vs_label = QLabel("vs")
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        team2_label = QLabel(self.team2_name)
        team2_label.setFont(QFont("Arial", 16, QFont.Bold))
        team2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        rule_label = QLabel(self.match_rule)
        rule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        start_hm = self.start_time.split(" ")[1] if " " in self.start_time else self.start_time
        end_hm = self.end_time.split(" ")[1] if " " in self.end_time else self.end_time
        time_label = QLabel(f"{start_hm} - {end_hm}")
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("color: #555555; font-size: 12px;")
        
        body_layout.addWidget(stage_label)
        body_layout.addWidget(team1_label)
        body_layout.addWidget(vs_label)
        body_layout.addWidget(team2_label)
        body_layout.addWidget(rule_label)
        body_layout.addWidget(time_label)
        
        # --- 3. 底部操作按鈕區 (新增) ---
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(10, 5, 10, 10)
        
        self.btn_checkin = QPushButton("📝 檢錄")
        self.btn_start = QPushButton("▶️ 開始賽事")
        self.btn_finish = QPushButton("⏹️ 結束賽事")
        
        self.btn_checkin.setStyleSheet("background-color: #007bff; color: white; padding: 5px;")
        self.btn_start.setStyleSheet("background-color: #28a745; color: white; padding: 5px;")
        self.btn_finish.setStyleSheet("background-color: #dc3545; color: white; padding: 5px;")
        
        # 綁定按鈕點擊事件，發射帶有 ID 的信號
        self.btn_checkin.clicked.connect(lambda: self.checkin_clicked.emit(self.match_id))
        self.btn_start.clicked.connect(lambda: self.start_clicked.emit(self.match_id))
        self.btn_finish.clicked.connect(lambda: self.finish_clicked.emit(self.match_id))
        
        btn_layout.addWidget(self.btn_checkin)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_finish)
        
        main_layout.addWidget(header_widget)
        main_layout.addWidget(body_widget)
        main_layout.addWidget(btn_widget)
        
        self._apply_border("black", False)
        self._update_button_visibility()

    def _apply_border(self, color: str, is_transparent: bool):
        border_color = "transparent" if is_transparent else color
        self.setStyleSheet(f"#MatchCard {{ border: 4px solid {border_color}; background-color: white; }}")

    def _update_button_visibility(self):
        """根據賽事狀態，顯示或隱藏對應的操作按鈕"""
        self.btn_checkin.setVisible(self.status == "upcoming")
        self.btn_start.setVisible(self.status == "checked_in")
        self.btn_finish.setVisible(self.status == "in_progress")

    def update_state(self, current_dt: datetime.datetime, flash_1s_on: bool, flash_2s_on: bool):
        # 每次更新狀態時，確保按鈕的顯示邏輯也是最新的
        self._update_button_visibility()
        
        fmt = "%Y-%m-%d %H:%M"
        try:
            start_dt = datetime.datetime.strptime(self.start_time, fmt)
            end_dt = datetime.datetime.strptime(self.end_time, fmt)
        except ValueError:
            self._apply_border("black", False)
            return

        diff_start_mins = (start_dt - current_dt).total_seconds() / 60.0
        diff_end_mins = (end_dt - current_dt).total_seconds() / 60.0

        if self.status == "in_progress":
            if diff_end_mins <= 0:
                self._apply_border("#28a745", not flash_2s_on)
            else:
                self._apply_border("#28a745", False)
        elif self.status == "checked_in":
            self._apply_border("#ffc107", False)
        elif self.status == "upcoming":
            if diff_start_mins <= 0:
                self._apply_border("#dc3545", not flash_1s_on)
            elif diff_start_mins <= PREP_MINUTES:
                self._apply_border("#dc3545", not flash_2s_on)
            elif diff_start_mins <= UPCOMING_MINUTES:
                self._apply_border("#dc3545", False)
            else:
                self._apply_border("black", False)
        else:
            self._apply_border("black", False)