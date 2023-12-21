from loguru import logger
import qtawesome as qta
from typing import Dict
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize

from . import app_globals as ag

toolbar_icons = {}
other_icons = {}


def collect_all_icons():
    _collect_toolbar_icons()

    sz = QSize(16, 16)
    tmp1 = qta.icon('mdi.circle', color="#00FF00")
    tmp2 = qta.icon('mdi.circle', color="#FF0000")
    other_icons["busy"] = (tmp1.pixmap(sz), tmp2.pixmap(sz))

    other_icons["link"] = (qta.icon('mdi.alpha-l', color=ag.qss_params["$LimeGreen"], scale_factor = 2),)
    other_icons["folder"] = (qta.icon('mdi.alpha-f', color=ag.qss_params["$LimeGreen"], scale_factor = 2),)
    other_icons["hidden"] = (qta.icon('mdi.alpha-h', color=ag.qss_params["$LimeGreen"], scale_factor = 2),)

    other_icons["ok"] = (qta.icon('mdi.check', color=ag.qss_params["$LimeGreen"]),)
    other_icons["cancel2"] = (qta.icon('mdi.window-close', color=ag.qss_params["$CarmineColor"]),)

    other_icons["toEdit"] = (qta.icon('mdi.pencil-outline', color=ag.qss_params["$navigatorColor"]),)
    other_icons["plus"] = (qta.icon('mdi.plus', color=ag.qss_params["$navigatorColor"]),)

    other_icons["right"] = (qta.icon('mdi.chevron-right', color=ag.qss_params["$navigatorColor"]),)
    other_icons["down"] = (qta.icon('mdi.chevron-down', color=ag.qss_params["$navigatorColor"]),)
    other_icons["up"] = (qta.icon('mdi.chevron-up', color=ag.qss_params["$navigatorColor"]),)
    other_icons["collapse_all"] = (qta.icon('mdi.collapse-all-outline', color=ag.qss_params["$topBarColor"]),)
    other_icons["refresh"] = (qta.icon('mdi.refresh', color=ag.qss_params["$topBarColor"]),)
    other_icons["open_db"] = (qta.icon('mdi.folder-open-outline', color=ag.qss_params["$topBarColor"]),)
    other_icons["more"] = (qta.icon('mdi.dots-horizontal', color=ag.qss_params["$topBarColor"]),)
    other_icons["remove_btn"] = (qta.icon('mdi.close', color=ag.qss_params["$dialogBackground"],
        color_active=ag.qss_params["$dialogInputEditColor"]),)
    other_icons["prev_folder"] = (qta.icon('mdi.arrow-left',),)
    other_icons["next_folder"] = (qta.icon('mdi.arrow-right',),)
    other_icons["show_hide"] = (
        qta.icon('mdi.checkbox-blank-outline', color=ag.qss_params["$topBarColor"]),
        qta.icon('mdi.checkbox-marked-outline', color=ag.qss_params["$topBarColor"]),
    )

def _collect_toolbar_icons():
    # global icons
    toolbar_icons["btnDir"] = (
        qta.icon('mdi.tree-outline', color=ag.qss_params["$ToolButtonColor"],
            color_active=ag.qss_params["$ToolButtonActiveColor"], scale_factor = 1.3),
        qta.icon('mdi.tree-outline', color=ag.qss_params["$ToolButtonActiveColor"], scale_factor = 1.3)
    )

    toolbar_icons["btnFilter"] = (
        qta.icon('mdi.filter-variant', color=ag.qss_params["$ToolButtonColor"],
            color_active=ag.qss_params["$ToolButtonActiveColor"]),
        qta.icon('mdi.filter-variant', color=ag.qss_params["$ToolButtonActiveColor"])
    )

    names_ = ('mdi.filter-variant', 'mdi.cog-outline')
    opt_ = {'options':[{'scale_factor': 1.0,
                        'offset': (-0.1, 0.0)},
                    {'scale_factor': 0.5,
                        'offset': (0.3, 0.2)}]
    }
    toolbar_icons["btnFilterSetup"] = (
        qta.icon(*names_, **(opt_ | {'color': ag.qss_params["$ToolButtonColor"],
                                    'color_active': ag.qss_params["$ToolButtonActiveColor"]})),
        qta.icon(*names_, **(opt_ | {'color': ag.qss_params["$ToolButtonActiveColor"]})),
    )

    toolbar_icons["btnToggleBar"] = (
        qta.icon('mdi.chevron-left', color=ag.qss_params["$ToolButtonColor"],
            color_active=ag.qss_params["$ToolButtonActiveColor"], scale_factor = 1.3),
        qta.icon('mdi.chevron-right', color=ag.qss_params["$ToolButtonColor"],
            color_active=ag.qss_params["$ToolButtonActiveColor"], scale_factor = 1.3),
    )

    toolbar_icons["btnSetup"] = (
        qta.icon('mdi.menu', color=ag.qss_params["$ToolButtonColor"],
            color_active=ag.qss_params["$ToolButtonActiveColor"]),
    )

    toolbar_icons["field_menu"] = (
        qta.icon('mdi.dots-horizontal', color=ag.qss_params["$topBarColor"]),
    )

def get_other_icon(key: str, index: int = 0) -> QIcon|QPixmap:
    return other_icons[key][index]

def add_other_icon(key: str, pict: QPixmap):
    ico = QIcon()
    ico.addPixmap(pict)
    other_icons[key] = (ico,)

def get_toolbar_icons() -> Dict:
    return toolbar_icons

def get_toolbar_icon(key: str, idx: int=0) -> QIcon:
    return toolbar_icons[key][idx]
