import config
from ui_mainwindow import Ui_MainWindow
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import ui_style
import ui_data


class ViewerGui(Qw.QMainWindow):
    def __init__(self, in_args, in_params):
        print("SFM Viewer: Gui mode")
        super(ViewerGui, self).__init__()
        self.i_app = ui_data.qt_icon_from_text_image(ui_data.APP_ICON)
        self.setWindowIcon(self.i_app)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("SFM Viewer")
        self._style_app()
        self._connect_signals()
        # self.update_ui_elements()

    def _connect_signals(self):
        self.ui.btn_exit.clicked.connect(self.close_app)
        self.ui.btn_info_cone_size.clicked.connect(lambda: self.window_message(config.HELP_INFO["cone_size"], "Info"))
        self.ui.btn_info_view_mode.clicked.connect(lambda: self.window_message(config.HELP_INFO["view_mode"], "Info"))
        self.ui.btn_info_subsample_mode.clicked.connect(
            lambda: self.window_message(config.HELP_INFO["subsample_mode"], "Info"))
        self.ui.btn_info_subsample_factor.clicked.connect(
            lambda: self.window_message(config.HELP_INFO["subsample_factor"], "Info"))

    def _style_app(self):
        f_id = Qg.QFontDatabase.addApplicationFontFromData(ui_data.text_data_to_bytes(ui_data.FONT_DATA_OPEN_SANS))
        if f_id < 0:
            print("Error loading font from data")
        families = Qg.QFontDatabase.applicationFontFamilies(f_id)
        # print(families)
        for wid in ["QLabel", "QPushButton", "QLineEdit", "QProgressBar", "QTabBar", "QTabWidget", "QCheckBox",
                    "QRadioButton", "QGroupBox", "QToolButton", "QComboBox", "QListView", "QSpinBox", "QDoubleSpinBox",
                    "QTextEdit", "QPlainTextEdit"]:
            Qw.QApplication.setFont(Qg.QFont(families[0], 12), wid)
        self.setStyleSheet(ui_style.APP_STYLESHEET)
        self._set_css_class(self.ui.btn_ok, "action")
        self._set_css_class(self.ui.btn_exit, "danger")

        self.i_info = ui_data.qt_icon_from_text_image(ui_data.INFO_ICON)
        for wid in [self.ui.btn_info_view_mode, self.ui.btn_info_cone_size, self.ui.btn_info_subsample_mode, self.ui.btn_info_subsample_factor]:
            wid.setIcon(self.i_info)

        self.i_save = ui_data.qt_icon_from_text_image(ui_data.SAVE_ICON)
        self.ui.btn_ok.setIcon(self.i_save)

        self.i_exit = ui_data.qt_icon_from_text_image(ui_data.EXIT_ICON)
        self.ui.btn_exit.setIcon(self.i_exit)

        self.i_path = ui_data.qt_icon_from_text_image(ui_data.PATH_ICON)
        self.ui.btn_in_path.setIcon(self.i_path)
        self.ui.btn_out_path.setIcon(self.i_path)

        self.i_back = ui_data.qt_icon_from_text_image(ui_data.BACK_ICON)
        self.ui.btn_go_back.setIcon(self.i_back)

        self.i_colors = ui_data.qt_icon_from_text_image(ui_data.COLORS_ICON)
        self.ui.btn_first_color.setIcon(self.i_colors)
        self.ui.btn_last_color.setIcon(self.i_colors)

    @staticmethod
    def _set_css_class(widget, class_name):
        widget.setProperty("cssClass", class_name)
        widget.style().polish(widget)

    def close_app(self):
        self.close()

    def window_message(self, msg, title="Info", minimum_width=800, minimum_height=300):
        txt = msg.replace("\n", "<br/>")

        used_font = self.font().__copy__()
        # used_size = used_font.pointSize()
        # if used_size > 2:
        #     used_font.setPointSize(used_size - 2)
        qd = Qw.QDialog(self)
        qd.setModal(True)
        qd.setPalette(self.palette())
        qd.setWindowTitle(title)

        scroll = Qw.QScrollArea()
        layout = Qw.QVBoxLayout()
        label = Qw.QLabel(txt, scroll)
        label.setTextFormat(Qc.Qt.RichText)
        label.setWordWrap(True)
        label.setPalette(self.palette())
        label.setFont(used_font)
        scroll.setWidget(label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        # scroll.setFixedHeight(200)
        mini_layout = Qw.QHBoxLayout()
        h_spacer = Qw.QSpacerItem(40, 20, Qw.QSizePolicy.Policy.Expanding, Qw.QSizePolicy.Policy.Minimum)
        mini_layout.addSpacerItem(h_spacer)
        btn = Qw.QPushButton(qd)
        btn.setFont(used_font)
        btn.setMinimumWidth(btn.minimumWidth())
        btn.clicked.connect(qd.accept)
        btn.setText("   OK   ")
        mini_layout.addWidget(btn)
        mini_layout.addSpacerItem(h_spacer)
        layout.addLayout(mini_layout)
        qd.setMinimumWidth(minimum_width)
        qd.setMinimumHeight(minimum_height)

        qd.setLayout(layout)
        qd.show()
        qd.exec()
