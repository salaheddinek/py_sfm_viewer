import config
import color
import pathlib
from ui_mainwindow import Ui_MainWindow
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import ui_style
import ui_data


class ViewerGui(Qw.QMainWindow):
    def __init__(self, in_args, in_params: config.Params):
        print("SFM Viewer: Gui mode")
        super(ViewerGui, self).__init__()
        self.i_app = ui_data.qt_icon_from_text_image(ui_data.APP_ICON)
        self.setWindowIcon(self.i_app)
        self.app_params = in_params
        self.app_params.input_path = in_args.input
        self.app_params.output_path = in_args.output
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("SFM Viewer")
        self._style_app()
        self._init()
        self._connect_signals()
        self.update_ui_elements()
        # self.update_ui_elements()

    def _connect_signals(self):
        info = config.HELP_INFO
        self.ui.btn_exit.clicked.connect(self.close_app)
        self.ui.btn_info_cone_size.clicked.connect(lambda: self.window_message(info["cone_size"], "Info"))
        self.ui.btn_info_view_mode.clicked.connect(lambda: self.window_message(info["view_mode"], "Info"))
        self.ui.btn_info_subsample_mode.clicked.connect(lambda: self.window_message(info["subsample_mode"], "Info"))
        self.ui.btn_info_subsample_factor.clicked.connect(lambda: self.window_message(info["subsample_factor"], "Info"))
        self.ui.btn_info_input.clicked.connect(lambda: self.window_message(info["input_path"], "Info"))

        self.ui.btn_in_path.clicked.connect(self._look_for_input_path)
        self.ui.btn_out_path.clicked.connect(self._look_for_output_path)
        self.ui.btn_suggest_output.clicked.connect(self._suggest_output_path)

        self.ui.combo_box_colormap.currentIndexChanged.connect(self._color_map_changed)
        self.ui.btn_first_color.clicked.connect(self._get_first_camera_color)
        self.ui.btn_last_color.clicked.connect(self._get_last_camera_color)

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
        for wid in [self.ui.btn_info_view_mode, self.ui.btn_info_cone_size, self.ui.btn_info_subsample_mode,
                    self.ui.btn_info_subsample_factor, self.ui.btn_info_input]:
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

    def _init(self):
        self.ui.line_edit_first_color.setReadOnly(True)
        self.ui.line_edit_last_color.setReadOnly(True)
        self.ui.line_edit_view_color.setReadOnly(True)
        self.ui.widget_msg.setHidden(True)
        self.ui.btn_go_back.setHidden(True)

        self.ui.line_edit_in_path.setText(str(self.app_params.input_path))
        self.app_params.process_output_path()
        self.ui.line_edit_out_path.setText(str(self.app_params.output_path))

        available_view_modes = []
        for vm in config.ViewMode:
            available_view_modes.append(vm.name)
        self.ui.combo_box_view_mode.addItems(available_view_modes)

        available_subsample_modes = []
        for csm in config.CameraSubsampleMode:
            available_subsample_modes.append(csm.name)
        self.ui.combo_box_subsample_mode.addItems(available_subsample_modes)
        custom_color_icon = ui_data.qt_icon_from_text_image(ui_data.CUSTOM_COLOR_ICON)
        self.ui.combo_box_colormap.addItem(custom_color_icon, "custom")
        for colormap in self.app_params.configuration["available_colormaps"]:
            c_generator = color.ColorGradient(self.app_params.configuration["available_colormaps"][colormap])

            w, h = 70, 50
            map_colors = c_generator.generate_colors(w)
            image = Qg.QImage(w, h, Qg.QImage.Format.Format_RGB32)
            for i in range(w):
                for j in range(h):
                    pixel_c = map_colors[i]
                    image.setPixelColor(i, j, Qg.QColor(pixel_c.r, pixel_c.g, pixel_c.b))
            c_map_icon = Qg.QIcon(Qg.QPixmap.fromImage(image))
            self.ui.combo_box_colormap.addItem(c_map_icon, colormap)

    def _look_for_input_path(self):
        target_file = ""
        if self.app_params.input_path != "":
            target_file = str(pathlib.Path(self.app_params.input_path))
        name = Qw.QFileDialog.getOpenFileName(self, 'input File', dir=target_file)
        name = name[0]
        if name != "":
            self.app_params.input_path = name
            self.ui.line_edit_in_path.setText(name)

    def _look_for_output_path(self):
        target_file = ""
        if self.app_params.output_path != "":
            target_file = str(pathlib.Path(self.app_params.output_path))
        name = Qw.QFileDialog.getSaveFileName(self, 'output File', dir=target_file)
        name = name[0]
        if name != "":
            self.app_params.output_path = name
            self.ui.line_edit_out_path.setText(name)

    def _suggest_output_path(self):
        self.app_params.input_path = self.ui.line_edit_in_path.text()
        if self.app_params.input_path == "":
            return
        self.app_params.output_path = ""
        self.app_params.process_output_path()
        self.ui.line_edit_out_path.setText(self.app_params.output_path)

    def _get_first_camera_color(self):
        qt_color = Qw.QColorDialog.getColor()
        try:
            res_color = color.Color(qt_color.red(), qt_color.green(), qt_color.blue())
            self.app_params.configuration["first_camera_color"] = res_color.to_str(True)
            self.update_ui_elements()
        except ValueError:
            print(f"could not parse first camera color from given color")

    def _get_last_camera_color(self):
        qt_color = Qw.QColorDialog.getColor()
        try:
            res_color = color.Color(qt_color.red(), qt_color.green(), qt_color.blue())
            self.app_params.configuration["last_camera_color"] = res_color.to_str(True)
            self.update_ui_elements()
        except ValueError:
            print(f"could not parse last camera color from given color")

    def _color_map_changed(self):
        self.app_params.configuration["colormap_used"] = self.ui.combo_box_colormap.currentText()
        self.update_ui_elements()

    def update_ui_elements(self):
        cfg = self.app_params.configuration
        self.ui.combo_box_view_mode.setCurrentIndex(cfg["view_mode"].value)
        self.ui.dspin_box_cone_size.setValue(cfg["camera_cone_size"])
        self.ui.combo_box_subsample_mode.setCurrentIndex(cfg["camera_subsample_mode"].value)
        self.ui.dspin_box_subsample_factor.setValue(cfg["camera_subsample_factor"])

        colormap_idx = 0
        for i, colormap in enumerate(cfg["available_colormaps"]):
            if colormap == cfg["colormap_used"]:
                colormap_idx = i + 1
        self.ui.combo_box_colormap.setCurrentIndex(colormap_idx)

        # custom colors widget
        cam1_color = color.Color.parse_from_str(cfg["first_camera_color"]).to_hex()
        self.ui.line_edit_first_color.setText(cam1_color)
        self.ui.line_edit_first_color.setStyleSheet(f"background-color: {cam1_color}")
        cam2_color = color.Color.parse_from_str(cfg["last_camera_color"]).to_hex()
        self.ui.line_edit_last_color.setText(cam2_color)
        self.ui.line_edit_last_color.setStyleSheet(f"background-color: {cam2_color}")
        if colormap_idx == 0:
            self.ui.wid_custom_colors.setHidden(False)
        else:
            self.ui.wid_custom_colors.setHidden(True)

        # preview of the color gradient
        if colormap_idx == 0:
            c_map = color.ColorGradient(f"{cam1_color} 0%, {cam2_color} 100%")
        else:
            c_map = color.ColorGradient(cfg["available_colormaps"][cfg["colormap_used"]])
        qt_gradient = c_map.generate_qt_gradient_str()
        self.ui.line_edit_view_color.setStyleSheet(f"background-color: {qt_gradient}")

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
