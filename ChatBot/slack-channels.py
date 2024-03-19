import logging
import os
import json

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


SLACK_BOT_TOKEN = "xoxb-4860420682530-4845896564391-gUqHGfhcvFNSCh5MAvxEqGfr"
SLACK_APP_TOKEN = "xapp-1-A04QVSAFVST-4860317221699-23a83a3bfa4ba1ee3f0b46c6520d89cd6a1cf0ec58899cb22154990359553d41"
OPENAI_API_KEY  = "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"


# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.

client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

channel_name = "gpt-test-channel"
conversation_id = None

try:
    # Call the conversations.list method using the WebClient
    for result in client.conversations_list():
        if conversation_id is not None:
            break
        for channel in result["channels"]:
            if channel["name"] == channel_name:
                conversation_id = channel["id"]
                #Print result
                print(f"Found conversation ID: {conversation_id}")
                break

except SlackApiError as e:
    print(f"Error: {e}")

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = conversation_id

#print("reached here")

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id)
    
    conversation_history = result["messages"]
    
    for i in result["messages"]:
        print(i["text"])
        print(i["ts"])
    logger.info("{} messages found in {}".format(len(conversation_history), channel_id))
    

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))


try:
    # Call the conversations.history method using the WebClient
    # The client passes the token you included in initialization    
    result = client.conversations_history(
        channel=conversation_id,
        inclusive=True,
        latest="1677383572.572579",
        limit=1
    )

    messages = result["messages"]
    for msg in messages:
        print(msg["text"])

except SlackApiError as e:
    print(f"Error: {e}")

try:
    #print(result["messages"][0]["thread_ts"])
    
    if "thread_ts" in result["messages"][0]:
        logging.info("threaded message")

except SlackApiError as e:
    print(f"Error: {e}")

result = client.conversations_replies(
    channel = channel_id,
    ts = result["messages"][0]["ts"])

for msg in result["messages"]:
    print(msg["text"])

#print(result)