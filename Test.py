import sys
import termios
import tty

print("Press keys (press 'q' to quit)")

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

try:
    tty.setraw(fd)
    while True:
        key = sys.stdin.read(1)
        print("You pressed:", key)
        if key == "q":
            break
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

