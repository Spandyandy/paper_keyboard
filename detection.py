import cv2
import numpy as np

class Detection(object):
    THRESHOLD = 1000

    def __init__(self, image):
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def get_pressed(self, image):

        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(self.previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

        # debug
        cv2.imshow('current_gray', current_gray)
        cv2.waitKey(10)
        h, w = threshold_image.shape[:2]
        each_keyboard = int(w/8)
        # set cell width
        keyboards = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        start_idx = 0
        end_idx = each_keyboard

        for idx, cell in enumerate(keyboards):
            if idx == 7:
                end_idx = w
            else:
                end_idx = each_keyboard * (idx+1)
            keyboards[idx] = cv2.countNonZero(threshold_image[0:h, start_idx:end_idx])
            start_idx = end_idx


        # store current image
        self.previous_gray = current_gray

        # obtain the most active cell
        top_cell = np.argmax(keyboards)

        # return the most active cell, if threshold met
        if keyboards[top_cell] >= self.THRESHOLD:
            return top_cell
        else:
            return None