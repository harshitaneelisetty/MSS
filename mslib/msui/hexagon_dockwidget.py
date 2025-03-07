# -*- coding: utf-8 -*-
"""

    mslib.msui.hexagon_dockwidget
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Control widget to configure remote sensing overlays.

    This file is part of MSS.

    :copyright: Copyright 2016-2017 Joern Ungermann, Stefan Ensmann
    :copyright: Copyright 2016-2023 by the MSS team, see AUTHORS.
    :license: APACHE-2.0, see LICENSE for details.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import numpy as np
import logging

from PyQt5 import QtWidgets
from mslib.utils.qt import ui_hexagon_dockwidget as ui
from mslib.msui import flighttrack as ft
from mslib.utils.coordinate import rotate_point
from mslib.utils.config import config_loader


class HexagonException(Exception):
    def __init__(self, error_string):
        logging.debug("%s", error_string)


def create_hexagon(center_lat, center_lon, radius, angle=0., clockwise=True):
    coords = (radius, 0.)
    coords_cart = [rotate_point(coords, angle=_a + angle) for _a in range(0, 361, 60)]
    if not clockwise:
        coords_cart.reverse()
    coords_sphere = [
        (center_lat + (_x / 110.),
         center_lon + (_y / (110. * np.cos(np.deg2rad((_x / 110.) + center_lat)))))
        for _x, _y in coords_cart]
    return coords_sphere


class HexagonControlWidget(QtWidgets.QWidget, ui.Ui_HexagonDockWidget):
    """
    This class implements the remote sensing functionality as dockable widget.
    """

    def __init__(self, parent=None, view=None):
        """
        Arguments:
        parent -- Qt widget that is parent to this widget.
        view -- reference to mpl canvas class
        """
        super(HexagonControlWidget, self).__init__(parent)
        self.setupUi(self)
        self.view = view
        if self.view:
            self.view.tableWayPoints.selectionModel().selectionChanged.connect(self.on_selection_changed)
            self.on_selection_changed(None)

        self.dsbHexgaonRadius.setValue(200)

        self.pbAddHexagon.clicked.connect(self._add_hexagon)
        self.pbRemoveHexagon.clicked.connect(self._remove_hexagon)

    def on_selection_changed(self, index):
        """
        Disables add and remove when multiple rows are selected
        """
        enable = len(self.view.tableWayPoints.selectionModel().selectedRows()) <= 1
        self.pbAddHexagon.setEnabled(enable)
        self.pbRemoveHexagon.setEnabled(enable)

    def _get_parameters(self):
        return {
            "center_lon": self.dsbHexagonLongitude.value(),
            "center_lat": self.dsbHexagonLatitude.value(),
            "radius": self.dsbHexgaonRadius.value(),
            "angle": self.dsbHexagonAngle.value(),
            "direction": self.cbClock.currentText(),
        }

    def _add_hexagon(self):
        table_view = self.view.tableWayPoints
        waypoints_model = self.view.waypoints_model
        params = self._get_parameters()

        if params["radius"] < 0.01:
            QtWidgets.QMessageBox.warning(
                self, "Add hexagon", "You cannot create a hexagon with zero radius!")
            return
        points = create_hexagon(params["center_lat"], params["center_lon"], params["radius"],
                                params["angle"], params["direction"] == "clockwise")
        index = table_view.currentIndex()
        if not index.isValid():
            row = 0
            flightlevel = config_loader(dataset="new_flighttrack_flightlevel")
        else:
            row = index.row() + 1
            flightlevel = waypoints_model.waypoint_data(row - 1).flightlevel
        waypoints = []
        for i, point in enumerate(points):
            waypoints.append(
                ft.Waypoint(lon=float(point[1]), lat=float(point[0]),
                            flightlevel=float(flightlevel), comments=f"Hexagon {(i + 1):d}"))
        waypoints_model.insertRows(row, rows=len(waypoints), waypoints=waypoints)
        index = waypoints_model.index(row, 0)
        table_view.setCurrentIndex(index)
        table_view.resizeRowsToContents()

    def _remove_hexagon(self):
        table_view = self.view.tableWayPoints
        waypoints_model = self.view.waypoints_model

        index = table_view.currentIndex()

        try:
            if not index.isValid():
                raise HexagonException("A waypoint of the hexagon must be selected.")
            row = index.row()
            comm = str(waypoints_model.waypoint_data(row).comments)
            if len(comm) == 9 and comm.startswith("Hexagon "):
                if (len(waypoints_model.all_waypoint_data()) - 7) < 2:  # = 3 waypoints + 7 hexagon points
                    raise HexagonException("Cannot remove hexagon, the flight track needs to consist "
                                           "of at least two points.")
                idx = int(comm[-1])
                row_min = row - (idx - 1)
                row_max = row + (7 - idx)
                if row_min < 0 or row_max > len(waypoints_model.all_waypoint_data()):
                    raise HexagonException("Cannot remove hexagon, hexagon is not complete "
                                           f"min, max = {row_min:d}, {row_max:d}")
                else:
                    found_one = False
                    for i in range(0, row_max - row_min):
                        if str(waypoints_model.waypoint_data(row_min + i).comments) != f"Hexagon {(i + 1):d}":
                            found_one = True
                            break
                    if found_one:
                        raise HexagonException("Cannot remove hexagon, hexagon comments are not found in all "
                                               f"points (min, max = {row_min:d}, {row_max:d})")
                    else:
                        sel = QtWidgets.QMessageBox.question(
                            None, "Remove hexagon",
                            f"This will remove waypoints {row_min:d}-{row_max:d}. Continue?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                            QtWidgets.QMessageBox.Yes)
                        if sel == QtWidgets.QMessageBox.Yes:
                            waypoints_model.removeRows(row_min, rows=7)
            else:
                raise HexagonException("Cannot remove hexagon, please select a hexagon "
                                       "waypoint ('Hexagon x' in comments field)")
        except HexagonException as ex:
            QtWidgets.QMessageBox.warning(self, "Remove hexagon", str(ex))
