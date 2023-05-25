import colorsys


def change_lightness(in_hex_color, in_added_lightness):
    c_hex = in_hex_color.lstrip('#')
    lv = len(c_hex)
    r, g, b = tuple(int(c_hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    n_l = l + in_added_lightness
    n_l = max(0, min(1, n_l))
    r, g, b = colorsys.hls_to_rgb(h, n_l, s)
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))


TEXT_COLOR = "#2f3337"   # "#ff0066"  2f3337
TEXT_DISABLED_COLOR = change_lightness(TEXT_COLOR, 0.3)

BG_COLOR = "#f3f3f2"  # 99ccff   f3f3f2
BG_ENTRY_COLOR = change_lightness(BG_COLOR, 0.03)
BG_DISABLED_COLOR = change_lightness(BG_COLOR, -0.1)
BORDERS_COLOR = "#b4b4b4"  # "#b4b4b4"   00ff66
ALMOST_TRANSPARENT_COLOR = "rgba(150, 150, 150, 2)"

FOCUS_COLOR = "#9c9cc9"

PROGRESS_COLOR = change_lightness(FOCUS_COLOR, 0.15)
PROGRESS_LIGHT_COLOR = change_lightness(FOCUS_COLOR, 0.18)

FRAME_COLOR = change_lightness(BG_COLOR, -0.05)

BOX_HOVER_COLOR = change_lightness(BG_COLOR, -0.08)
BOX_CHECKED_COLOR = FRAME_COLOR
BOX_FOCUS_COLOR = FOCUS_COLOR

BTN_COLOR = BG_COLOR
BTN_LIGHT_COLOR = change_lightness(BTN_COLOR, 0.05)
BTN_DARK_COLOR = change_lightness(BTN_COLOR, -0.05)
BTN_DARKER_COLOR = change_lightness(BTN_COLOR, -0.1)
BTN_DARKEST_COLOR = change_lightness(BTN_COLOR, -0.2)

BTN_ACTION_COLOR = "#eff8e8"
BTN_ACTION_LIGHT_COLOR = change_lightness(BTN_ACTION_COLOR, 0.05)
BTN_ACTION_DARK_COLOR = change_lightness(BTN_ACTION_COLOR, -0.05)
BTN_ACTION_DARKER_COLOR = change_lightness(BTN_ACTION_COLOR, -0.1)
BTN_ACTION_DARKEST_COLOR = change_lightness(BTN_ACTION_COLOR, -0.2)

BTN_DANGER_COLOR = "#f8e8e8"
BTN_DANGER_LIGHT_COLOR = change_lightness(BTN_DANGER_COLOR, 0.05)
BTN_DANGER_DARK_COLOR = change_lightness(BTN_DANGER_COLOR, -0.05)
BTN_DANGER_DARKER_COLOR = change_lightness(BTN_DANGER_COLOR, -0.1)
BTN_DANGER_DARKEST_COLOR = change_lightness(BTN_DANGER_COLOR, -0.2)

