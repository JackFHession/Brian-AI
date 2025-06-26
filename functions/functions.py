import os
import webbrowser
import threading

def say_internal(text):
    os.system(f'./vocal/speak "{text}"')

def say(text):
    threading.Thread(target=say_internal,args=(text,)).start()

def DoFunction(intent_class):
    
    try:
        tag = intent_class.get("tag")

        if tag == "open-google":
            webbrowser.open("https://www.google.com", new=2)
        elif tag == "search-web":
            query = intent_class.get("query")
            webbrowser.open(f"https://www.google.com/search?q={query}", new=2)
        elif tag == "open-firefox":
            os.system("firefox &")
        elif tag == "close-firefox":
            os.system("pkill firefox")
        elif tag == "set-reminder":
            reminder = intent_class.get("reminder")
            os.system(f'notify-send "Reminder" "{reminder}"')
        elif tag == "play-music":
            os.system(f"playerctl play-pause")
        elif tag == "open-terminal":
            os.system("gnome-terminal &")
        elif tag == "run-command":
            command = intent_class.get("command")
            os.system(command)
        elif tag == "send-email":
            recipient = intent_class.get("recipient")
            subject = intent_class.get("subject")
            message = intent_class.get("message")
            os.system(f"echo \"{message}\" | mail -s \"{subject}\" {recipient}")
        elif tag == "shutdown":
            print("Shut down.")
            os.system("shutdown now")
        elif tag == "reboot":
            print("Reboot.")
            os.system("reboot")
        elif tag == "increase-volume":
            os.system("amixer -D pulse set Master 5%+")
        elif tag == "decrease-volume":
            os.system("amixer -D pulse set Master 5%-")
        elif tag == "mute-volume":
            os.system("amixer -D pulse set Master mute")
        elif tag == "unmute-volume":
            os.system("amixer -D pulse set Master unmute")
        elif tag == "open-file":
            file_path = intent_class.get("file_path")
            os.system(f"xdg-open {file_path}")
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
    return True
