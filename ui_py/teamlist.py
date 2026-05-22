# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'teamlist.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QLabel, QMainWindow, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.team_list_f = QFrame(self.centralwidget)
        self.team_list_f.setObjectName(u"team_list_f")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.team_list_f.sizePolicy().hasHeightForWidth())
        self.team_list_f.setSizePolicy(sizePolicy)
        self.team_list_f.setMinimumSize(QSize(160, 0))
        self.team_list_f.setMaximumSize(QSize(160, 16777215))
        self.team_list_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.team_list_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.team_list_f)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.team_list_l = QLabel(self.team_list_f)
        self.team_list_l.setObjectName(u"team_list_l")
        self.team_list_l.setMinimumSize(QSize(0, 20))
        self.team_list_l.setMaximumSize(QSize(16777215, 20))
        self.team_list_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.team_list_l)

        self.team_list_view = QGraphicsView(self.team_list_f)
        self.team_list_view.setObjectName(u"team_list_view")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.team_list_view.sizePolicy().hasHeightForWidth())
        self.team_list_view.setSizePolicy(sizePolicy1)
        self.team_list_view.setMinimumSize(QSize(0, 100))
        self.team_list_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout.addWidget(self.team_list_view)


        self.horizontalLayout.addWidget(self.team_list_f)

        self.athlete_list_f = QFrame(self.centralwidget)
        self.athlete_list_f.setObjectName(u"athlete_list_f")
        self.athlete_list_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.athlete_list_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.athlete_list_f)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.athlete_list_l = QLabel(self.athlete_list_f)
        self.athlete_list_l.setObjectName(u"athlete_list_l")
        sizePolicy.setHeightForWidth(self.athlete_list_l.sizePolicy().hasHeightForWidth())
        self.athlete_list_l.setSizePolicy(sizePolicy)
        self.athlete_list_l.setMinimumSize(QSize(0, 20))
        self.athlete_list_l.setMaximumSize(QSize(16777215, 20))
        self.athlete_list_l.setFrameShape(QFrame.Shape.NoFrame)
        self.athlete_list_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.athlete_list_l)

        self.athlete_list_view = QGraphicsView(self.athlete_list_f)
        self.athlete_list_view.setObjectName(u"athlete_list_view")
        self.athlete_list_view.setMinimumSize(QSize(0, 100))
        self.athlete_list_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_2.addWidget(self.athlete_list_view)


        self.horizontalLayout.addWidget(self.athlete_list_f)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u968a\u4f0d/\u9078\u624b\u540d\u55ae", None))
        self.team_list_l.setText(QCoreApplication.translate("MainWindow", u"\u968a\u4f0d\u540d\u55ae", None))
        self.athlete_list_l.setText(QCoreApplication.translate("MainWindow", u"\u9078\u624b\u540d\u55ae", None))
    # retranslateUi