APP_STYLESHEET = f"""

QMainWindow {{
    background-color: {BG_COLOR};
}}

/* -----+-----+-----+----- */
QPushButton, QToolButton, QComboBox {{
    color: {TEXT_COLOR};
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 {BTN_COLOR}, stop:1 {BTN_DARK_COLOR});
    border-radius:3px; 
    border: solid {BTN_DARKEST_COLOR}; 
    border-width: 1px 2px 2px 1px;
    padding: 4px 14px 4px 14px; 
}}

QPushButton:hover , QToolButton:hover , QComboBox:hover {{
    background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 {BTN_LIGHT_COLOR}, stop:1 {BTN_COLOR});
}}
QPushButton:disabled , QToolButton:disabled , QComboBox:disabled {{
    background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 {BTN_DARK_COLOR}, stop:1 {BTN_DARKER_COLOR});
    border: solid {BTN_DARKEST_COLOR};
    border-width: 1px 2px 2px 1px;
    color: {TEXT_DISABLED_COLOR};
}}
QPushButton:pressed , QToolButton:pressed  {{background-color: {BTN_DARKER_COLOR};}}
QToolButton {{ padding: 2px 5px 2px 5px; }}
/* -----+-----+-----+----- */

QComboBox::down-arrow {{
    border-style: double;
    margin-top: 4px;
    border: 6px solid {ALMOST_TRANSPARENT_COLOR};
    border-top: 6px solid {BORDERS_COLOR};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: {BORDERS_COLOR};
    border-left-style: solid;
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}}
QListView {{
    margin: 0px;
    background-color: {BG_COLOR}; 
    border: 1px solid {BORDERS_COLOR};
}}

QComboBox:selected{{
    background-color: {FOCUS_COLOR}; 
}}

/* -----+-----+-----+----- */
QLineEdit, QSpinBox, QDoubleSpinBox{{
    border: solid {BORDERS_COLOR}; 
    border-width: 1; 
    border-radius: 4;
    background-color: {BG_ENTRY_COLOR};
    padding: 2px 0px 2px 0px;
    color: {TEXT_COLOR};
    selection-background-color: {FOCUS_COLOR};
    selection-color: {BG_ENTRY_COLOR};
}}
QLineEdit::disabled, QSpinBox::disabled, QDoubleSpinBox:disabled {{
    background-color: {BG_DISABLED_COLOR}; 
    color: {TEXT_DISABLED_COLOR}; 
}}
QLineEdit::focus, QSpinBox::focus, QDoubleSpinBox:focus {{
    border-color: {FOCUS_COLOR}; 
    border-width: 1.55;
}}
/* -----+-----+-----+----- */
QSpinBox::up-button, QDoubleSpinBox::up-button{{
    background-color: {ALMOST_TRANSPARENT_COLOR};
    height: 12.5px;
    border: 1px solid {ALMOST_TRANSPARENT_COLOR};
    border-left-color: {BORDERS_COLOR};
    padding: 3px;
    padding-top: -3px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background-color: {ALMOST_TRANSPARENT_COLOR};
    height: 12.5px;
    border: 1px solid {ALMOST_TRANSPARENT_COLOR};
    border-left-color: {BORDERS_COLOR};
    padding: 3px;
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    border-style: double;
    margin-top: 0px;
    border: 4px solid {ALMOST_TRANSPARENT_COLOR};
    border-bottom: 4px solid {BORDERS_COLOR};
}}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    border-style: double;
    margin-top: 7px;
    border: 4px solid {ALMOST_TRANSPARENT_COLOR};
    border-top: 4px solid {BORDERS_COLOR};
}}
QSpinBox::up-arrow::pressed, QDoubleSpinBox::up-arrow::pressed {{
    border-bottom: 4px solid {TEXT_COLOR};
}}
QSpinBox::down-arrow::pressed, QDoubleSpinBox::down-arrow::pressed {{
    border-top: 4px solid {TEXT_COLOR};
}}
/* -----+-----+-----+----- */

QTextEdit, QPlainTextEdit{{
    border: solid {BORDERS_COLOR}; 
    border-width: 1; 
    border-radius: 4;
    background-color: {BG_ENTRY_COLOR};
    padding: 2px 1px 2px 0px;
    color: {TEXT_COLOR};
    selection-background-color: {FOCUS_COLOR};
    selection-color: {BG_ENTRY_COLOR};
}}
QTextEdit:disabled, QPlainTextEdit:disabled {{
    background-color: {BG_DISABLED_COLOR}; 
    color: {TEXT_DISABLED_COLOR}; 
}}
QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {FOCUS_COLOR}; 
    border-width: 1.55;
}}

/* -----+-----+-----+----- */

QLabel {{
    color: {TEXT_COLOR};    
}}
QLabel::disabled {{ color: {TEXT_DISABLED_COLOR};}}
/* -----+-----+-----+----- */

QProgressBar {{
    text-align: center;
    color: {TEXT_COLOR};
    border: solid {BORDERS_COLOR};
    border-width: 1px; 
    border-radius: 4px;
    background-color: {BG_ENTRY_COLOR};
}}
QProgressBar::chunk {{
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 {PROGRESS_COLOR}, stop:1 {PROGRESS_LIGHT_COLOR});
    border-radius: 4px;
}}
/* -----+-----+-----+----- */

QTabWidget {{
    color: {TEXT_COLOR};
    background-color:{BG_COLOR};
}}
QTabWidget::pane {{
        border-color: {BORDERS_COLOR};
        background-color: {BG_COLOR};
        border-style: solid;
        border-width: 1px;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
}}

QTabBar::tab {{
    padding: 4px 14px 4px 14px;
    color: {TEXT_COLOR};
    background-color: {BG_DISABLED_COLOR};
    border-style: solid;
    border-width: 1px 1px 0px 1px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border-color: {BORDERS_COLOR}; 

    border-bottom-color: {BG_COLOR};
}}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {{
      background-color: {BG_COLOR};
}}
QTabBar::tab:!selected {{
        margin-top: 5px;
}}
/* -----+-----+-----+----- */

QCheckBox , QRadioButton {{
    color: {TEXT_COLOR};
    padding: 2px 10px 2px 10px;
}}

QCheckBox:disabled , QRadioButton:disabled {{
    color: {TEXT_DISABLED_COLOR};
}}

QCheckBox:hover , QRadioButton::hover{{
    border-radius:4px;
    border-style:solid;
    border-width:1px;
    border-color: {BORDERS_COLOR};
    background-color: {BOX_HOVER_COLOR};
}}
QCheckBox::indicator {{
    border-radius:2px;
    border-style:solid;
    border-width:1px;
    border-color: {BORDERS_COLOR};
    background-color: {BG_ENTRY_COLOR}; 
}}

QRadioButton::indicator {{
    border-radius: 7px;
    border-style:solid;
    border-width:1px;
    border-color: {BORDERS_COLOR};
    background-color: {BG_ENTRY_COLOR}; 
}}
QCheckBox::indicator:pressed , QRadioButton::indicator:pressed {{ background-color: {FRAME_COLOR}; }}

QCheckBox::indicator:checked {{
    background-color: qradialgradient(spread:repeat,  cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
    stop:0 {BOX_FOCUS_COLOR}, stop:0.499 {BOX_FOCUS_COLOR},  stop:0.5 {BOX_CHECKED_COLOR}, stop:1 {BOX_CHECKED_COLOR}); 
    /* background-color: qlineargradient(spread: pad, x0:0.0, y0:0.0, x1:0.0, y1:1.0, stop: 0.5 red, stop: 1 qlineargradient(spread: pad, x0:0.0, y0:0.0, x1:1.0, y1:0.0, stop: 0.5 green, stop: 1 yellow)); */

}}
QRadioButton::indicator:checked {{
    background-color: qradialgradient(spread:repeat,  cx:0.5, cy:0.5, radius:0.6, fx:0.5, fy:0.5,
    stop:0 {BOX_FOCUS_COLOR}, stop:0.4 {BOX_FOCUS_COLOR},  stop:0.6 {BOX_CHECKED_COLOR}, stop:1 {BOX_CHECKED_COLOR});
}}

/* -----+-----+-----+----- */

QGroupBox {{
    color: {TEXT_COLOR};
    background-color: {FRAME_COLOR};
    border: solid {BORDERS_COLOR};
    border-width: 1px; 
    border-radius: 4px;
    margin-top: 25px;
}}
QGroupBox:disabled {{
    color: {TEXT_DISABLED_COLOR};
}}
QGroupBox::title {{color: {TEXT_COLOR};}}
QGroupBox::title::disabled {{color: {TEXT_DISABLED_COLOR};}}
/* -----+-----+-----+----- */

QFrame[cssClass="highlight"] {{
    background-color: {FRAME_COLOR};
    border: solid {BORDERS_COLOR};
    border-width: 1px; 
    border-radius: 4px;
}}
/* -----+-----+-----+----- */
QPushButton[cssClass="action"], QToolButton[cssClass="action"], QComboBox[cssClass="action"] {{
    border-color: {BTN_ACTION_DARKEST_COLOR};
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 {BTN_ACTION_COLOR}, stop:1 {BTN_ACTION_DARK_COLOR});
}}

QPushButton[cssClass="action"]:hover , QToolButton[cssClass="action"]:hover , QComboBox[cssClass="action"]:hover {{
    background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 {BTN_ACTION_LIGHT_COLOR}, stop:1 {BTN_ACTION_COLOR});
}}
QPushButton[cssClass="action"]:pressed , QToolButton[cssClass="action"]:pressed {{
    background-color: {BTN_ACTION_DARKER_COLOR};
}}
/* -----+-----+-----+----- */
QPushButton[cssClass="danger"], QToolButton[cssClass="danger"], QComboBox[cssClass="danger"] {{
    border-color: {BTN_DANGER_DARKEST_COLOR};
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 {BTN_DANGER_COLOR}, stop:1 {BTN_DANGER_DARK_COLOR});
}}

QPushButton[cssClass="danger"]:hover , QToolButton[cssClass="danger"]:hover , QComboBox[cssClass="danger"]:hover {{
    background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 {BTN_DANGER_LIGHT_COLOR}, stop:1 {BTN_DANGER_COLOR});
}}
QPushButton[cssClass="danger"]:pressed , QToolButton[cssClass="danger"]:pressed {{
    background-color: {BTN_DANGER_DARKER_COLOR};
}}


QStatusBar {{
    color: {BG_COLOR};
}}
/* TODO: support for [QMenuBar, QMenuBar::item, QMenuBar::item:selected, QMenu, QMenu::item, QMenu::item:selected] */

"""
