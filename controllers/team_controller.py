from PySide6.QtWidgets import (QMainWindow, QDialog, QMessageBox, QMenu, 
                               QGraphicsScene, QGraphicsTextItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from models.data_manager import DataManager
from ui_py.teamlist import Ui_MainWindow as Ui_TeamList
from ui_py.addteam import Ui_add_team_dialog
from ui_py.addathlete import Ui_add_athlete_dialog

class TeamController:
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager
        
        # 初始化隊伍名單視窗
        self.window = QMainWindow()
        self.ui = Ui_TeamList()
        self.ui.setupUi(self.window)
        
        self.team_scene = QGraphicsScene()
        self.ui.team_list_view.setScene(self.team_scene)
        
        self.athlete_scene = QGraphicsScene()
        self.ui.athlete_list_view.setScene(self.athlete_scene)
        
        # 綁定右鍵選單
        self._setup_context_menus()
        
        self._refresh_team_view()

    def show(self):
        self.window.show()

    # ==========================================
    # 介面設定與事件綁定
    # ==========================================
    def _setup_context_menus(self):
        # 開啟自訂選單政策
        self.ui.team_list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.team_list_view.customContextMenuRequested.connect(self.show_team_menu)

        self.ui.athlete_list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.athlete_list_view.customContextMenuRequested.connect(self.show_athlete_menu)

    def show_team_menu(self, pos):
        menu = QMenu()
        add_action = QAction("新增隊伍", self.window)
        add_action.triggered.connect(self.open_add_team_dialog)
        menu.addAction(add_action)
        
        # 將相對座標轉換為全域座標顯示選單
        menu.exec_(self.ui.team_list_view.mapToGlobal(pos))

    def show_athlete_menu(self, pos):
        menu = QMenu()
        add_action = QAction("新增選手", self.window)
        add_action.triggered.connect(self.open_add_athlete_dialog)
        menu.addAction(add_action)
        menu.exec_(self.ui.athlete_list_view.mapToGlobal(pos))

    # ==========================================
    # 對話框邏輯 (Dialogs)
    # ==========================================
    def open_add_team_dialog(self):
        dialog = QDialog()
        ui = Ui_add_team_dialog()
        ui.setupUi(dialog)

        if dialog.exec() == QDialog.Accepted:
            team_name = ui.team_name_edit.text().strip()
            if not team_name:
                QMessageBox.warning(self.window, "錯誤", "隊伍名稱不能為空！")
                return
            try:
                self.dm.add_team(team_name)
                self._refresh_team_view()
                QMessageBox.information(self.window, "成功", f"隊伍「{team_name}」已新增。")
            except Exception as e:
                QMessageBox.critical(self.window, "錯誤", f"寫入失敗: {e}")

    def open_add_athlete_dialog(self):
        teams = self.dm.get_all_teams()
        if not teams:
            QMessageBox.warning(self.window, "提示", "請先點擊左側右鍵建立至少一支隊伍，才能新增選手。")
            return

        dialog = QDialog()
        ui = Ui_add_athlete_dialog()
        ui.setupUi(dialog)

        # 動態載入隊伍到下拉選單
        for team in teams:
            ui.team_cbox.addItem(team.name, userData=team.team_id)

        if dialog.exec() == QDialog.Accepted:
            team_id = ui.team_cbox.currentData()
            name = ui.name_edit.text().strip()
            student_id = ui.school_num_edit.text().strip()
            gender = ui.gender_cbox.currentText()
            grade = ui.grade_cbox.currentText()
            department = ui.department_edit.text().strip()
            is_school_team = (ui.school_team_cbox.currentText() == "是")
            remark = ui.remark_edit.text().strip()

            if not name or not student_id:
                QMessageBox.warning(self.window, "錯誤", "姓名與學號為必填欄位！")
                return

            try:
                self.dm.add_athlete(team_id, name, student_id, gender, grade, department, is_school_team, remark)
                self._refresh_athlete_view()
                QMessageBox.information(self.window, "成功", f"選手「{name}」已新增。")
            except Exception as e:
                QMessageBox.critical(self.window, "錯誤", f"寫入失敗: {e}")

    # ==========================================
    # 畫面更新邏輯 (View Refresh)
    # ==========================================
    def _refresh_team_view(self):
        self.team_scene.clear()
        y_offset = 0
        for team in self.dm.get_all_teams():
            text_item = QGraphicsTextItem(f"[{team.team_id}] {team.name}")
            text_item.setPos(10, y_offset)
            self.team_scene.addItem(text_item)
            y_offset += 25

    def _refresh_athlete_view(self):
        self.athlete_scene.clear()
        y_offset = 0
        # 暫時列出所有選手
        for athlete in self.dm.athletes.values():
            team_name = self.dm.teams[athlete.team_id].name if athlete.team_id in self.dm.teams else "未知"
            text_item = QGraphicsTextItem(f"{athlete.name} ({athlete.student_id}) - {team_name} / {athlete.department}")
            text_item.setPos(10, y_offset)
            self.athlete_scene.addItem(text_item)
            y_offset += 25