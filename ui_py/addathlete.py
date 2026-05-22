# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addathlete.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_add_athlete_dialog(object):
    def setupUi(self, add_athlete_dialog):
        if not add_athlete_dialog.objectName():
            add_athlete_dialog.setObjectName(u"add_athlete_dialog")
        add_athlete_dialog.resize(400, 358)
        self.verticalLayout = QVBoxLayout(add_athlete_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.add_athlete_f = QFrame(add_athlete_dialog)
        self.add_athlete_f.setObjectName(u"add_athlete_f")
        self.add_athlete_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_athlete_f.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.add_athlete_f)
        self.gridLayout.setObjectName(u"gridLayout")
        self.name_edit = QLineEdit(self.add_athlete_f)
        self.name_edit.setObjectName(u"name_edit")
        self.name_edit.setMaxLength(50)

        self.gridLayout.addWidget(self.name_edit, 3, 1, 1, 1)

        self.gender_cbox = QComboBox(self.add_athlete_f)
        self.gender_cbox.addItem("")
        self.gender_cbox.addItem("")
        self.gender_cbox.setObjectName(u"gender_cbox")

        self.gridLayout.addWidget(self.gender_cbox, 6, 1, 1, 1)

        self.gender_l = QLabel(self.add_athlete_f)
        self.gender_l.setObjectName(u"gender_l")

        self.gridLayout.addWidget(self.gender_l, 6, 0, 1, 1)

        self.school_team_l = QLabel(self.add_athlete_f)
        self.school_team_l.setObjectName(u"school_team_l")

        self.gridLayout.addWidget(self.school_team_l, 9, 0, 1, 1)

        self.school_num_edit = QLineEdit(self.add_athlete_f)
        self.school_num_edit.setObjectName(u"school_num_edit")
        self.school_num_edit.setMaxLength(20)

        self.gridLayout.addWidget(self.school_num_edit, 5, 1, 1, 1)

        self.grade_l = QLabel(self.add_athlete_f)
        self.grade_l.setObjectName(u"grade_l")

        self.gridLayout.addWidget(self.grade_l, 7, 0, 1, 1)

        self.remark_l = QLabel(self.add_athlete_f)
        self.remark_l.setObjectName(u"remark_l")

        self.gridLayout.addWidget(self.remark_l, 10, 0, 1, 1)

        self.remark_edit = QLineEdit(self.add_athlete_f)
        self.remark_edit.setObjectName(u"remark_edit")

        self.gridLayout.addWidget(self.remark_edit, 10, 1, 1, 1)

        self.department_l = QLabel(self.add_athlete_f)
        self.department_l.setObjectName(u"department_l")

        self.gridLayout.addWidget(self.department_l, 8, 0, 1, 1)

        self.department_edit = QLineEdit(self.add_athlete_f)
        self.department_edit.setObjectName(u"department_edit")
        self.department_edit.setMaxLength(20)

        self.gridLayout.addWidget(self.department_edit, 8, 1, 1, 1)

        self.grade_cbox = QComboBox(self.add_athlete_f)
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.addItem("")
        self.grade_cbox.setObjectName(u"grade_cbox")

        self.gridLayout.addWidget(self.grade_cbox, 7, 1, 1, 1)

        self.school_num_l = QLabel(self.add_athlete_f)
        self.school_num_l.setObjectName(u"school_num_l")

        self.gridLayout.addWidget(self.school_num_l, 5, 0, 1, 1)

        self.name_l = QLabel(self.add_athlete_f)
        self.name_l.setObjectName(u"name_l")

        self.gridLayout.addWidget(self.name_l, 3, 0, 1, 1)

        self.school_team_cbox = QComboBox(self.add_athlete_f)
        self.school_team_cbox.addItem("")
        self.school_team_cbox.addItem("")
        self.school_team_cbox.setObjectName(u"school_team_cbox")

        self.gridLayout.addWidget(self.school_team_cbox, 9, 1, 1, 1)

        self.team_l = QLabel(self.add_athlete_f)
        self.team_l.setObjectName(u"team_l")

        self.gridLayout.addWidget(self.team_l, 2, 0, 1, 1)

        self.team_cbox = QComboBox(self.add_athlete_f)
        self.team_cbox.setObjectName(u"team_cbox")

        self.gridLayout.addWidget(self.team_cbox, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.add_athlete_f)

        self.buttonBox = QDialogButtonBox(add_athlete_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(add_athlete_dialog)
        self.buttonBox.accepted.connect(add_athlete_dialog.accept)
        self.buttonBox.rejected.connect(add_athlete_dialog.reject)

        QMetaObject.connectSlotsByName(add_athlete_dialog)
    # setupUi

    def retranslateUi(self, add_athlete_dialog):
        add_athlete_dialog.setWindowTitle(QCoreApplication.translate("add_athlete_dialog", u"Dialog", None))
        self.gender_cbox.setItemText(0, QCoreApplication.translate("add_athlete_dialog", u"\u7537", None))
        self.gender_cbox.setItemText(1, QCoreApplication.translate("add_athlete_dialog", u"\u5973", None))

        self.gender_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u6027\u5225", None))
        self.school_team_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u6821\u968a/\u9ad4\u4fdd\u751f\u8cc7\u683c", None))
        self.grade_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u5e74\u7d1a", None))
        self.remark_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u5099\u8a3b", None))
        self.department_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u7cfb\u6240", None))
        self.grade_cbox.setItemText(0, QCoreApplication.translate("add_athlete_dialog", u"\u5927\u4e00", None))
        self.grade_cbox.setItemText(1, QCoreApplication.translate("add_athlete_dialog", u"\u5927\u4e8c", None))
        self.grade_cbox.setItemText(2, QCoreApplication.translate("add_athlete_dialog", u"\u5927\u4e09", None))
        self.grade_cbox.setItemText(3, QCoreApplication.translate("add_athlete_dialog", u"\u5927\u56db", None))
        self.grade_cbox.setItemText(4, QCoreApplication.translate("add_athlete_dialog", u"\u5927\u4e94~\u5927\u516d", None))
        self.grade_cbox.setItemText(5, QCoreApplication.translate("add_athlete_dialog", u"\u78a9\u4e00~", None))
        self.grade_cbox.setItemText(6, QCoreApplication.translate("add_athlete_dialog", u"\u535a\u4e00~", None))
        self.grade_cbox.setItemText(7, QCoreApplication.translate("add_athlete_dialog", u"\u5176\u4ed6", None))

        self.school_num_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u5b78\u865f", None))
        self.name_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u59d3\u540d", None))
        self.school_team_cbox.setItemText(0, QCoreApplication.translate("add_athlete_dialog", u"\u5426", None))
        self.school_team_cbox.setItemText(1, QCoreApplication.translate("add_athlete_dialog", u"\u662f", None))

        self.team_l.setText(QCoreApplication.translate("add_athlete_dialog", u"\u6240\u5c6c\u968a\u4f0d", None))
    # retranslateUi

