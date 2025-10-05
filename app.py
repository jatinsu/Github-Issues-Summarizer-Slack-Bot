import os
from slack_bolt import App
from dotenv import load_dotenv
# import re
import json
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()   
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
app = App(token=SLACK_BOT_TOKEN)

@app.message("testing for slack bot")
def say_hello(say):
    say(f"Hello world")

@app.event("message")
def handle_message_im(message, say):
    # check if the message is from github bot
    if message['bot_id'] != "B09GJGSLK4Y":
        print("the message is not from github bot")
        return

    # print the message in the plain text
    github_issue_link = json.loads(message['attachments'][0]['actions'][0]['value'])['issueHtmlUrl']
    say(f"The github issue link is {github_issue_link}")
    issue_message = message['attachments'][0]['text']
    say(f"The message is {issue_message}")
    print(f"{json.dumps(message, indent=2)}")

    
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
