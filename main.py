from AI.main import *
from functions.functions import *
from display.tesseract import *
import threading

print("Which interface? (cmd/voice)")
choice = input("You: ")
choice = choice.lower()

intent_classifier = IntentClassifier()
threading.Thread(target=draw_tesseract).start()

if choice == "cmd":
    One = 1
    while True:
        msg = input("You: ")
        intent_class = intent_classifier.say(msg)
        success = DoFunction(intent_class)
        if success is True:
            print(intent_class)
        else:
            print(f"{intent_class}: Failed.")
elif choice == "discord":
    pass
elif choice == "voice":
    pass

