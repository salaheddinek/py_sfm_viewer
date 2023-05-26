# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line_edit_in_path = QLineEdit(self.centralwidget)
        self.line_edit_in_path.setObjectName(u"line_edit_in_path")

        self.gridLayout_3.addWidget(self.line_edit_in_path, 0, 1, 1, 1)

        self.btn_out_path = QPushButton(self.centralwidget)
        self.btn_out_path.setObjectName(u"btn_out_path")

        self.gridLayout_3.addWidget(self.btn_out_path, 1, 2, 1, 1)

        self.btn_in_path = QPushButton(self.centralwidget)
        self.btn_in_path.setObjectName(u"btn_in_path")

        self.gridLayout_3.addWidget(self.btn_in_path, 0, 2, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.line_edit_out_path = QLineEdit(self.centralwidget)
        self.line_edit_out_path.setObjectName(u"line_edit_out_path")

        self.gridLayout_3.addWidget(self.line_edit_out_path, 1, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.btn_suggest_output = QPushButton(self.centralwidget)
        self.btn_suggest_output.setObjectName(u"btn_suggest_output")

        self.gridLayout_3.addWidget(self.btn_suggest_output, 1, 3, 1, 1)

        self.btn_info_input = QToolButton(self.centralwidget)
        self.btn_info_input.setObjectName(u"btn_info_input")

        self.gridLayout_3.addWidget(self.btn_info_input, 0, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.dspin_box_cone_size = QDoubleSpinBox(self.groupBox)
        self.dspin_box_cone_size.setObjectName(u"dspin_box_cone_size")
        self.dspin_box_cone_size.setDecimals(4)
        self.dspin_box_cone_size.setMinimum(0.000100000000000)
        self.dspin_box_cone_size.setMaximum(99999.000000000000000)
        self.dspin_box_cone_size.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.dspin_box_cone_size, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.combo_box_view_mode = QComboBox(self.groupBox)
        self.combo_box_view_mode.setObjectName(u"combo_box_view_mode")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box_view_mode.sizePolicy().hasHeightForWidth())
        self.combo_box_view_mode.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.combo_box_view_mode, 0, 1, 1, 1)

        self.btn_info_view_mode = QToolButton(self.groupBox)
        self.btn_info_view_mode.setObjectName(u"btn_info_view_mode")

        self.gridLayout.addWidget(self.btn_info_view_mode, 0, 2, 1, 1)

        self.btn_info_cone_size = QToolButton(self.groupBox)
        self.btn_info_cone_size.setObjectName(u"btn_info_cone_size")

        self.gridLayout.addWidget(self.btn_info_cone_size, 1, 2, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.dspin_box_subsample_factor = QDoubleSpinBox(self.groupBox_2)
        self.dspin_box_subsample_factor.setObjectName(u"dspin_box_subsample_factor")
        self.dspin_box_subsample_factor.setDecimals(4)
        self.dspin_box_subsample_factor.setMinimum(0.000100000000000)
        self.dspin_box_subsample_factor.setMaximum(99999.000000000000000)
        self.dspin_box_subsample_factor.setSingleStep(1.000000000000000)

        self.gridLayout_4.addWidget(self.dspin_box_subsample_factor, 2, 3, 1, 1)

        self.btn_info_subsample_mode = QToolButton(self.groupBox_2)
        self.btn_info_subsample_mode.setObjectName(u"btn_info_subsample_mode")

        self.gridLayout_4.addWidget(self.btn_info_subsample_mode, 1, 4, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 2, 0, 1, 1)

        self.combo_box_subsample_mode = QComboBox(self.groupBox_2)
        self.combo_box_subsample_mode.setObjectName(u"combo_box_subsample_mode")
        sizePolicy.setHeightForWidth(self.combo_box_subsample_mode.sizePolicy().hasHeightForWidth())
        self.combo_box_subsample_mode.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.combo_box_subsample_mode, 1, 3, 1, 1)

        self.btn_info_subsample_factor = QToolButton(self.groupBox_2)
        self.btn_info_subsample_factor.setObjectName(u"btn_info_subsample_factor")

        self.gridLayout_4.addWidget(self.btn_info_subsample_factor, 2, 4, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 2, 2)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.combo_box_colormap = QComboBox(self.groupBox_3)
        self.combo_box_colormap.setObjectName(u"combo_box_colormap")

        self.verticalLayout.addWidget(self.combo_box_colormap)

        self.wid_custom_colors = QWidget(self.groupBox_3)
        self.wid_custom_colors.setObjectName(u"wid_custom_colors")
        self.gridLayout_2 = QGridLayout(self.wid_custom_colors)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btn_first_color = QPushButton(self.wid_custom_colors)
        self.btn_first_color.setObjectName(u"btn_first_color")

        self.gridLayout_2.addWidget(self.btn_first_color, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.wid_custom_colors)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_3.addWidget(self.label_7)

        self.line_edit_first_color = QLineEdit(self.wid_custom_colors)
        self.line_edit_first_color.setObjectName(u"line_edit_first_color")

        self.horizontalLayout_3.addWidget(self.line_edit_first_color)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.wid_custom_colors)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_4.addWidget(self.label_8)

        self.line_edit_last_color = QLineEdit(self.wid_custom_colors)
        self.line_edit_last_color.setObjectName(u"line_edit_last_color")

        self.horizontalLayout_4.addWidget(self.line_edit_last_color)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

        self.btn_last_color = QPushButton(self.wid_custom_colors)
        self.btn_last_color.setObjectName(u"btn_last_color")

        self.gridLayout_2.addWidget(self.btn_last_color, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.wid_custom_colors)

        self.line_edit_view_color = QLineEdit(self.groupBox_3)
        self.line_edit_view_color.setObjectName(u"line_edit_view_color")

        self.verticalLayout.addWidget(self.line_edit_view_color)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.widget_msg = QWidget(self.centralwidget)
        self.widget_msg.setObjectName(u"widget_msg")
        self.verticalLayout_3 = QVBoxLayout(self.widget_msg)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_msg_title = QLabel(self.widget_msg)
        self.label_msg_title.setObjectName(u"label_msg_title")

        self.verticalLayout_3.addWidget(self.label_msg_title)

        self.label_msg_content = QLabel(self.widget_msg)
        self.label_msg_content.setObjectName(u"label_msg_content")

        self.verticalLayout_3.addWidget(self.label_msg_content)


        self.verticalLayout_2.addWidget(self.widget_msg)

        self.verticalSpacer = QSpacerItem(17, 131, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.btn_ok = QPushButton(self.centralwidget)
        self.btn_ok.setObjectName(u"btn_ok")

        self.horizontalLayout_2.addWidget(self.btn_ok)

        self.btn_go_back = QPushButton(self.centralwidget)
        self.btn_go_back.setObjectName(u"btn_go_back")

        self.horizontalLayout_2.addWidget(self.btn_go_back)

        self.btn_exit = QPushButton(self.centralwidget)
        self.btn_exit.setObjectName(u"btn_exit")

        self.horizontalLayout_2.addWidget(self.btn_exit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_out_path.setText(QCoreApplication.translate("MainWindow", u"Path", None))
        self.btn_in_path.setText(QCoreApplication.translate("MainWindow", u"Path", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Input file", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Output file", None))
        self.btn_suggest_output.setText(QCoreApplication.translate("MainWindow", u"suggest", None))
        self.btn_info_input.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Camera cones and geometry", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"View mode", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cone size", None))
        self.btn_info_view_mode.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.btn_info_cone_size.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Camera cones subsampling", None))
        self.btn_info_subsample_mode.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Subsample factor", None))
        self.btn_info_subsample_factor.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Subsample mode", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Camera cone colors", None))
        self.btn_first_color.setText(QCoreApplication.translate("MainWindow", u"Change color", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"First color", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Last color", None))
        self.btn_last_color.setText(QCoreApplication.translate("MainWindow", u"Change color", None))
        self.label_msg_title.setText(QCoreApplication.translate("MainWindow", u"Message Title", None))
        self.label_msg_content.setText(QCoreApplication.translate("MainWindow", u"Message content", None))
        self.btn_ok.setText(QCoreApplication.translate("MainWindow", u"OK  ", None))
        self.btn_go_back.setText(QCoreApplication.translate("MainWindow", u"Go back", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
    # retranslateUi

