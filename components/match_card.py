import datetime
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# 將時間設定宣告為常數，方便未來讀取設定檔或手動修改
UPCOMING_MINUTES = 60
PREP_MINUTES = 10

class MatchCardWidget(QFrame):
    def __init__(self, match_id: str, court: str, stage: str, team1_name: str, 
                 team2_name: str, match_rule: str, start_time: str, end_time: str, status: str):
        super().__init__()
        # 儲存賽事資料
        self.match_id = match_id
        self.court = court
        self.stage = stage
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.match_rule = match_rule
        self.start_time = start_time
        self.end_time = end_time
        self.status = status # 預期為: "upcoming", "checked_in", "in_progress", "finished"

        self.init_ui()
        
    def init_ui(self):
        # 設定卡片固定尺寸，確保畫面整齊
        self.setFixedSize(220, 260) 
        self.setObjectName("MatchCard")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==========================================
        # 1. 頂部標題列 (Header)
        # ==========================================
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # 左側 Match ID (深底白字)
        self.id_label = QLabel(self.match_id)
        self.id_label.setStyleSheet("color: white; background-color: #2b2b2b; padding: 5px; font-weight: bold; font-size: 16px;")
        self.id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 右側 場地 (白底黑字)
        self.court_label = QLabel(f"場地 {self.court}")
        self.court_label.setStyleSheet("color: black; background-color: white; padding: 5px; font-weight: bold; font-size: 16px;")
        self.court_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(self.id_label, 1)
        header_layout.addWidget(self.court_label, 1)
        
        # ==========================================
        # 2. 主資訊區 (Body)
        # ==========================================
        body_widget = QWidget()
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        stage_label = QLabel(self.stage)
        stage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        team1_label = QLabel(self.team1_name)
        team1_label.setFont(QFont("Arial", 18, QFont.Bold))
        team1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        vs_label = QLabel("vs")
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        team2_label = QLabel(self.team2_name)
        team2_label.setFont(QFont("Arial", 18, QFont.Bold))
        team2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        rule_label = QLabel(self.match_rule)
        rule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 擷取時間字串中的 HH:mm 部分 (假設傳入格式為 YYYY-MM-DD HH:mm)
        start_hm = self.start_time.split(" ")[1] if " " in self.start_time else self.start_time
        end_hm = self.end_time.split(" ")[1] if " " in self.end_time else self.end_time
        time_label = QLabel(f"{start_hm} - {end_hm}")
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("color: #555555; font-size: 12px; margin-top: 5px;")
        
        body_layout.addWidget(stage_label)
        body_layout.addWidget(team1_label)
        body_layout.addWidget(vs_label)
        body_layout.addWidget(team2_label)
        body_layout.addWidget(rule_label)
        body_layout.addWidget(time_label)
        
        main_layout.addWidget(header_widget)
        main_layout.addWidget(body_widget)
        
        # 預設黑框
        self._apply_border("black", False)

    # ==========================================
    # 3. 狀態與閃爍邏輯 (State Machine)
    # ==========================================
    def _apply_border(self, color: str, is_transparent: bool):
        """套用 QSS 外框樣式。若 is_transparent 為 True，則外框隱藏以製造閃爍感"""
        border_color = "transparent" if is_transparent else color
        # 利用 QSS 控制邊框與底色
        self.setStyleSheet(f"""
            #MatchCard {{
                border: 4px solid {border_color};
                background-color: white;
            }}
        """)

    def update_state(self, current_dt: datetime.datetime, flash_1s_on: bool, flash_2s_on: bool):
        """
        由 MainController 的心跳定時呼叫。
        根據本機時間與賽程時間的差距，決定邊框顏色與是否要隱藏(閃爍)。
        """
        fmt = "%Y-%m-%d %H:%M"
        try:
            start_dt = datetime.datetime.strptime(self.start_time, fmt)
            end_dt = datetime.datetime.strptime(self.end_time, fmt)
        except ValueError:
            self._apply_border("black", False)
            return

        # 計算時間差 (分鐘)
        diff_start_mins = (start_dt - current_dt).total_seconds() / 60.0
        diff_end_mins = (end_dt - current_dt).total_seconds() / 60.0

        if self.status == "in_progress":
            if diff_end_mins <= 0:
                # 進行中 (超時) -> 綠色外框 + 2秒閃爍
                self._apply_border("#28a745", not flash_2s_on)
            else:
                # 進行中 (正常) -> 綠色外框常亮
                self._apply_border("#28a745", False)
                
        elif self.status == "checked_in":
            # 準備進行 (檢錄完畢) -> 黃色外框常亮
            self._apply_border("#ffc107", False)
            
        elif self.status == "upcoming":
            if diff_start_mins <= 0:
                # 準備進行 (逾時未檢錄) -> 紅色外框 + 1秒閃爍
                self._apply_border("#dc3545", not flash_1s_on)
            elif diff_start_mins <= PREP_MINUTES:
                # 準備進行 (未檢錄) -> 紅色外框 + 2秒閃爍
                self._apply_border("#dc3545", not flash_2s_on)
            elif diff_start_mins <= UPCOMING_MINUTES:
                # 即將開始 -> 紅色外框常亮
                self._apply_border("#dc3545", False)
            else:
                # 超過設定的準備時間 (例如 1 小時後) -> 普通黑框
                self._apply_border("black", False)
        else:
            # 已結束 (finished) 或其他 -> 普通黑框
            self._apply_border("black", False)