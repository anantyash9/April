import getch
from threading import Thread
from time import sleep

# from pyserver import move_bot

left, right, direction = 0, 0, 1


# def decay():
#     global left, right
#     while True:
#         left = max(0, left - 1)
#         right = max(0, right - 1)
#         sleep(0.001)
#
#
# Thread(target=decay).start()

while True:
    key = ord(getch.getch())
    if key == 27:  # ESC
        break
    elif key == 224:  # Special keys (arrows, f keys, ins, del, etc.)
        key = ord(getch.getch())
        if key == 72:  # Up arrow
            left += 1
            right += 1
            # move_bot(left, right)
        elif key == 80:  # Down arrow
            left += 1
            right += 1
            # move_bot(left, right)
    print(key)