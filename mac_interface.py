import pyautogui
import time
freePongActive = False
#todo: should be called process command
def handleCommand(command, keyPosition, price=0):
                global freePongActive
                if command == 'FIRE':
                    print("fire, clicking mouse")
                    # Line below change to what control you want to assign to the premium button.
                    pyautogui.click(button='right')
                if command == 'FREE_FIRE':
                    print("processing fire")
                    if not freePongActive:
                        freePongActive = True
                        print("free pong fire was enabled")
                        # Line below change to what control you want to assign to free button.
                        pyautogui.click(button='right')
                        print("free ping pong", freePongActive)
                        # Time delay you want in seconds between when they can free fire.
                        time.sleep(10)
                        freePongActive = False
                    else:
                        print("ping pong not enabled")
