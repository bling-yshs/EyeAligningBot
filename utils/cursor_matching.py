import cv2
from grabscreen import grab_screen

from collections import Counter


class LocQueue():
    def __init__(self, maxsize=9):
        self.queue = []
        self.maxsize = maxsize
        self.ptr = 0

    def put(self, elem):
        if self.full():
            self.queue[self.ptr] = elem
            self.ptr = (self.ptr + 1) % self.maxsize
        else:
            self.queue.append(elem)
    
    def full(self):
        return len(self.queue) == self.maxsize

    def major(self):
        return Counter(self.queue).most_common(1)  # a list of (key, value)


Loc_Q = LocQueue(maxsize=100)

def cursor_match(template_cursor):

    # screen
    img = grab_screen(region=(0, 0, 1200, 900))
    img_H = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :,0]
    # template
    
    template_cursor_H = cv2.cvtColor(template_cursor, cv2.COLOR_BGR2HSV)[:, :, 0]

    # matching by NCC
    result = cv2.matchTemplate(img_H, template_cursor_H, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    # majority voting
    Loc_Q.put(maxLoc if abs(maxVal)>abs(minVal) else minLoc)
    Loc = Loc_Q.major()[0][0]

    # draw the region
    (startY, startX) = Loc
    startX = startX + 3   # X=Loc[1] Y=Loc[0]+17
    startY = startY + 17
    endX = startX + 26
    endY = startY
    img_H = cv2.rectangle(img_H.copy(), (startY, startX), (endY, endX), 255, 1)

    # display
    # cv2.namedWindow('img_H', cv2.WINDOW_NORMAL)
    # cv2.imshow('img_H', img_H)

    return Loc[1], Loc[0] + 17

