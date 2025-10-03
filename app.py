import os
from slack_bolt import App
from dotenv import load_dotenv
# import re
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()   
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
app = App(token=SLACK_BOT_TOKEN)

@app.message("testing for slack bot")
def say_hello(say, event):
    say(f"Hello world")

@app.event("message")
def handle_message_im(message, say):
    # check if the message is from github bot
    if "bot_id" not in message and "bot_id" != "U09GJGSSQ1W":
        print("the message is not from github bot")
        return
    
    # print the message in the plain text
    say(f"the user id is {message['user']} and the message is {message['text']}")
    the_message = message['text']
    print(the_message)

    
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
