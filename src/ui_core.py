import config
import color
import pathlib
import geometry_builder
from ui_mainwindow import Ui_MainWindow
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import ui_style
import ui_data


class TrajectoryWorker(Qc.QObject):
    show_msg = Qc.Signal(str, str, bool)
    complete = Qc.Signal()

    def __init__(self, parameters: config.Params):
        super(TrajectoryWorker, self).__init__()
        self.app_params = parameters

    def run(self):
        viewer = geometry_builder.GeometryBuilder(self.app_params)
        err_title = "ERROR: process halted\n"
        try:
            res = viewer.write_camera_trajectory_plot()
            msg = f"result saved to:\n{self.app_params.output_path}\n"
            msg += f"number of camera cones plotted: {res['num_cones_plotted']}\n\n"
            if self.app_params.configuration["automatic_cone_size"]:
                msg += f"estimated cone size: {res['used_cone_size']:g}\n"
            rot = self.app_params.configuration["camera_rotation"]
            if rot[0] != 0 or rot[1] != 0 or rot[2] != 0:
                msg += f"camera rotation correction angles (deg): [x:{rot[0]:g}, y:{rot[1]:g}, z:{rot[2]:g}]\n"
            msg += res['trajectory_stats'].get_stats()
            self.app_params.save_to_config_file()
            self.show_msg.emit("Process finished successfully\n", msg, False)
        except ValueError as err:
            msg = "type: ValueError\nmessage: " + str(err)
            self.show_msg.emit(err_title, msg, False)
        except TypeError as err:
            msg = "type: TypeError\nmessage: " + str(err)
            self.show_msg.emit(err_title, msg, False)
        except IOError as err:
            msg = "type: IOError\nmessage: " + str(err)
            self.show_msg.emit(err_title, msg, False)

        self.complete.emit()


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
        self.thread = None
        self.traj_saver = None
        self.show_advanced_options = False

        self.setWindowTitle("SFM Viewer")
        self._style_app()
        self._init()
        self.update_ui_elements()
        self._connect_signals()
        # self.update_ui_elements()
        self.resize(800, 520)

    def _connect_signals(self):
        info = config.HELP_INFO
        self.ui.btn_exit.clicked.connect(self.close_app)
        self.ui.btn_info_cone_size.clicked.connect(lambda: self.window_message(info["cone_size"], "Info"))
        self.ui.btn_info_view_mode.clicked.connect(lambda: self.window_message(info["view_mode"], "Info"))
        self.ui.btn_info_subsample_mode.clicked.connect(lambda: self.window_message(info["subsample_mode"], "Info"))
        self.ui.btn_info_subsample_factor.clicked.connect(lambda: self.window_message(info["subsample_factor"], "Info"))
        self.ui.btn_info_input.clicked.connect(lambda: self.window_message(info["input_path"], "Info"))
        self.ui.btn_info_rot_correction.clicked.connect(lambda: self.window_message(info["rotation_angles"], "Info"))
        self.ui.btn_info_links_size.clicked.connect(lambda: self.window_message(info["links_size"], "Info"))
        self.ui.btn_info_auto_cone_size.clicked.connect(lambda: self.window_message(info["auto_cone_size"], "Info"))

        self.ui.btn_in_path.clicked.connect(self._look_for_input_path)
        self.ui.btn_out_path.clicked.connect(self._look_for_output_path)
        self.ui.btn_suggest_output.clicked.connect(self._suggest_output_path)

        self.ui.check_box_auto_cone.clicked.connect(self._automatic_cone_size_changed)
        self.ui.combo_box_colormap.currentIndexChanged.connect(self._retrieve_and_update)
        self.ui.btn_first_color.clicked.connect(self._get_first_camera_color)
        self.ui.btn_last_color.clicked.connect(self._get_last_camera_color)
        self.ui.check_box_show_advanced.clicked.connect(self._retrieve_and_update)

        self.ui.btn_ok.clicked.connect(self._run_trajectory_plot_algorithm)
        self.ui.btn_go_back.clicked.connect(self._go_back_to_main_window)

    def _style_app(self):
        f_id = Qg.QFontDatabase.addApplicationFontFromData(ui_data.text_data_to_bytes(ui_data.FONT_DATA_WORK_SANS))
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
        self._set_css_class(self.ui.label_msg_title, "title")

        self.i_info = ui_data.qt_icon_from_text_image(ui_data.INFO_ICON)
        for wid in [self.ui.btn_info_view_mode, self.ui.btn_info_cone_size, self.ui.btn_info_subsample_mode,
                    self.ui.btn_info_subsample_factor, self.ui.btn_info_input, self.ui.btn_info_rot_correction,
                    self.ui.btn_info_links_size, self.ui.btn_info_auto_cone_size]:
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

        self._set_css_class(self.ui.wid_advanced_options, "highlight")

    def _init(self):
        self.ui.line_edit_first_color.setReadOnly(True)
        self.ui.line_edit_last_color.setReadOnly(True)
        self.ui.line_edit_view_color.setReadOnly(True)
        self.ui.widget_msg.setHidden(True)
        self.ui.btn_go_back.setHidden(True)
        self.app_params.process_output_path()
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
        self.retrieve_info_from_ui()
        target_file = ""
        if self.app_params.input_path != "":
            target_file = str(pathlib.Path(self.app_params.input_path))
        name = Qw.QFileDialog.getOpenFileName(self, 'input File', dir=target_file)
        name = name[0]
        if name != "":
            self.app_params.input_path = name
        self.update_ui_elements()

    def _look_for_output_path(self):
        self.retrieve_info_from_ui()
        target_file = ""
        if self.app_params.output_path != "":
            target_file = str(pathlib.Path(self.app_params.output_path))
        name = Qw.QFileDialog.getSaveFileName(self, 'output File', dir=target_file)
        name = name[0]
        if name != "":
            self.app_params.output_path = name
        self.ui.line_edit_out_path.setText(name)

    def _automatic_cone_size_changed(self):
        self.retrieve_info_from_ui()
        if self.ui.check_box_auto_cone.isChecked():
            self.app_params.configuration["automatic_cone_size"] = True
        else:
            self.app_params.configuration["automatic_cone_size"] = False
        self.update_ui_elements()

    def _suggest_output_path(self):
        self.retrieve_info_from_ui()
        if self.app_params.input_path == "":
            return
        self.app_params.output_path = ""
        self.app_params.process_output_path()
        self.update_ui_elements()

    def _get_first_camera_color(self):
        self.retrieve_info_from_ui()
        qt_color = Qw.QColorDialog.getColor()
        try:
            res_color = color.Color(qt_color.red(), qt_color.green(), qt_color.blue())
            self.app_params.configuration["first_camera_color"] = res_color.to_str(True)
        except ValueError:
            print(f"could not parse first camera color from given color")
        self.update_ui_elements()

    def _get_last_camera_color(self):
        self.retrieve_info_from_ui()
        qt_color = Qw.QColorDialog.getColor()
        try:
            res_color = color.Color(qt_color.red(), qt_color.green(), qt_color.blue())
            self.app_params.configuration["last_camera_color"] = res_color.to_str(True)
        except ValueError:
            print(f"could not parse last camera color from given color")
        self.update_ui_elements()

    def _retrieve_and_update(self):
        self.retrieve_info_from_ui()
        self.update_ui_elements()

    def update_ui_elements(self):
        self.ui.line_edit_in_path.setText(self.app_params.input_path)
        self.ui.line_edit_out_path.setText(self.app_params.output_path)
        cfg = self.app_params.configuration
        self.ui.combo_box_view_mode.setCurrentIndex(cfg["view_mode"].value)
        self.ui.dspin_box_cone_size.setValue(cfg["camera_cone_size"])
        self.ui.check_box_auto_cone.setChecked(cfg["automatic_cone_size"])
        if cfg["automatic_cone_size"]:
            self.ui.dspin_box_cone_size.setDisabled(True)
        else:
            self.ui.dspin_box_cone_size.setDisabled(False)
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
        self.ui.check_box_show_advanced.setChecked(self.show_advanced_options)
        if self.show_advanced_options:
            self.ui.wid_advanced_options.setHidden(False)
        else:
            self.ui.wid_advanced_options.setHidden(True)

        self.ui.dspin_box_rot_x.setValue(cfg["camera_rotation"][0])
        self.ui.dspin_box_rot_y.setValue(cfg["camera_rotation"][1])
        self.ui.dspin_box_rot_z.setValue(cfg["camera_rotation"][2])
        self.ui.dspin_box_link_size.setValue(cfg["links_size_ratio"])
        self.ui.dspin_box_auto_cone_size.setValue(cfg["auto_cone_size_factor"])

    def retrieve_info_from_ui(self):
        self.app_params.input_path = self.ui.line_edit_in_path.text()
        self.app_params.output_path = self.ui.line_edit_out_path.text()
        cfg = self.app_params.configuration
        cfg["view_mode"] = config.ViewMode(self.ui.combo_box_view_mode.currentIndex())
        cfg["camera_cone_size"] = self.ui.dspin_box_cone_size.value()
        cfg["automatic_cone_size"] = self.ui.check_box_auto_cone.isChecked()
        cfg["camera_subsample_mode"] = config.CameraSubsampleMode(self.ui.combo_box_subsample_mode.currentIndex())
        cfg["camera_subsample_factor"] = self.ui.dspin_box_subsample_factor.value()
        cfg["colormap_used"] = self.ui.combo_box_colormap.currentText()
        cfg["first_camera_color"] = color.Color.parse_from_str(self.ui.line_edit_first_color.text()).to_str(True)
        cfg["last_camera_color"] = color.Color.parse_from_str(self.ui.line_edit_last_color.text()).to_str(True)
        cfg["links_size_ratio"] = self.ui.dspin_box_link_size.value()
        cfg["auto_cone_size_factor"] = self.ui.dspin_box_auto_cone_size.value()
        cfg["camera_rotation"][0] = self.ui.dspin_box_rot_x.value()
        cfg["camera_rotation"][1] = self.ui.dspin_box_rot_y.value()
        cfg["camera_rotation"][2] = self.ui.dspin_box_rot_z.value()
        self.app_params.configuration = cfg
        self.show_advanced_options = self.ui.check_box_show_advanced.isChecked()

    def _run_trajectory_plot_algorithm(self):
        self.retrieve_info_from_ui()
        # viewer = geometry_builder.GeometryBuilder(self.app_params)
        # viewer.write_camera_trajectory_plot()
        self.display_in_app_message("Processing ...",
                                    f"loading trajectory and saving its plot to:\n{self.app_params.output_path}",
                                    True)
        # self.tmp_p()
        self.thread = Qc.QThread()
        self.traj_saver = TrajectoryWorker(self.app_params)
        self.traj_saver.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.traj_saver.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.traj_saver.complete.connect(self.thread.quit)
        self.traj_saver.complete.connect(self.traj_saver.deleteLater)
        self.traj_saver.show_msg.connect(self.display_in_app_message)

        # start the thread
        self.thread.start()

    def display_in_app_message(self, title, message, hide_go_back_button=False):
        self.ui.label_msg_title.setText(title)
        self.ui.label_msg_content.setText(message)
        self.ui.widget_main.setHidden(True)
        self.ui.widget_msg.setHidden(False)
        self.ui.btn_ok.setHidden(True)
        self.ui.btn_go_back.setHidden(hide_go_back_button)

    def _go_back_to_main_window(self):
        self.ui.widget_msg.setHidden(True)
        self.ui.btn_go_back.setHidden(True)
        self.ui.widget_main.setHidden(False)
        self.ui.btn_ok.setHidden(False)
        self.update_ui_elements()

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
