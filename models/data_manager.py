import csv
import os
from dataclasses import dataclass, asdict
from typing import Dict, List

# ==========================================
# 資料模型 (Dataclasses)
# ==========================================
@dataclass
class Team:
    team_id: str
    name: str

@dataclass
class Athlete:
    athlete_id: str
    team_id: str
    name: str
    student_id: str
    gender: str
    grade: str
    department: str
    is_school_team: bool
    remark: str

@dataclass
class Match:
    match_id: str
    match_type: str
    team1_id: str
    team2_id: str
    court: str
    scheduled_time: str
    status: str
    remark: str

# ==========================================
# 資料管理引擎 (DataManager)
# ==========================================
class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.teams_file = os.path.join(self.data_dir, "teams.csv")
        self.athletes_file = os.path.join(self.data_dir, "athletes.csv")
        self.matches_file = os.path.join(self.data_dir, "matches.csv")
        
        # 記憶體快取 (Dictionary)
        self.teams: Dict[str, Team] = {}
        self.athletes: Dict[str, Athlete] = {}
        self.matches: Dict[str, Match] = {}
        
        # 啟動時載入資料
        self._load_all_data()

    def _atomic_write_csv(self, file_path: str, fieldnames: List[str], data_list: List[dict]):
        """原子寫入法，避免寫入一半崩潰導致檔案損毀"""
        temp_file = file_path + ".tmp"
        try:
            with open(temp_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
            os.replace(temp_file, file_path)
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"寫入檔案 {file_path} 失敗: {e}")
            raise e

    def _load_all_data(self):
        """從 CSV 載入資料到記憶體"""
        # 載入 Teams
        if os.path.exists(self.teams_file):
            with open(self.teams_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    self.teams[row['team_id']] = Team(**row)

        # 載入 Athletes
        if os.path.exists(self.athletes_file):
            with open(self.athletes_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    row['is_school_team'] = row['is_school_team'] == 'True'
                    self.athletes[row['athlete_id']] = Athlete(**row)
                    
        # 載入 Matches
        if os.path.exists(self.matches_file):
            with open(self.matches_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    self.matches[row['match_id']] = Match(**row)

    # ==========================================
    # 隊伍 (Team) CRUD
    # ==========================================
    def get_all_teams(self) -> List[Team]:
        return list(self.teams.values())

    def add_team(self, name: str) -> str:
        current_ids = [int(tid[1:]) for tid in self.teams.keys() if tid.startswith('T')]
        next_id = f"T{(max(current_ids) + 1 if current_ids else 1):03d}"
        
        self.teams[next_id] = Team(team_id=next_id, name=name)
        self._save_teams()
        return next_id

    def _save_teams(self):
        self._atomic_write_csv(self.teams_file, ["team_id", "name"], [asdict(t) for t in self.teams.values()])

    # ==========================================
    # 選手 (Athlete) CRUD
    # ==========================================
    def add_athlete(self, team_id: str, name: str, student_id: str, gender: str, 
                    grade: str, department: str, is_school_team: bool, remark: str) -> str:
        
        current_ids = [int(pid[1:]) for pid in self.athletes.keys() if pid.startswith('P')]
        next_id = f"P{(max(current_ids) + 1 if current_ids else 1):03d}"
        
        new_athlete = Athlete(next_id, team_id, name, student_id, gender, grade, department, is_school_team, remark)
        self.athletes[next_id] = new_athlete
        self._save_athletes()
        return next_id

    def _save_athletes(self):
        data = []
        for athlete in self.athletes.values():
            row = asdict(athlete)
            row['is_school_team'] = str(row['is_school_team'])
            data.append(row)
        fieldnames = ["athlete_id", "team_id", "name", "student_id", "gender", "grade", "department", "is_school_team", "remark"]
        self._atomic_write_csv(self.athletes_file, fieldnames, data)
        
    # ==========================================
    # 賽事 (Match) CRUD (預留框架)
    # ==========================================
    # 之後我們再補上新增 Match 的相關邏輯...