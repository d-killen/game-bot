import cv2
import os
import pytesseract
import time
import win32api, win32con
import numpy as np
import random

from PIL import Image, ImageGrab
from pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

X_PAD = 1909
Y_PAD = 194

def mousePos(cord):
    loc=(X_PAD + cord[0], Y_PAD + cord[1])
    win32api.SetCursorPos(loc)
    time.sleep(.1)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)  

def place_bet(cord):
    loc=(X_PAD + cord[0], Y_PAD + cord[1])
    win32api.SetCursorPos(loc)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)    
	
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - X_PAD
    y = y - Y_PAD
    clicked_cord = (x, y)
    return clicked_cord

def bet_clear():
    mousePos(bet_cord['clear'])
    leftClick()

def spin():
    mousePos((1193, 952))
    leftClick()
    time.sleep(.1)
    leftClick()
    time.sleep(.1)
    leftClick()
    time.sleep(1)
    leftClick()
    time.sleep(1)

def get_result(num_results, even_tracker, red_tracker):

    red = 0
    even = 0

    # Grab the number image
    box = (X_PAD + 1246, Y_PAD + 344, X_PAD + 1281, Y_PAD + 382)
    img = ImageGrab.grab(box)

    # Get the number
    arr = np.array(img) # OpenCV and PyTesseract need array input
    gry = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    txt = image_to_string(gry, config="--psm 7")
    txt.replace('\n', '')
    
    # Get even or odd
    if int(txt) % 2 == 0: # even
        even = 1
    elif int(txt) % 2 != 0: # odd
        even = -1
    
    # Get the colour
    col = sorted(img.getcolors())
    hex = ('#%02x%02x%02x' % col[-2][1])
    #print(hex)
    if hex == '#000000':
        red = -1
    elif hex == '#ff0000':
        red = 1
    
    # Update the results
    num_results.insert(0, int(txt))
    if len(num_results) > 20:
        num_results.pop()
    
    even_tracker += even
    red_tracker += red

    return num_results, even_tracker, red_tracker

bet_cord = {
00 : (175, 416),
0 : (180, 551),
1 : (256, 576),
2 : (256, 488),
3 : (268, 378),
4 : (345, 583),
5 : (341, 500),
6 : (348, 375),
7 : (412, 584),
8 : (413, 481),
9 : (418, 405),
10 : (489, 584),
11 : (496, 486),
12 : (498, 380),
13 : (573, 587),
14 : (575, 488),
15 : (576, 397),
16 : (650, 584),
17 : (638, 486),
18 : (636, 381),
19 : (710, 584),
20 : (711, 485),
21 : (723, 392),
22 : (794, 580),
23 : (794, 482),
24 : (793, 407),
25 : (878, 575),
26 : (874, 491),
27 : (873, 373),
28 : (951, 581),
29 : (949, 491),
30 : (953, 395),
31 : (1016, 598),
32 : (1020, 482),
33 : (1015, 387),
34 : (1098, 572),
35 : (1095, 481),
36 : (1103, 394),
'1st' : (1178, 577),
'2nd' : (1182, 476),
'3rd' : (1178, 382),
'1-12' : (397, 685),
'13-24' : (693, 681),
'25-36' : (989, 676),
'1-18' : (292, 773),
'19-36' : (1084, 772),
'even' : (470, 766),
'odd' : (920, 765),
'red' : (603, 771),
'black' : (777, 775),
'clear' : (87, 294)
}

def main():
    # Bot Logic
    num_results = []
    even_tracker = 0 # This tracks the current likelihood of even (+ve) or odd (-ve)
    red_tracker = 0 # This tracks the current likelihood of red (+ve) or black (-ve)
    
    # Starts with 2500
    capital = 2500

    # First bet
    # Spin
    # Result
    # Process
    # Analysis
    # Select bets
    # Place bets
    # Spin

    # Bets that can be placed
    #   - Numbers
    #   - Odds/Evens
    #   - Black/Red
    #   - Thirds
    #   - Halves

    for i in range(1, 21):
        #print("Enter a number to bet on:")
        choice = random.randint(1, 36)
        bet_clear()
        print(f"Placing bet on {choice}")
        place_bet(bet_cord[choice])

        #
        if even_tracker < -2:
            # bet even
            place_bet(bet_cord['even'])

        elif even_tracker > 2:
            # bet odd
            place_bet(bet_cord['odd'])
        
        #
        if red_tracker < -2:
            # bet red
            place_bet(bet_cord['red'])

        elif red_tracker > 2:
            # bet black
            place_bet(bet_cord['black'])

        spin()

        num_results, even_tracker, red_tracker = \
        get_result(num_results, even_tracker, red_tracker)

        print(f"The result was {num_results[0]}")
        print(f"Last results were:{num_results}")
        print(f"The red tracker is:{red_tracker}")
        print(f"The even tracker is:{even_tracker}")

if __name__ == '__main__':
    main()
