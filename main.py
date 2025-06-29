from AI.main import *
from functions.functions import *
from display.tesseract import *
from interfaces.discord import *
import threading
import random

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
            response = random.choice(intent_class["responses"])
            print(response)
            say(response)
        else:
            print(f"{intent_class}: Failed.")

elif choice == "discord":
    with open("./config/discord_key.txt", "r") as file:
        token = file.read().strip()

    discord_interface = MyDiscordBot(
        token,
        intent_classifier=intent_classifier,
        do_function=DoFunction,
        say_function=say
    )
    discord_interface.run()


elif choice == "voice":
    pass

