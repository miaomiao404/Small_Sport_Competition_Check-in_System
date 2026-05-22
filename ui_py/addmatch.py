# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addmatch.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateTimeEdit,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_court_court_edit(object):
    def setupUi(self, court_court_edit):
        if not court_court_edit.objectName():
            court_court_edit.setObjectName(u"court_court_edit")
        court_court_edit.resize(400, 361)
        self.verticalLayout = QVBoxLayout(court_court_edit)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.add_athlete_f = QFrame(court_court_edit)
        self.add_athlete_f.setObjectName(u"add_athlete_f")
        self.add_athlete_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_athlete_f.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.add_athlete_f)
        self.gridLayout.setObjectName(u"gridLayout")
        self.match_type_l_2 = QLabel(self.add_athlete_f)
        self.match_type_l_2.setObjectName(u"match_type_l_2")

        self.gridLayout.addWidget(self.match_type_l_2, 4, 0, 1, 1)

        self.start_time_dtedit = QDateTimeEdit(self.add_athlete_f)
        self.start_time_dtedit.setObjectName(u"start_time_dtedit")
        self.start_time_dtedit.setDate(QDate(2026, 1, 1))

        self.gridLayout.addWidget(self.start_time_dtedit, 5, 2, 1, 1)

        self.match_num_l = QLabel(self.add_athlete_f)
        self.match_num_l.setObjectName(u"match_num_l")

        self.gridLayout.addWidget(self.match_num_l, 0, 0, 1, 1)

        self.remark_l = QLabel(self.add_athlete_f)
        self.remark_l.setObjectName(u"remark_l")

        self.gridLayout.addWidget(self.remark_l, 8, 0, 1, 1)

        self.match_type_cbox = QComboBox(self.add_athlete_f)
        self.match_type_cbox.addItem("")
        self.match_type_cbox.addItem("")
        self.match_type_cbox.addItem("")
        self.match_type_cbox.addItem("")
        self.match_type_cbox.addItem("")
        self.match_type_cbox.addItem("")
        self.match_type_cbox.setObjectName(u"match_type_cbox")

        self.gridLayout.addWidget(self.match_type_cbox, 3, 2, 1, 1)

        self.match_type_cbox_2 = QComboBox(self.add_athlete_f)
        self.match_type_cbox_2.addItem("")
        self.match_type_cbox_2.addItem("")
        self.match_type_cbox_2.addItem("")
        self.match_type_cbox_2.addItem("")
        self.match_type_cbox_2.addItem("")
        self.match_type_cbox_2.addItem("")
        self.match_type_cbox_2.setObjectName(u"match_type_cbox_2")

        self.gridLayout.addWidget(self.match_type_cbox_2, 4, 2, 1, 1)

        self.team_2_cbox = QComboBox(self.add_athlete_f)
        self.team_2_cbox.setObjectName(u"team_2_cbox")

        self.gridLayout.addWidget(self.team_2_cbox, 2, 2, 1, 1)

        self.match_type_l = QLabel(self.add_athlete_f)
        self.match_type_l.setObjectName(u"match_type_l")

        self.gridLayout.addWidget(self.match_type_l, 3, 0, 1, 1)

        self.match_num_sbox = QSpinBox(self.add_athlete_f)
        self.match_num_sbox.setObjectName(u"match_num_sbox")

        self.gridLayout.addWidget(self.match_num_sbox, 0, 2, 1, 1)

        self.remark_edit_2 = QLineEdit(self.add_athlete_f)
        self.remark_edit_2.setObjectName(u"remark_edit_2")

        self.gridLayout.addWidget(self.remark_edit_2, 7, 2, 1, 1)

        self.match_court_l = QLabel(self.add_athlete_f)
        self.match_court_l.setObjectName(u"match_court_l")

        self.gridLayout.addWidget(self.match_court_l, 7, 0, 1, 1)

        self.start_time_l = QLabel(self.add_athlete_f)
        self.start_time_l.setObjectName(u"start_time_l")

        self.gridLayout.addWidget(self.start_time_l, 5, 0, 1, 1)

        self.end_time_l = QLabel(self.add_athlete_f)
        self.end_time_l.setObjectName(u"end_time_l")

        self.gridLayout.addWidget(self.end_time_l, 6, 0, 1, 1)

        self.remark_edit = QLineEdit(self.add_athlete_f)
        self.remark_edit.setObjectName(u"remark_edit")

        self.gridLayout.addWidget(self.remark_edit, 8, 2, 1, 1)

        self.team_2_l = QLabel(self.add_athlete_f)
        self.team_2_l.setObjectName(u"team_2_l")

        self.gridLayout.addWidget(self.team_2_l, 2, 0, 1, 1)

        self.team_1_l = QLabel(self.add_athlete_f)
        self.team_1_l.setObjectName(u"team_1_l")

        self.gridLayout.addWidget(self.team_1_l, 1, 0, 1, 1)

        self.team_1_cbox = QComboBox(self.add_athlete_f)
        self.team_1_cbox.setObjectName(u"team_1_cbox")

        self.gridLayout.addWidget(self.team_1_cbox, 1, 2, 1, 1)

        self.end_time_dtedit = QDateTimeEdit(self.add_athlete_f)
        self.end_time_dtedit.setObjectName(u"end_time_dtedit")
        self.end_time_dtedit.setDate(QDate(2026, 1, 1))

        self.gridLayout.addWidget(self.end_time_dtedit, 6, 2, 1, 1)


        self.verticalLayout.addWidget(self.add_athlete_f)

        self.buttonBox = QDialogButtonBox(court_court_edit)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(court_court_edit)
        self.buttonBox.accepted.connect(court_court_edit.accept)
        self.buttonBox.rejected.connect(court_court_edit.reject)

        QMetaObject.connectSlotsByName(court_court_edit)
    # setupUi

    def retranslateUi(self, court_court_edit):
        court_court_edit.setWindowTitle(QCoreApplication.translate("court_court_edit", u"\u7de8\u8f2f/\u52a0\u5165\u8cfd\u4e8b", None))
        self.match_type_l_2.setText(QCoreApplication.translate("court_court_edit", u"\u6bcf\u5c40\u5f97\u5206\u6578", None))
        self.match_num_l.setText(QCoreApplication.translate("court_court_edit", u"\u8cfd\u4e8b\u7de8\u865f", None))
        self.remark_l.setText(QCoreApplication.translate("court_court_edit", u"\u5099\u8a3b", None))
        self.match_type_cbox.setItemText(0, QCoreApplication.translate("court_court_edit", u"\u7537\u55ae", None))
        self.match_type_cbox.setItemText(1, QCoreApplication.translate("court_court_edit", u"\u5973\u55ae", None))
        self.match_type_cbox.setItemText(2, QCoreApplication.translate("court_court_edit", u"\u7537\u96d9", None))
        self.match_type_cbox.setItemText(3, QCoreApplication.translate("court_court_edit", u"\u5973\u96d9", None))
        self.match_type_cbox.setItemText(4, QCoreApplication.translate("court_court_edit", u"\u6df7\u96d9", None))
        self.match_type_cbox.setItemText(5, QCoreApplication.translate("court_court_edit", u"\u5718\u9ad4", None))

        self.match_type_cbox_2.setItemText(0, QCoreApplication.translate("court_court_edit", u"\u7537\u55ae", None))
        self.match_type_cbox_2.setItemText(1, QCoreApplication.translate("court_court_edit", u"\u5973\u55ae", None))
        self.match_type_cbox_2.setItemText(2, QCoreApplication.translate("court_court_edit", u"\u7537\u96d9", None))
        self.match_type_cbox_2.setItemText(3, QCoreApplication.translate("court_court_edit", u"\u5973\u96d9", None))
        self.match_type_cbox_2.setItemText(4, QCoreApplication.translate("court_court_edit", u"\u6df7\u96d9", None))
        self.match_type_cbox_2.setItemText(5, QCoreApplication.translate("court_court_edit", u"\u5718\u9ad4", None))

        self.match_type_l.setText(QCoreApplication.translate("court_court_edit", u"\u8cfd\u4e8b\u985e\u578b", None))
        self.match_court_l.setText(QCoreApplication.translate("court_court_edit", u"\u5834\u5730", None))
        self.start_time_l.setText(QCoreApplication.translate("court_court_edit", u"\u958b\u59cb\u6642\u9593", None))
        self.end_time_l.setText(QCoreApplication.translate("court_court_edit", u"\u7d50\u675f\u6642\u9593", None))
        self.team_2_l.setText(QCoreApplication.translate("court_court_edit", u"\u968a\u4f0d\u4e8c", None))
        self.team_1_l.setText(QCoreApplication.translate("court_court_edit", u"\u968a\u4f0d\u4e00", None))
    # retranslateUi

