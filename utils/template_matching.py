
import cv2
from grabscreen import grab_screen


def temp_match(template_eye, template_eye_precise):

    # screen
    img = grab_screen(region=(0, 0, 1200, 900))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # matching by NCC
    result = cv2.matchTemplate(img, template_eye, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)  

    # draw the region
    (startY, startX) = maxLoc
    endX = startX + template_eye.shape[0]
    endY = startY + template_eye.shape[1]
    if maxVal > 0.6:
        img = cv2.rectangle(
            img, (startY, startX), (endY, endX), (255, 0, 0), 1)

    # focusing
    precise = grab_screen(region=(startY, startX, endY, endX + 70))
    precise = cv2.cvtColor(precise, cv2.COLOR_RGB2BGR)

    # precisely matching by NCC
    destX = destY = None
    if maxVal > 0.8:

        result_p = cv2.matchTemplate(
            precise, template_eye_precise, cv2.TM_CCOEFF_NORMED)
        (minVal_p, maxVal_p, minLoc_p, maxLoc_p) = cv2.minMaxLoc(result_p)  
        pixelY, pixelX = maxLoc_p

        # draw the line
        precise = cv2.rectangle(
            precise, (pixelY + 2, pixelX + 2), (pixelY + 2, pixelX + 80), (0, 0, 255), 1)
        
        if maxVal_p > 0.7:
            destX = pixelX + 60 + startX
            destY = pixelY + 2 + startY
        else:
            destX = destY = None
    
    # cv2.namedWindow('screen_full', cv2.WINDOW_NORMAL)
    cv2.namedWindow('screen_pixel', cv2.WINDOW_NORMAL)
    # cv2.imshow('screen_full', img)
    cv2.imshow('screen_pixel', precise)
    
    return destX, destY
    