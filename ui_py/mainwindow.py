# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.topic_l = QLabel(self.centralwidget)
        self.topic_l.setObjectName(u"topic_l")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.topic_l.sizePolicy().hasHeightForWidth())
        self.topic_l.setSizePolicy(sizePolicy)
        self.topic_l.setMinimumSize(QSize(0, 20))
        self.topic_l.setMaximumSize(QSize(16777215, 30))
        self.topic_l.setTextFormat(Qt.TextFormat.AutoText)
        self.topic_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.topic_l)

        self.match_name_l = QLabel(self.centralwidget)
        self.match_name_l.setObjectName(u"match_name_l")
        self.match_name_l.setMinimumSize(QSize(0, 40))
        self.match_name_l.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(12)
        self.match_name_l.setFont(font)
        self.match_name_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.match_name_l)

        self.match_frame = QFrame(self.centralwidget)
        self.match_frame.setObjectName(u"match_frame")
        self.match_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.match_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.match_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.match_in_progress_f = QFrame(self.match_frame)
        self.match_in_progress_f.setObjectName(u"match_in_progress_f")
        self.match_in_progress_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.match_in_progress_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.match_in_progress_f)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.match_in_progress_l = QLabel(self.match_in_progress_f)
        self.match_in_progress_l.setObjectName(u"match_in_progress_l")
        self.match_in_progress_l.setMinimumSize(QSize(0, 20))
        self.match_in_progress_l.setMaximumSize(QSize(16777215, 20))
        self.match_in_progress_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.match_in_progress_l)

        self.match_in_progress_view = QGraphicsView(self.match_in_progress_f)
        self.match_in_progress_view.setObjectName(u"match_in_progress_view")
        self.match_in_progress_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_4.addWidget(self.match_in_progress_view)


        self.horizontalLayout_2.addWidget(self.match_in_progress_f)

        self.match_in_preperation_f = QFrame(self.match_frame)
        self.match_in_preperation_f.setObjectName(u"match_in_preperation_f")
        self.match_in_preperation_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.match_in_preperation_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.match_in_preperation_f)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.match_in_preperation_l = QLabel(self.match_in_preperation_f)
        self.match_in_preperation_l.setObjectName(u"match_in_preperation_l")
        sizePolicy.setHeightForWidth(self.match_in_preperation_l.sizePolicy().hasHeightForWidth())
        self.match_in_preperation_l.setSizePolicy(sizePolicy)
        self.match_in_preperation_l.setMinimumSize(QSize(0, 20))
        self.match_in_preperation_l.setMaximumSize(QSize(16777215, 20))
        self.match_in_preperation_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.match_in_preperation_l)

        self.match_in_preperation_view = QGraphicsView(self.match_in_preperation_f)
        self.match_in_preperation_view.setObjectName(u"match_in_preperation_view")
        self.match_in_preperation_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_3.addWidget(self.match_in_preperation_view)


        self.horizontalLayout_2.addWidget(self.match_in_preperation_f)

        self.match_upcoming_f = QFrame(self.match_frame)
        self.match_upcoming_f.setObjectName(u"match_upcoming_f")
        self.match_upcoming_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.match_upcoming_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.match_upcoming_f)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.match_upcoming_l = QLabel(self.match_upcoming_f)
        self.match_upcoming_l.setObjectName(u"match_upcoming_l")
        sizePolicy.setHeightForWidth(self.match_upcoming_l.sizePolicy().hasHeightForWidth())
        self.match_upcoming_l.setSizePolicy(sizePolicy)
        self.match_upcoming_l.setMinimumSize(QSize(0, 20))
        self.match_upcoming_l.setMaximumSize(QSize(16777215, 20))
        self.match_upcoming_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.match_upcoming_l)

        self.match_upcoming_view = QGraphicsView(self.match_upcoming_f)
        self.match_upcoming_view.setObjectName(u"match_upcoming_view")
        self.match_upcoming_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_2.addWidget(self.match_upcoming_view)


        self.horizontalLayout_2.addWidget(self.match_upcoming_f)


        self.verticalLayout.addWidget(self.match_frame)

        self.function_f = QFrame(self.centralwidget)
        self.function_f.setObjectName(u"function_f")
        self.function_f.setMaximumSize(QSize(16777215, 30))
        self.function_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.function_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.function_f)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 0, 0)
        self.all_match_btn = QPushButton(self.function_f)
        self.all_match_btn.setObjectName(u"all_match_btn")
        self.all_match_btn.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.all_match_btn)

        self.team_list_btn = QPushButton(self.function_f)
        self.team_list_btn.setObjectName(u"team_list_btn")
        self.team_list_btn.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.team_list_btn)


        self.verticalLayout.addWidget(self.function_f)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8cfd\u4e8b\u8cc7\u8a0a\u7e3d\u8868", None))
        self.topic_l.setText(QCoreApplication.translate("MainWindow", u"\u7fbd\u7403\u8cfd\u4e8b\u6aa2\u9304\u7cfb\u7d71", None))
        self.match_name_l.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u524d\u8cfd\u4e8b\u540d\u7a31", None))
        self.match_in_progress_l.setText(QCoreApplication.translate("MainWindow", u"\u9032\u884c\u4e2d\u8cfd\u4e8b", None))
        self.match_in_preperation_l.setText(QCoreApplication.translate("MainWindow", u"\u6e96\u5099\u9032\u884c\u8cfd\u4e8b", None))
        self.match_upcoming_l.setText(QCoreApplication.translate("MainWindow", u"\u5373\u5c07\u9032\u884c\u8cfd\u4e8b", None))
        self.all_match_btn.setText(QCoreApplication.translate("MainWindow", u"\u6240\u6709\u8cfd\u4e8b", None))
        self.team_list_btn.setText(QCoreApplication.translate("MainWindow", u"\u968a\u4f0d/\u9078\u624b\u540d\u55ae", None))
    # retranslateUi

