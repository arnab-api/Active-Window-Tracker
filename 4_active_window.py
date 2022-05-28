import pyscreenshot as ImageGrab

import time
from collections import namedtuple

import Xlib
import Xlib.display
# import imutils
import cv2
import numpy as np
import matplotlib.pyplot as plt


disp = Xlib.display.Display()
root = disp.screen().root

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
MyGeom = namedtuple('MyGeom', 'x y height width')


def get_active_window():
    win_id = root.get_full_property(NET_ACTIVE_WINDOW,
                                    Xlib.X.AnyPropertyType).value[0]
    try:
        return disp.create_resource_object('window', win_id)
    except Xlib.error.XError:
        pass


def get_absolute_geometry(win):
    """
    Returns the (x, y, height, width) of a window relative to the top-left
    of the screen.
    """
    geom = win.get_geometry()
    (x, y) = (geom.x, geom.y)
    while True:
        parent = win.query_tree().parent
        pgeom = parent.get_geometry()
        x += pgeom.x
        y += pgeom.y
        if parent.id == root.id:
            break
        win = parent
    return MyGeom(x, y, geom.height, geom.width)


def get_window_bbox(win):
    """
    Returns (x1, y1, x2, y2) relative to the top-left of the screen.
    """
    geom = get_absolute_geometry(win)
    x1 = geom.x
    y1 = geom.y
    x2 = x1 + geom.width
    y2 = y1 + geom.height
    return (x1, y1, x2, y2)


image_dims = (854, 480)

image = ImageGrab.grab()
image = np.array(image)
# image = imutils.resize(image, width=1080)
image = cv2.resize(image, image_dims)
cv2.namedWindow("Tracker")
print(type(image))
cv2.imshow("Tracker", image)

while True:
    # Protect against races when the window gets destroyed before we
    # have a chance to use it.  Guessing there's a way to lock access
    # to the resource, but for this demo we're just punting.  Good
    # enough for who it's for.
    try:
        win = get_active_window()
        bbox = get_window_bbox(win)
        print(win.get_wm_name(), bbox)

        cv2.imshow("Tracker", image)
        image = ImageGrab.grab(bbox=bbox)
        image = np.array(image)
        # image = imutils.resize(image, width=1080)
        image = cv2.resize(image, image_dims)

        key = cv2.waitKey(10)
        if key == 27: # exit on ESC
            break

    except Xlib.error.BadWindow:
        print("Window vanished")
    time.sleep(.1)

cv2.destroyWindow("Tracker")
