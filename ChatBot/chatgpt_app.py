SLACK_BOT_TOKEN = "xoxb-4860420682530-4845896564391-gUqHGfhcvFNSCh5MAvxEqGfr"
SLACK_APP_TOKEN = "xapp-1-A04QVSAFVST-4860317221699-23a83a3bfa4ba1ee3f0b46c6520d89cd6a1cf0ec58899cb22154990359553d41"
OPENAI_API_KEY  = "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"

import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

# Event API & Web API
app = App(token=SLACK_BOT_TOKEN) 
client = WebClient(SLACK_BOT_TOKEN)

# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    # Let the user know that we are busy with the request 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")
    
    posts = client.conversations_replies(
        channel=body["event"]["channel"],
        ts=body["event"]["thread_ts"])

    #print(posts)

    #concat_msg = "summarize given text in issue, detection, root cause, mttr, impact: "
    #concat_msg = "perform sentiment analysis on following conversation: \n"
    concat_msg = "Relevant conversation : \n"
    for post in posts["messages"]:
        if post["user"] != "U04QVSCGLBH": #ignore its own responses for now
            concat_msg = concat_msg + "<@" + post["user"] + ">" + \
            ":" + post["text"] + "\n"

    concat_msg = concat_msg + "end of conversation.\n"
    #concat_msg = concat_msg + "Please ignore messages from GPT-test in the conversation.\n"

    concat_msg = concat_msg + prompt

    #print(concat_msg)

    # Check ChatGPT
    # temperature: controls creativity, high for more creative
    # tokens: summary length
    # stop: end char
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=concat_msg,
        max_tokens=200,
        #n=1,
        stop=None,
        temperature=0.5,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        top_p=1.0).choices[0].text
    
    
    # Reply to thread 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Here you go: \n{response}")

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()