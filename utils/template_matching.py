# Done by Balloon_356
# Bilibili: https://space.bilibili.com/244384103

import cv2
from utils.grabscreen import grab_screen



def temp_match(template_eye, mask, region=(0, 0, 1919, 1079)):
    '''
    param: template_eye(cv2.imread()), the template used to match the screenshot
    param: mask, the mask used in cv2.matchTemplate
    param: region, the region of screenshot
    return: minVal of matchTemplate result, destX, destY, endereye
    '''

    # screen
    img_screen = grab_screen(region=region)
    img_screen = cv2.cvtColor(img_screen, cv2.COLOR_RGB2BGR)

    # matching
    result = cv2.matchTemplate(img_screen, template_eye, cv2.TM_SQDIFF, mask=mask)
    (minVal, _, minLoc, _) = cv2.minMaxLoc(result)  

    if minVal > 10:
        print(minVal)
        return minVal, None, None, None

    else:
        (LocY, LocX) = minLoc

        # used to grab screen
        startX = LocX - 5
        startY = LocY - 5
        endX = LocX + 95
        endY = LocY + 25

        endereye = grab_screen(region=(startY, startX, endY, endX))

        # original dest point
        destX = LocX + 10
        destY = LocY + 9

        # draw the line
        color = (255, 224, 47)
        x1 = destX - startX
        y1 = destY - startY
        # cv2.line  point(y1, x1) to point(y2, x2)
        endereye = cv2.line(endereye, (y1, x1), (y1, x1+10), color, 1)
        endereye = cv2.line(endereye, (y1, x1+20), (y1, x1+30), color, 1)
        endereye = cv2.line(endereye, (y1, x1+40), (y1, x1+50), color, 1)
        endereye = cv2.line(endereye, (y1, x1+60), (y1, x1+70), color, 1)

        return minVal, destX+50, destY, endereye