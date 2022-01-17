import pyWinhook
import pythoncom
from pynput.keyboard import Key, Controller
import clipboard

# import re
# regex = r"[\u0600-\u06FF\u0750-\u077F\u0590-\u05FF\uFE70-\uFEFF]"
# re.search(regex, key.char, re.UNICODE)

print("""    _         _        ____ _____ _
   / \  _   _| |_ ___ |  _ \_   _| |
  / _ \| | | | __/ _ \| |_) || | | |
 / ___ \ |_| | || (_) |  _ < | | | |___
/_/   \_\__,_|\__\___/|_| \_\|_| |_____|

""")
print("contact: mh.alijany@gmail.com\n")

status = False
keyboard = Controller()
keys = [*range(16, 27), *range(30, 41), *range(43, 53), 57]
stack = set()
shift = False
print("status: enabled" if status else "status: disabled")
print("press f2 to enable AutoRTL")
print("press f3 reverse clipboard content")


def printInfo(event):
    # print('MessageName: {}'.format(event.MessageName))
    # print('Message: {}'.format(event.Message))
    # print('Time: {}'.format(event.Time))
    # print('Window: {}'.format(event.Window))
    # print('WindowName: {}'.format(event.WindowName))
    # print('Ascii: {}'.format(chr(event.Ascii)))
    print('Key: {}'.format(event.Key))
    print('KeyID: {}'.format(event.KeyID))
    print('ScanCode: {}'.format(event.ScanCode))
    print('Extended: {}'.format(event.Extended))
    print('Injected: {}'.format(event.injected))
    print('Alt: {}'.format(event.Alt))
    print('Transition: {}'.format(event.Transition))


def OnKeyboardEvent(event):
    global status, stack, shift
    if event.KeyID == 114:
        text = clipboard.paste()
        clipboard.copy(text[::-1])
        print("clipboard content reversed")
        return True
    if event.KeyID == 113:
        status = not status
        print("status: enabled" if status else "status: disabled")
        return True
    if not status:
        return True
    if event.Injected:
        return True
    if event.KeyID == 46:
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    elif event.KeyID == 8:
        keyboard.press(Key.delete)
        keyboard.release(Key.delete)
    elif event.KeyID == 13:
        keyboard.press(Key.end)
        keyboard.release(Key.end)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif event.ScanCode in keys and len(stack) == 0:
        if shift:
            with keyboard.pressed(Key.shift):
                keyboard.press(chr(event.Ascii))
                keyboard.release(chr(event.Ascii))
        else:
            keyboard.press(chr(event.Ascii))
            keyboard.release(chr(event.Ascii))
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif event.ScanCode == 42:
        shift = True
    elif not event.ScanCode in stack:
        stack.add(event.ScanCode)
        return True
    return False


def OnReleaseEvent(event):
    global stack, shift
    if event.ScanCode == 42:
        shift = event.Injected
    elif event.ScanCode in stack:
        stack.remove(event.ScanCode)
    return True


hm = pyWinhook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnReleaseEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
