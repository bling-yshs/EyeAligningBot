
import cv2
from utils.grabscreen import grab_screen


def temp_match(template_eye, template_eye_precise, region=(0, 0, 1919, 1079)):

    # screen
    img = grab_screen(region=region)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # matching
    result = cv2.matchTemplate(img, template_eye, cv2.TM_SQDIFF)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)  

    if minVal > 900000:
        return minVal, None, None, None
    else:
        (startY, startX) = minLoc
        endX = startX + template_eye.shape[0]
        endY = startY + template_eye.shape[1]

        # focusing
        precise = grab_screen(region=(startY, startX, endY-1, endX+70-1))
        precise = cv2.cvtColor(precise, cv2.COLOR_RGB2BGR)

        # precisely matching by NCC
        result_p = cv2.matchTemplate(
            precise, template_eye_precise, cv2.TM_CCOEFF_NORMED)
        (minVal_p, maxVal_p, minLoc_p, maxLoc_p) = cv2.minMaxLoc(result_p)  
        pixelY, pixelX = maxLoc_p

        # draw the line
        x1 = pixelX + 2
        y1 = pixelY + 2
        color = (255, 224, 47)
        precise = cv2.line(precise, (y1, x1), (y1, x1+10), color, 1)
        precise = cv2.line(precise, (y1, x1+20), (y1, x1+30), color, 1)
        precise = cv2.line(precise, (y1, x1+40), (y1, x1+50), color, 1)
        precise = cv2.line(precise, (y1, x1+60), (y1, x1+70), color, 1)
        precise = cv2.line(precise, (y1, x1+80), (y1, x1+90), color, 1)
        
        destX = pixelX + 60 + startX
        destY = pixelY + 2 + startY

        return minVal, destX, destY, cv2.cvtColor(precise, cv2.COLOR_BGR2RGB)


    
    