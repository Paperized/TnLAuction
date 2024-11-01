import mouse
import time

def onclick():
    print(mouse.get_position())

mouse.on_middle_click(onclick)

while True:
    time.sleep(0.1)

mouse.unhook_all()

# top left(2233, 487)
# bottom left(2237, 487)
# top right(2233, 550)
# bottom right(2237, 550)