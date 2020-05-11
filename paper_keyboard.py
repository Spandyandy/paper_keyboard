from detection import Detection
from threading import Thread
import cv2
import time


class CaptureCam:

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        print("fps", fps)

    # create thread for capturing images
    def start(self):
        Thread(target=self._update_frame, args=()).start()

    def release(self):
        self.video_capture.release()

    def _update_frame(self):
        while (True):
            self.current_frame = self.video_capture.read()[1]

    # get the current frame
    def get_current_frame(self):
        return self.current_frame


video = CaptureCam()
video.start()

# initialise detection with first webcam frame
frame = video.get_current_frame()
# rectangle area in which the keyboard image will be placed
top, left = (int(frame.shape[1] / 4) - 150, int(frame.shape[0] / 4) - 20)
bottom, right = (int(frame.shape[1] * 3 / 4) + 150, int(frame.shape[0] * 3 / 4) + 20)

frame = frame[left:right, top:bottom]
detection = Detection(frame)

switch = True
captured = False
MORPH = 7
CANNY = 250
pressed_output = open('pressed_keys.txt', 'a')

frame_rate = 3
prev = 0
while True:
    # current frame
    time_elapsed = time.time() - prev
    start_time = time.time()
    frame = video.get_current_frame()

    if time_elapsed > 1/frame_rate:
        prev = time.time()

        cv2.rectangle(frame, (top, left), (bottom, right), (0, 255, 0), 2)
        cv2.imshow("original", frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 1, 10, 120)

        edges = cv2.Canny(gray, 10, CANNY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        _, contours, h = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        max_approx = None

        for cont in contours:

            arc_len = cv2.arcLength(cont, True)

            approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)
            bounding_rec = cv2.boundingRect(approx)
            if len(approx) == 4:
                # print("rectangle!")
                if cv2.contourArea(cont) > max_area:
                    max_area = cv2.contourArea(cont)
                    max_approx = approx
                    max_bbox = bounding_rec

        if max_approx is not None:
            cv2.drawContours(frame, [max_approx], -1, (255, 0, 0), 2)

        if captured:
            # boxed region for keyboard
            frame = frame[left:right, top:bottom]
            cv2.imshow("img cropped", frame)

            # use motion detection to get active cell
            cell = detection.get_pressed(frame)
            if cell is None:
                continue
            # if time.time() - start_time > 1:
            if writing:
                pressed_output.write("{}\n".format(7-cell+1))
                pressed_output.flush()
                # pressed_output.close()

                p_out = open("pressed_keys.txt", "r")
                print(p_out.readlines()[-1])
                p_out.close()
                print("PRESSED:", 7-cell+1)


    # sleeping for 1 second
    # to not detect hand moving
    # time.sleep(1 - time.time() + start_time)

    pressed_key = cv2.waitKey(10)
    if pressed_key == ord("b"):
        captured = True
        writing = True

    elif pressed_key == 27:  # press ESC to exit
        pressed_output.write("stopped playing")
        pressed_output.close()
        video.release()
        cv2.destroyAllWindows()
        break