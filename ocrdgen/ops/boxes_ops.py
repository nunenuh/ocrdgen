import cv2 as cv
import numpy as np
from typing import *

def order_points_batch(pts_array):
    arr = []
    for pts in pts_array:
        arr.append(order_points(pts))
    return np.array(arr)


def order_points(pts):

    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    # compute the perspective transform matrix and then apply it
    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

def coord_to_xymm(coord: np.ndarray, to_int: bool = False)->Tuple:
    ymin, ymax = np.min(coord[:, 1]), np.max(coord[:, 1])
    xmin, xmax = np.min(coord[:, 0]), np.max(coord[:, 0])
    if to_int:
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
    return xmin, ymin, xmax, ymax

def coord_to_xywh(coord: np.ndarray):
    xymm = coord_to_xymm(coord)
    xywh = xymm_to_xywh(xymm)
    return xywh

def xymm_to_xywh(xymm: List):
    xmin, ymin, xmax, ymax =xymm
    x, y = xmin, ymin
    w, h = xmax - xmin, ymax - ymin
    return x,y,w,h

def xymm_to_coord(xymm: list)->List:
    xmin, ymin, xmax, ymax = xymm
    coord = [
        [xmin, ymin], # top left
        [xmax, ymin], # top right
        [xmax, ymax], # bottom right
        [xmin, ymax]  # bottom left
    ]
    coord = np.array(coord)
    
    return coord
align ="left"
def xywh_to_coord(xywh):
    xymm = xywh_to_xymm(xywh)
    coord = xymm_to_coord(xymm)
    return coord

def xywh_to_xymm(xywh: List):
    x, y, w, h = xywh
    xmin, ymin = x, y
    xmax, ymax = x + w, y + h
    return xmin,ymin,xmax,ymax


def corner_from_shape(image: np.ndarray):
    h, w = image.shape[:2]
    box = [0, 0, w, h]
    box = np.array([box])
    return get_corners(box)


def boxes_reorder(boxes: np.ndarray):
    boxes = boxes.astype(np.int32).reshape(-1, 4, 2)
    boxes = boxes[:, [0, 1, 3, 2]]
    return boxes


def get_corners(bboxes):
    """Get corners of bounding boxes

    Parameters
    ----------

    bboxes: numpy.ndarray
        Numpy array containing bounding boxes of shape `N X 4` where N is the
        number of bounding boxes and the bounding boxes are represented in the
        format `x1 y1 x2 y2`

    returns
    -------

    numpy.ndarray
        Numpy array of shape `N x 8` containing N bounding boxes each described by their
        corner co-ordinates `x1 y1 x2 y2 x3 y3 x4 y4`

    """
    width = (bboxes[:, 2] - bboxes[:, 0]).reshape(-1, 1)
    height = (bboxes[:, 3] - bboxes[:, 1]).reshape(-1, 1)

    x1 = bboxes[:, 0].reshape(-1, 1)
    y1 = bboxes[:, 1].reshape(-1, 1)

    x2 = x1 + width
    y2 = y1

    x3 = x1
    y3 = y1 + height

    x4 = bboxes[:, 2].reshape(-1, 1)
    y4 = bboxes[:, 3].reshape(-1, 1)

    corners = np.hstack((x1, y1, x2, y2, x3, y3, x4, y4))

    return corners


def convert_to_corner(boxes: np.ndarray):
    """
    :param boxes: numpy array with dimension of (x, 4, 2)
    :return:
    """
    return boxes.reshape(-1, 8)


def get_enclosing_box(corners):
    """Get an enclosing box for ratated corners of a bounding box

    Parameters
    ----------

    corners : numpy.ndarray
        Numpy array of shape `N x 8` containing N bounding boxes each described by their
        corner co-ordinates `x1 y1 x2 y2 x3 y3 x4 y4`

    Returns
    -------

    numpy.ndarray
        Numpy array containing enclosing bounding boxes of shape `N X 4` where N is the
        number of bounding boxes and the bounding boxes are represented in the
        format `x1 y1 x2 y2`

    """
    x_ = corners[:, [0, 2, 4, 6]]
    y_ = corners[:, [1, 3, 5, 7]]

    xmin = np.min(x_, 1).reshape(-1, 1)
    ymin = np.min(y_, 1).reshape(-1, 1)
    xmax = np.max(x_, 1).reshape(-1, 1)
    ymax = np.max(y_, 1).reshape(-1, 1)

    final = np.hstack((xmin, ymin, xmax, ymax, corners[:, 8:]))

    return final
