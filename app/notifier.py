# notifier.py

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID

slack_client = WebClient(token=SLACK_BOT_TOKEN)

def send_slack_summary(project_name, error_list):
    if not error_list:
        return

    message = f"*🚨 {project_name.upper()} Logs - Summary of Errors*\n"

    for filename, errors in error_list.items():
        message += f"\n*File:* `{filename}`"
        for err in errors:
            message += f"\n• `{err.strip()}`"
        message += "\n"

    message += f"\n_Project: {project_name}_"

    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=message
        )
        print(f"[INFO] Slack message sent to channel {SLACK_CHANNEL_ID} for project {project_name}")
    except SlackApiError as e:
        print(f"[ERROR] Failed to send Slack message: {e.response['error']}")
