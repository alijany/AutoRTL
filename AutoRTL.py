import pynput

# import re
# regex = r"[\u0600-\u06FF\u0750-\u077F\u0590-\u05FF\uFE70-\uFEFF]"
# re.search(regex, key.char, re.UNICODE)

keyboard = pynput.keyboard.Controller()
status = True

print("""    _         _        ____ _____ _     
   / \  _   _| |_ ___ |  _ \_   _| |    
  / _ \| | | | __/ _ \| |_) || | | |    
 / ___ \ |_| | || (_) |  _ < | | | |___ 
/_/   \_\__,_|\__\___/|_| \_\|_| |_____|
                                        
""")
print("contact: mh.alijany@gmail.com\n")


def on_press(key):
    global status, COMBINATIONS
    if key == pynput.keyboard.Key.f2:
        status = not status
        print("status: enabled" if status else "status: disabled")
    if status and (key == pynput.keyboard.Key.space or hasattr(key, "char")):
        keyboard.press(pynput.keyboard.Key.left)


listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
