# roulette-bot
This is a simple bot to play an online game of roulette at https://www.247roulette.org/; it is not intended to win but demonstrate key coding concepts needed to automate a simple in-browser game.

## Built With
- Pillow
- OpenCV
- PyTesseract
- PyWin

## Use
The script is currently configured to run with the web game opened in a Brave browser window measuring 1720x1440 pixels.

Prior to running for the first time the constants X_PAD and Y_PAD should be updated for your configuration to represent the top left corner of the game area. This should allow the script to function with alternate setups however it has not been tested.

## Function
The script runs for twenty spins of each time selecting a random number to bet upon.

After each spin the even/odd and black/red events are tracked, once one has happened three times in a row a bet is placed for the opposite event.

