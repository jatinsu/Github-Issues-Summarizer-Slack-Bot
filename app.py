import os
from slack_bolt import App
from dotenv import load_dotenv
import requests
import json
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()   
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
GH_TOKEN = os.environ.get("GH_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
app = App(token=SLACK_BOT_TOKEN)

@app.message("testing for slack bot")
def say_hello(say):
    say(f"Hello world")

def summarize_github_issue(github_issue_body):
    # summarize the github issue body using the github issue body using gemini api
    return github_issue_body

@app.event("message")
def github_issue_message(message, say):
    # check if the message is from github bot
    if 'bot_id' not in message:
        return
    elif (message['bot_id'] != "B09GJGSLK4Y" or "Issue opened" not in message['attachments'][0]['fallback']):
        print("the message is not from github bot")
        return

    # get the github issue body from the github issue link
    github_issue_link = json.loads(message['attachments'][0]['actions'][0]['value'])['issueHtmlUrl']
    converted_github_issue_link = github_issue_link.replace("github.com", "api.github.com/repos")

    headers = {
        "Accept": "application/vnd.github.v3.raw+json",
        "Authorization": f"Bearer {GH_TOKEN}"
    }
    response = requests.get(converted_github_issue_link, headers=headers)
    if response.status_code == 200:
        github_issue_body = response.json().get("body", "")
    else:
        github_issue_body = f"Failed to fetch issue body: {response.status_code}"
    
    say(f"{github_issue_body}")
    
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
