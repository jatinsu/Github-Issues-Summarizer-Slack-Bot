import os
from slack_bolt import App
from dotenv import load_dotenv
# import re
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()   
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)


@app.message(compile("Issue created by"))
def handle_message_im(say):
    say(f"This is a github pull request")

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
