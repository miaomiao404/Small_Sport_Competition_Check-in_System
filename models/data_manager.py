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
    start_time: str
    end_time: str
    status: str
    remark: str

@dataclass
class Lineup:
    match_id: str
    team_id: str
    athlete_id: str

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
        self.lineups_file = os.path.join(self.data_dir, "lineups.csv")
        
        self.teams: Dict[str, Team] = {}
        self.athletes: Dict[str, Athlete] = {}
        self.matches: Dict[str, Match] = {}
        self.lineups: List[Lineup] = [] 
        
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
        if os.path.exists(self.teams_file):
            with open(self.teams_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    self.teams[row['team_id']] = Team(**row)

        if os.path.exists(self.athletes_file):
            with open(self.athletes_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    row['is_school_team'] = row['is_school_team'] == 'True'
                    self.athletes[row['athlete_id']] = Athlete(**row)
                    
        if os.path.exists(self.matches_file):
            with open(self.matches_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    self.matches[row['match_id']] = Match(**row)

        if os.path.exists(self.lineups_file):
            with open(self.lineups_file, mode='r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    self.lineups.append(Lineup(**row))

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

    def update_team(self, team_id: str, name: str):
        if team_id in self.teams:
            self.teams[team_id].name = name
            self._save_teams()

    def delete_team(self, team_id: str):
        if any(a.team_id == team_id for a in self.athletes.values()):
            raise ValueError("該隊伍仍有選手名單，無法直接刪除！請先移除旗下選手。")
        if any(m.team1_id == team_id or m.team2_id == team_id for m in self.matches.values()):
            raise ValueError("該隊伍已有排定賽程，無法刪除！")
            
        del self.teams[team_id]
        self._save_teams()

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

    def update_athlete(self, athlete_id: str, team_id: str, name: str, student_id: str, 
                       gender: str, grade: str, department: str, is_school_team: bool, remark: str):
        if athlete_id in self.athletes:
            a = self.athletes[athlete_id]
            a.team_id, a.name, a.student_id = team_id, name, student_id
            a.gender, a.grade, a.department = gender, grade, department
            a.is_school_team, a.remark = is_school_team, remark
            self._save_athletes()

    def delete_athlete(self, athlete_id: str):
        if hasattr(self, 'lineups') and any(l.athlete_id == athlete_id for l in self.lineups):
            raise ValueError("該選手已有檢錄出賽紀錄，為保留賽事歷史，無法刪除！")
            
        del self.athletes[athlete_id]
        self._save_athletes()

    def _save_athletes(self):
        data = []
        for athlete in self.athletes.values():
            row = asdict(athlete)
            row['is_school_team'] = str(row['is_school_team'])
            data.append(row)
        fieldnames = ["athlete_id", "team_id", "name", "student_id", "gender", "grade", "department", "is_school_team", "remark"]
        self._atomic_write_csv(self.athletes_file, fieldnames, data)
        
    # ==========================================
    # 賽事 (Match) CRUD
    # ==========================================
    def add_match(self, match_id: str, match_type: str, team1_id: str, team2_id: str,
                  court: str, start_time: str, end_time: str, status: str, remark: str):
        
        if match_id in self.matches:
            raise ValueError(f"賽事編號 {match_id} 已存在，請使用其他編號。")
            
        new_match = Match(match_id, match_type, team1_id, team2_id, court, start_time, end_time, status, remark)
        self.matches[match_id] = new_match
        self._save_matches()

    def _save_matches(self):
        fieldnames = ["match_id", "match_type", "team1_id", "team2_id", "court", 
                      "start_time", "end_time", "status", "remark"]
        self._atomic_write_csv(self.matches_file, fieldnames, [asdict(m) for m in self.matches.values()])

    # ==========================================
    # 檢錄名單 (Lineups) CRUD
    # ==========================================
    def save_match_lineup(self, match_id: str, lineups_data: List[dict]):
        self.lineups = [l for l in self.lineups if l.match_id != match_id]
        
        for data in lineups_data:
            self.lineups.append(Lineup(match_id=match_id, 
                                       team_id=data['team_id'], 
                                       athlete_id=data['athlete_id']))
            
        fieldnames = ["match_id", "team_id", "athlete_id"]
        self._atomic_write_csv(self.lineups_file, fieldnames, [asdict(l) for l in self.lineups])