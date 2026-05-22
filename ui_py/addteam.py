# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addteam.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_add_team_dialog(object):
    def setupUi(self, add_team_dialog):
        if not add_team_dialog.objectName():
            add_team_dialog.setObjectName(u"add_team_dialog")
        add_team_dialog.resize(400, 200)
        self.verticalLayout = QVBoxLayout(add_team_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.team_name_f = QFrame(add_team_dialog)
        self.team_name_f.setObjectName(u"team_name_f")
        self.team_name_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.team_name_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.team_name_f)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.team_name_l = QLabel(self.team_name_f)
        self.team_name_l.setObjectName(u"team_name_l")
        self.team_name_l.setMinimumSize(QSize(50, 0))
        self.team_name_l.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.team_name_l)

        self.team_name_edit = QLineEdit(self.team_name_f)
        self.team_name_edit.setObjectName(u"team_name_edit")
        self.team_name_edit.setMaxLength(100)

        self.horizontalLayout.addWidget(self.team_name_edit)


        self.verticalLayout.addWidget(self.team_name_f)

        self.buttonBox = QDialogButtonBox(add_team_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(add_team_dialog)
        self.buttonBox.accepted.connect(add_team_dialog.accept)
        self.buttonBox.rejected.connect(add_team_dialog.reject)

        QMetaObject.connectSlotsByName(add_team_dialog)
    # setupUi

    def retranslateUi(self, add_team_dialog):
        add_team_dialog.setWindowTitle(QCoreApplication.translate("add_team_dialog", u"Dialog", None))
        self.team_name_l.setText(QCoreApplication.translate("add_team_dialog", u"\u968a\u4f0d\u540d\u7a31:", None))
    # retranslateUi

