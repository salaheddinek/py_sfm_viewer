from ui_mainwindow import Ui_MainWindow
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import ui_style
import ui_data


class ViewerGui(Qw.QMainWindow):
    def __init__(self, in_args, in_params):
        print("gui init")
        super(ViewerGui, self).__init__()

        # self.i = qt_icons.qt_icon_from_text_image(qt_icons.APP_ICON)
        # self.setWindowIcon(self.i)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.setFont(Qg.QFont())
        self.setWindowTitle("SFM Viewer")
        self._style_app()
        # self._connect_signals()
        # self.update_ui_elements()

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
        self._set_css_class(self.ui.pushButton, "action")
        self._set_css_class(self.ui.pushButton_2, "danger")

    @staticmethod
    def _set_css_class(widget, class_name):
        widget.setProperty("cssClass", class_name)
        widget.style().polish(widget)