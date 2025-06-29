import nextcord
from nextcord.ext import commands
import random

class MyDiscordBot:
    def __init__(self, token: str, intent_classifier, do_function, say_function):
        intents = nextcord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.token = token
        self.intent_classifier = intent_classifier
        self.do_function = do_function
        self.say_function = say_function

        self._register_events()

    def _register_events(self):
        @self.bot.event
        async def on_ready():
            print(f"🤖 Discord bot ready as {self.bot.user} (ID: {self.bot.user.id})")

        @self.bot.event
        async def on_message(message):
            # Ignore bot's own messages
            if message.author == self.bot.user:
                return

            # Classify and process the intent
            user_input = message.content
            intent_class = self.intent_classifier.say(user_input)
            success = self.do_function(intent_class)

            if success is True:
                response = random.choice(intent_class["responses"])
                await message.channel.send(response)
                self.say_function(response)  # Optional: voice speak
            else:
                await message.channel.send(f"⚠️ {intent_class}: Failed.")

    def run(self):
        self.bot.run(self.token)
