from PySide6.QtWidgets import (QMainWindow, QDialog, QMessageBox, QMenu, 
                               QListWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from models.data_manager import DataManager
from ui_py.teamlist import Ui_MainWindow as Ui_TeamList
from ui_py.addteam import Ui_add_team_dialog
from ui_py.addathlete import Ui_add_athlete_dialog

class TeamController:
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager
        
        self.window = QMainWindow()
        self.ui = Ui_TeamList()
        self.ui.setupUi(self.window)
        
        self._setup_native_widgets()
        self._setup_context_menus()
        self._refresh_team_list()

    def show(self):
        self._refresh_team_list()
        self.window.show()

    # ==========================================
    # 1. 動態替換為標準資料表元件 (關鍵技巧)
    # ==========================================
    def _setup_native_widgets(self):
        # 隱藏原本的 QGraphicsView
        self.ui.team_list_view.hide()
        self.ui.athlete_list_view.hide()

        # 建立左側：隊伍清單 (QListWidget)
        self.team_list_widget = QListWidget()
        self.team_list_widget.setStyleSheet("font-size: 16px; padding: 5px;")
        self.ui.verticalLayout.addWidget(self.team_list_widget)
        # 綁定選擇事件：點擊隊伍時更新右側
        self.team_list_widget.itemSelectionChanged.connect(self._on_team_selected)

        # 建立右側：選手資料表 (QTableWidget)
        self.athlete_table = QTableWidget()
        self.athlete_table.setColumnCount(6)
        self.athlete_table.setHorizontalHeaderLabels(["姓名", "學號", "性別", "系所/年級", "校隊", "備註"])
        self.athlete_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # 整列選取
        self.athlete_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # 禁止直接在表上修改文字
        self.athlete_table.horizontalHeader().setStretchLastSection(True) # 備註欄自動填滿
        self.ui.verticalLayout_2.addWidget(self.athlete_table)

    # ==========================================
    # 2. 右鍵選單邏輯
    # ==========================================
    def _setup_context_menus(self):
        self.team_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.team_list_widget.customContextMenuRequested.connect(self.show_team_menu)

        self.athlete_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.athlete_table.customContextMenuRequested.connect(self.show_athlete_menu)

    def show_team_menu(self, pos):
        menu = QMenu()
        item = self.team_list_widget.itemAt(pos)
        
        add_action = QAction("➕ 新增隊伍", self.window)
        add_action.triggered.connect(lambda: self.open_team_dialog(edit_id=None))
        menu.addAction(add_action)

        if item:
            # 取出隱藏在 item 裡的 team_id
            team_id = item.data(Qt.ItemDataRole.UserRole)
            menu.addSeparator()
            
            edit_action = QAction("✏️ 編輯隊伍", self.window)
            edit_action.triggered.connect(lambda: self.open_team_dialog(edit_id=team_id))
            menu.addAction(edit_action)
            
            delete_action = QAction("❌ 刪除隊伍", self.window)
            delete_action.triggered.connect(lambda: self.delete_team(team_id))
            menu.addAction(delete_action)
            
        menu.exec(self.team_list_widget.mapToGlobal(pos))

    def show_athlete_menu(self, pos):
        menu = QMenu()
        item = self.athlete_table.itemAt(pos)
        
        # 必須有選取隊伍才能新增選手
        current_team_item = self.team_list_widget.currentItem()
        if current_team_item:
            add_action = QAction("➕ 新增選手", self.window)
            add_action.triggered.connect(lambda: self.open_athlete_dialog(edit_id=None))
            menu.addAction(add_action)

        if item:
            # 取出隱藏在第一欄(姓名)裡的 athlete_id
            row = item.row()
            athlete_id = self.athlete_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            menu.addSeparator()
            
            edit_action = QAction("✏️ 編輯選手", self.window)
            edit_action.triggered.connect(lambda: self.open_athlete_dialog(edit_id=athlete_id))
            menu.addAction(edit_action)
            
            delete_action = QAction("❌ 刪除選手", self.window)
            delete_action.triggered.connect(lambda: self.delete_athlete(athlete_id))
            menu.addAction(delete_action)
            
        menu.exec(self.athlete_table.mapToGlobal(pos))

    # ==========================================
    # 3. 畫面刷新與過濾聯動
    # ==========================================
    def _refresh_team_list(self):
        """刷新左側隊伍清單"""
        # 紀錄當前選取的隊伍 ID，刷新後嘗試恢復選取
        current_item = self.team_list_widget.currentItem()
        selected_id = current_item.data(Qt.ItemDataRole.UserRole) if current_item else None

        self.team_list_widget.clear()
        
        for team in self.dm.get_all_teams():
            item = QListWidgetItem(team.name)
            item.setData(Qt.ItemDataRole.UserRole, team.team_id) # 隱藏 ID
            self.team_list_widget.addItem(item)
            
            if team.team_id == selected_id:
                item.setSelected(True)
                self.team_list_widget.setCurrentItem(item)

        # 如果沒有隊伍被選中，清空右側
        if not self.team_list_widget.currentItem():
            self.athlete_table.setRowCount(0)

    def _on_team_selected(self):
        """左側點擊時，更新右側選手表"""
        current_item = self.team_list_widget.currentItem()
        if not current_item:
            return
            
        team_id = current_item.data(Qt.ItemDataRole.UserRole)
        # 過濾出該隊的選手
        team_athletes = [a for a in self.dm.athletes.values() if a.team_id == team_id]
        
        self.athlete_table.setRowCount(len(team_athletes))
        for row, ath in enumerate(team_athletes):
            # 建立表格項目並填入資料
            name_item = QTableWidgetItem(ath.name)
            name_item.setData(Qt.ItemDataRole.UserRole, ath.athlete_id) # 隱藏 ID 於第一欄
            
            self.athlete_table.setItem(row, 0, name_item)
            self.athlete_table.setItem(row, 1, QTableWidgetItem(ath.student_id))
            self.athlete_table.setItem(row, 2, QTableWidgetItem(ath.gender))
            self.athlete_table.setItem(row, 3, QTableWidgetItem(f"{ath.department} ({ath.grade})"))
            self.athlete_table.setItem(row, 4, QTableWidgetItem("是" if ath.is_school_team else "否"))
            self.athlete_table.setItem(row, 5, QTableWidgetItem(ath.remark))

    # ==========================================
    # 4. 新增/編輯 對話框邏輯
    # ==========================================
    def open_team_dialog(self, edit_id=None):
        dialog = QDialog()
        ui = Ui_add_team_dialog()
        ui.setupUi(dialog)

        # 若為編輯模式，帶入原數值
        if edit_id:
            dialog.setWindowTitle("編輯隊伍")
            ui.team_name_edit.setText(self.dm.teams[edit_id].name)

        if dialog.exec() == QDialog.Accepted:
            name = ui.team_name_edit.text().strip()
            if not name:
                QMessageBox.warning(self.window, "錯誤", "隊伍名稱不能為空！")
                return
            try:
                if edit_id:
                    self.dm.update_team(edit_id, name)
                else:
                    self.dm.add_team(name)
                self._refresh_team_list()
            except Exception as e:
                QMessageBox.critical(self.window, "錯誤", f"操作失敗: {e}")

    def open_athlete_dialog(self, edit_id=None):
        dialog = QDialog()
        ui = Ui_add_athlete_dialog()
        ui.setupUi(dialog)

        teams = self.dm.get_all_teams()
        for team in teams:
            ui.team_cbox.addItem(team.name, userData=team.team_id)

        # 預設選中目前在左側列表選擇的隊伍
        current_team_item = self.team_list_widget.currentItem()
        if current_team_item:
            current_team_id = current_team_item.data(Qt.ItemDataRole.UserRole)
            index = ui.team_cbox.findData(current_team_id)
            if index >= 0:
                ui.team_cbox.setCurrentIndex(index)

        # 若為編輯模式，帶入原數值
        if edit_id:
            dialog.setWindowTitle("編輯選手")
            ath = self.dm.athletes[edit_id]
            ui.name_edit.setText(ath.name)
            ui.school_num_edit.setText(ath.student_id)
            ui.department_edit.setText(ath.department)
            ui.remark_edit.setText(ath.remark)
            
            # 設定下拉選單數值
            ui.team_cbox.setCurrentIndex(ui.team_cbox.findData(ath.team_id))
            ui.gender_cbox.setCurrentText(ath.gender)
            ui.grade_cbox.setCurrentText(ath.grade)
            ui.school_team_cbox.setCurrentText("是" if ath.is_school_team else "否")

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
                QMessageBox.warning(self.window, "錯誤", "姓名與學號為必填！")
                return

            try:
                if edit_id:
                    self.dm.update_athlete(edit_id, team_id, name, student_id, gender, grade, department, is_school_team, remark)
                else:
                    self.dm.add_athlete(team_id, name, student_id, gender, grade, department, is_school_team, remark)
                
                # 重新觸發左側點擊事件，以刷新右側表格
                self._on_team_selected()
            except Exception as e:
                QMessageBox.critical(self.window, "錯誤", f"操作失敗: {e}")

    # ==========================================
    # 5. 刪除邏輯 (附帶警告與阻擋)
    # ==========================================
    def delete_team(self, team_id: str):
        team_name = self.dm.teams[team_id].name
        reply = QMessageBox.warning(self.window, "確認刪除", 
                                    f"確定要刪除隊伍「{team_name}」嗎？",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.dm.delete_team(team_id)
                self._refresh_team_list()
            except ValueError as ve:
                QMessageBox.warning(self.window, "無法刪除", str(ve))

    def delete_athlete(self, athlete_id: str):
        ath_name = self.dm.athletes[athlete_id].name
        reply = QMessageBox.warning(self.window, "確認刪除", 
                                    f"確定要刪除選手「{ath_name}」嗎？",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.dm.delete_athlete(athlete_id)
                self._on_team_selected() # 刷新表格
            except ValueError as ve:
                QMessageBox.warning(self.window, "無法刪除", str(ve))