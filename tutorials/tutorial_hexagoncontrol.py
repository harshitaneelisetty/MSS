"""
    msui.tutorials.tutorial_hexagoncontrol.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This python script generates an automatic demonstration of how to create a hexagon flightrack with the waypoints.
    Placing a centre waypoint, how we can draw a perfect hexagon flight path around it with variable radius of
    hexagon and variable angle of first waypoint of the hexagon.
    This file is part of MSS.

    :copyright: Copyright 2021 Hrithik Kumar Verma
    :copyright: Copyright 2021-2023 by the MSS team, see AUTHORS.
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

import pyautogui as pag

from sys import platform
from pyscreeze import ImageNotFoundException
from tutorials.utils import platform_keys, start, finish
from tutorials.pictures import picture


def automate_hexagoncontrol():
    """
    This is the main automating script of the MSS hexagon control of table view which will be recorded and saved
    to a file having dateframe nomenclature with a .mp4 extension(codec).
    """
    # Giving time for loading of the MSS GUI.
    pag.sleep(5)
    tv_x = None
    tv_y = None

    ctrl, enter, win, alt = platform_keys()

    # Maximizing the window
    try:
        pag.hotkey('ctrl', 'command', 'f') if platform == 'darwin' else pag.hotkey(win, 'up')
    except Exception:
        print("\nException : Enable Shortcuts for your system or try again!")
        raise
    pag.sleep(2)
    pag.hotkey('ctrl', 'h')
    pag.sleep(3)

    # Changing map to Global
    try:
        x, y = pag.locateCenterOnScreen(picture('wms', 'europe_cyl.png'))
        pag.click(x, y, interval=2)
        pag.press('down', presses=2, interval=0.5)
        pag.press(enter, interval=1)
        pag.sleep(5)
    except (ImageNotFoundException, OSError, Exception):
        print("\n Exception : Map change dropdown could not be located on the screen")
        raise

    # Zooming into the map
    try:
        x, y = pag.locateCenterOnScreen(picture('wms', 'zoom.png'))
        pag.click(x, y, interval=2)
        pag.move(379, 205, duration=1)
        pag.dragRel(70, 75, duration=2)
        pag.sleep(5)
    except ImageNotFoundException:
        print("\n Exception : Zoom button could not be located on the screen")
        raise

    # Opening TableView
    pag.move(500, 0, duration=1)
    pag.click(duration=1)
    pag.sleep(1)
    pag.hotkey('ctrl', 't')
    pag.sleep(3)

    # Relocating Tableview by performing operations on table view
    try:
        x, y = pag.locateCenterOnScreen(picture('wms', 'selecttoopencontrol.png'))
        pag.moveTo(x + 250, y - 462, duration=1)
        if platform == 'linux' or platform == 'linux2':
            # the window need to be moved a bit below the topview window
            pag.dragRel(400, 387, duration=2)
        elif platform == 'win32' or platform == 'darwin':
            pag.dragRel(200, 487, duration=2)
        pag.sleep(2)
        if platform == 'linux' or platform == 'linux2':
            # this is to select over the window manager the topview and brings it on top
            # ToDo the help search function should be used for this (ctrl f)
            pag.keyDown('altleft')
            pag.press('tab')
            pag.keyUp('tab')
            pag.press('tab')
            pag.keyUp('tab')
            pag.keyUp('altleft')
        elif platform == 'win32':
            pag.keyDown('alt')
            pag.press('tab')
            pag.press('right')
            pag.keyUp('alt')
        elif platform == 'darwin':
            pag.keyDown('command')
            pag.press('tab')
            pag.press('right')
            pag.keyUp('command')
        pag.sleep(1)
        if platform == 'win32' or platform == 'darwin':
            pag.dragRel(None, -700, duration=2)
            tv_x, tv_y = pag.position()
        elif platform == 'linux' or platform == 'linux2':
            tv_x, tv_y = pag.position()
    except (ImageNotFoundException, OSError, TypeError, Exception):
        print("\nException : TableView's Select to open Control option not found on the screen.")
        raise

    # Opening Hexagon Control dockwidget
    if tv_x is not None and tv_y is not None:
        pag.moveTo(tv_x - 250, tv_y + 462, duration=2)
        pag.click(duration=2)
        pag.sleep(1)
        pag.press('down')
        pag.sleep(1)
        pag.press(enter)
        pag.sleep(2)

    # Entering Centre Latitude and Centre Longitude of Delhi around which hexagon will be drawn
    try:
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'center_latitude.png'))
        pag.sleep(1)
        pag.click(x + 370, y, duration=2)
        pag.sleep(1)
        pag.hotkey(ctrl, 'a')
        pag.sleep(1)
        pag.typewrite('28.57', interval=0.3)
        pag.sleep(1)
        pag.press(enter)

        pag.sleep(1)
        pag.click(x + 943, y, duration=2)
        pag.sleep(1)
        pag.hotkey(ctrl, 'a')
        pag.sleep(1)
        pag.typewrite('77.10', interval=0.3)
        pag.sleep(1)
        pag.press(enter)
    except (ImageNotFoundException, OSError, Exception):
        print("\nException :\'Center Latitude\' button not found on the screen.")
        raise

    # Clicking on the add hexagon button
    try:
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'add_hexagon.png'))
        pag.click(x, y, duration=2)
        pag.sleep(3)
    except (ImageNotFoundException, OSError, Exception):
        print("\nException :\'Add Hexagon\' button not found on the screen.")
        raise

    # Changing the Radius of the hexagon
    try:
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'radius.png'))
        pag.click(x + 400, y, duration=2)
        pag.sleep(1)
        pag.hotkey(ctrl, 'a')
        pag.sleep(1)
        pag.typewrite('500.00', interval=0.3)
        pag.sleep(1)
        pag.press(enter)
    except (ImageNotFoundException, OSError, Exception):
        print("\nException :\'Radius\' button not found on the screen.")
        raise

    # Clicking on the Remove Hexagon Button
    try:
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'remove_hexagon.png'))
        pag.click(x, y, duration=2)
        pag.sleep(2)
        pag.press('left')
        pag.sleep(1)
        pag.press(enter)
        pag.sleep(2)
    except (ImageNotFoundException, OSError, Exception):
        print("\nException :\'Remove Hexagon\' button not found on the screen.")
        raise

    # Clicking on the add hexagon button
    try:
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'add_hexagon.png'))
        pag.click(x, y, duration=2)
        pag.sleep(3)
    except (ImageNotFoundException, OSError, Exception):
        print("\nException :\'Add Hexagon\' button not found on the screen.")
        raise

    # Changing the angle of first point of the hexagon
    try:
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'radius.png'))
        pag.sleep(1)
        pag.click(x + 967, y, duration=2)
        pag.sleep(1)
        pag.hotkey(ctrl, 'a')
        pag.sleep(1)
        pag.typewrite('90.00', interval=0.3)
        pag.sleep(1)
        pag.press(enter)

        # Clicking on the Remove Hexagon Button
        try:
            x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'remove_hexagon.png'))
            pag.click(x, y, duration=2)
            pag.sleep(2)
            pag.press('left')
            pag.sleep(1)
            pag.press(enter)
            pag.sleep(2)
        except (ImageNotFoundException, OSError, Exception):
            print("\nException :\'Remove Hexagon\' button not found on the screen.")
            raise

        # Clicking on the add hexagon button
        try:
            x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'add_hexagon.png'))
            pag.click(x, y, duration=2)
            pag.sleep(3)
        except (ImageNotFoundException, OSError, Exception):
            print("\nException :\'Add Hexagon\' button not found on the screen.")
            raise

        # Changing to a different angle of first point
        x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'radius.png'))
        pag.sleep(1)
        pag.click(x + 967, y, duration=2)
        pag.sleep(1)
        pag.hotkey(ctrl, 'a')
        pag.sleep(1)
        pag.typewrite('120.00', interval=0.3)
        pag.sleep(1)
        pag.press(enter)

        # Clicking on the Remove Hexagon Button
        try:
            x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'remove_hexagon.png'))
            pag.click(x, y, duration=2)
            pag.sleep(2)
            pag.press('left')
            pag.sleep(1)
            pag.press(enter)
            pag.sleep(2)
        except (ImageNotFoundException, OSError, Exception):
            print("\nException :\'Remove Hexagon\' button not found on the screen.")
            raise

        # Clicking on the add hexagon button
        try:
            x, y = pag.locateCenterOnScreen(picture('hexagoncontrol', 'add_hexagon.png'))
            pag.click(x, y, duration=2)
            pag.sleep(3)
        except (ImageNotFoundException, OSError, Exception):
            print("\nException :\'Add Hexagon\' button not found on the screen.")
            raise
    except (ImageNotFoundException, OSError, Exception):
        print("\nException :\'Radius (for Angle of first point)\' button not found on the screen.")
        raise

    pag.moveTo(tv_x, tv_y, duration=2)
    pag.click(duration=2)

    print("\nAutomation is over for this tutorial. Watch next tutorial for other functions.")
    finish()


if __name__ == '__main__':
    start(target=automate_hexagoncontrol, duration=170)
