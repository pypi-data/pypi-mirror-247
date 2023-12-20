# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl

import PyQt6.QtCore as qtcr
import PyQt6.QtWidgets as wdgt

from pyvispr.config.appearance.color import color_e
from pyvispr.config.main import TITLE
from pyvispr.interface.window.messenger import CreateMessageCanal
from pyvispr.interface.window.widget.function_list import function_list_wgt_t
from pyvispr.interface.window.widget.module_list import module_list_wgt_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class installer_wdw_t(wdgt.QMainWindow):
    def __post_init__(self) -> None:
        """"""
        wdgt.QMainWindow.__init__(self)
        self.setWindowTitle(f"{TITLE} - Node Installer")

        single = wdgt.QWidget()
        select = wdgt.QPushButton("Select Python File")
        drop = wdgt.QLabel("Drop Python File")
        drop.setAlignment(qtcr.Qt.AlignmentFlag.AlignCenter)
        drop.setStyleSheet(f"background-color: {color_e.lightgray.name()};")
        layout = wdgt.QHBoxLayout()
        layout.addWidget(select)
        layout.addWidget(drop)
        single.setLayout(layout)

        multiple = wdgt.QWidget()
        select = wdgt.QPushButton("Select Base Folder")
        drop = wdgt.QLabel("Drop Base Folder")
        drop.setAlignment(qtcr.Qt.AlignmentFlag.AlignCenter)
        drop.setStyleSheet(f"background-color: {color_e.lightgray.name()};")
        layout = wdgt.QHBoxLayout()
        layout.addWidget(select)
        layout.addWidget(drop)
        multiple.setLayout(layout)

        system = wdgt.QWidget()
        module_list = module_list_wgt_t(element_name="Modules")
        function_list = function_list_wgt_t(element_name="Functions")
        layout = wdgt.QGridLayout()
        layout.addWidget(module_list, 1, 1, alignment=qtcr.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(
            module_list.filter_wgt, 2, 1, alignment=qtcr.Qt.AlignmentFlag.AlignLeft
        )
        layout.addWidget(function_list, 1, 2, alignment=qtcr.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(
            function_list.filter_wgt, 2, 2, alignment=qtcr.Qt.AlignmentFlag.AlignLeft
        )
        system.setLayout(layout)

        tabs = wdgt.QTabWidget(self)
        for widget, name in (
            (single, "Single"),
            (multiple, "Batch (User)"),
            (system, "Batch (System)"),
        ):
            tabs.addTab(widget, name)

        done = wdgt.QPushButton("Done")
        CreateMessageCanal(done, "clicked", self.close)

        layout = wdgt.QVBoxLayout()
        layout.addWidget(tabs)
        layout.addWidget(done)

        central = wdgt.QWidget(self)
        central.setLayout(layout)
        self.setCentralWidget(central)
