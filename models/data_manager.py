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
    match_category: str
    win_games: int
    points_per_game: int
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
    point_name: str
    team_id: str
    athlete_id: str

@dataclass
class Score:
    match_id: str
    point_name: str    # 記錄如 "主賽", "男單", "女單" 等點數名稱
    game_index: int    # 第幾局 (1, 2, 3...)
    team1_score: int
    team2_score: int

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
        self.scores_file = os.path.join(self.data_dir, "scores.csv")
        
        self.teams: Dict[str, Team] = {}
        self.athletes: Dict[str, Athlete] = {}
        self.matches: Dict[str, Match] = {}
        self.lineups: List[Lineup] = [] 
        self.scores: List[Score] = []
        
        self._load_all_data()

    def _atomic_write_csv(self, file_path: str, fieldnames: List[str], data_list: List[dict]):
        """原子寫入法，避免寫入一半崩潰導致檔案損毀"""
        temp_file = file_path + ".tmp"
        try:
            # 💡 修正 1：寫入時使用 utf-8-sig 加上 BOM，解決 Excel 中文亂碼與跑版問題
            with open(temp_file, mode='w', newline='', encoding='utf-8-sig') as f:
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
            with open(self.teams_file, mode='r', encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    self.teams[row['team_id']] = Team(**row)

        if os.path.exists(self.athletes_file):
            with open(self.athletes_file, mode='r', encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    row['is_school_team'] = row['is_school_team'] == 'True'
                    self.athletes[row['athlete_id']] = Athlete(**row)
                    
        if os.path.exists(self.matches_file):
            with open(self.matches_file, mode='r', encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    row['win_games'] = int(row['win_games'])
                    row['points_per_game'] = int(row['points_per_game'])
                    self.matches[row['match_id']] = Match(**row)

        if os.path.exists(self.lineups_file):
            with open(self.lineups_file, mode='r', encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    if 'point_name' not in row:
                        row['point_name'] = '主賽'
                    self.lineups.append(Lineup(**row))

        if os.path.exists(self.scores_file):
            with open(self.scores_file, mode='r', encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    row['game_index'] = int(row['game_index'])
                    row['team1_score'] = int(row['team1_score'])
                    row['team2_score'] = int(row['team2_score'])
                    self.scores.append(Score(**row))

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
    def add_match(self, match_id: str, match_category: str, win_games: int, points_per_game: int,
                  team1_id: str, team2_id: str, court: str, start_time: str, end_time: str, status: str, remark: str):
        
        if match_id in self.matches:
            raise ValueError(f"賽事編號 {match_id} 已存在，請使用其他編號。")
            
        new_match = Match(match_id, match_category, win_games, points_per_game, team1_id, team2_id, court, start_time, end_time, status, remark)
        self.matches[match_id] = new_match
        self._save_matches()

    def _save_matches(self):
        fieldnames = ["match_id", "match_category", "win_games", "points_per_game", 
                      "team1_id", "team2_id", "court", "start_time", "end_time", "status", "remark"]
        self._atomic_write_csv(self.matches_file, fieldnames, [asdict(m) for m in self.matches.values()])

    # ==========================================
    # 檢錄名單 (Lineups) CRUD
    # ==========================================
    def save_match_lineup(self, match_id: str, lineups_data: List[dict]):
        self.lineups = [l for l in self.lineups if l.match_id != match_id]
        
        for data in lineups_data:
            self.lineups.append(Lineup(match_id=match_id, 
                                       point_name=data['point_name'], # 🟢 新增
                                       team_id=data['team_id'], 
                                       athlete_id=data['athlete_id']))
            
        fieldnames = ["match_id", "point_name", "team_id", "athlete_id"] # 🟢 新增欄位
        self._atomic_write_csv(self.lineups_file, fieldnames, [asdict(l) for l in self.lineups])

    # ==========================================
    # 比分紀錄 (Scores) CRUD
    # ==========================================
    def save_match_scores(self, match_id: str, scores_data: List[dict]):
        """
        儲存特定賽事的比分。
        scores_data 格式: [{'point_name': '男單', 'game_index': 1, 'team1_score': 21, 'team2_score': 19}, ...]
        """
        # 移除舊有該場賽事的比分
        self.scores = [s for s in self.scores if s.match_id != match_id]
        
        # 寫入新比分
        for data in scores_data:
            self.scores.append(Score(
                match_id=match_id,
                point_name=data['point_name'],
                game_index=data['game_index'],
                team1_score=data['team1_score'],
                team2_score=data['team2_score']
            ))
            
        fieldnames = ["match_id", "point_name", "game_index", "team1_score", "team2_score"]
        self._atomic_write_csv(self.scores_file, fieldnames, [asdict(s) for s in self.scores])

    def get_match_scores(self, match_id: str) -> List[Score]:
        """取得特定賽事的所有比分紀錄"""
        return [s for s in self.scores if s.match_id == match_id]
    
    def get_match_winner(self, match_id: str) -> int:
        """
        根據目前記錄的分數，自動判定獲勝隊伍。
        回傳: 0 (無/未結束), 1 (隊伍1獲勝), 2 (隊伍2獲勝)
        """
        match = self.matches.get(match_id)
        scores = self.get_match_scores(match_id)
        if not match or not scores:
            return 0

        # 將分數依照點數 (point_name) 進行分組
        point_scores = {}
        for s in scores:
            if s.point_name not in point_scores:
                point_scores[s.point_name] = []
            point_scores[s.point_name].append(s)

        team1_points_won = 0
        team2_points_won = 0

        # 計算每個「點」是誰獲勝
        for point_name, games in point_scores.items():
            t1_game_wins = sum(1 for g in games if g.team1_score > g.team2_score)
            t2_game_wins = sum(1 for g in games if g.team2_score > g.team1_score)
            
            if t1_game_wins >= match.win_games:
                team1_points_won += 1
            elif t2_game_wins >= match.win_games:
                team2_points_won += 1

        # 判定總體賽事獲勝者
        if "團體" in match.match_category:
            # 團體賽五點搶三勝
            if team1_points_won >= 3:
                return 1
            elif team2_points_won >= 3:
                return 2
        else:
            # 個人賽贏下該點即獲勝
            if team1_points_won > 0:
                return 1
            elif team2_points_won > 0:
                return 2
                
        return 0