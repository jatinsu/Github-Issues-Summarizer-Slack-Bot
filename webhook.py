import os
from flask import Flask, request, jsonify
from slack_bolt import App
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

flask_app = Flask(__name__)

slack_app = App(token=SLACK_BOT_TOKEN)

# summarize the github issue body using the github issue body using gemini api
def summarize_github_issue(github_issue_body):
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=github_issue_body,
        config=types.GenerateContentConfig(
            system_instruction=open("prompts/single_sentence.txt", "r").read()
        )
    )
    return response.text

@flask_app.route('/webhook', methods=['POST'])
def webhook():    
    try:
        data = request.json
    except:
        return jsonify({'status': 'error'}), 400
    
    issue_body = data['issue']['body']
    
    # Summarize the issue body
    if data['action'] == 'opened':
        loading_summary_message = slack_app.client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=f"Loading Summary of issue {data['issue']['title']}..."
        )
        summarized_issue_body = summarize_github_issue(issue_body)
        full_summary = f"Summary of issue <{data['issue']['html_url']}|{data['issue']['title']}>:\n\n{summarized_issue_body}"
        slack_app.client.chat_update(
            channel=loading_summary_message['channel'],
            ts=loading_summary_message['ts'],
            text=full_summary
        )

    return jsonify({'status': 'received'}), 200


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=True)