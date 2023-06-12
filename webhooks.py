import flask
import json
import requests
from flask import Flask
app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    webhook_id = flask.request.args.get("webhook_id")
    webhook_auth = flask.request.args.get("webhook_auth")

    color = flask.request.args.get("color")
    if color is None:
        color = 0xec6cb9

    data = json.loads(flask.request.data.decode())
    try:
        if data["action"] == "created":
            sponsorship = data["sponsorship"]
            username = sponsorship["sponsor"]["login"]
            tier_name = sponsorship["tier"]["name"]
            supporter_url_html = sponsorship["sponsor"]["html_url"]
            supporter_icon = sponsorship["sponsor"]["avatar_url"]
            privacy_level = sponsorship["privacy_level"]
            webhook_send_json = {
              "embeds": [
                {
                  "color": color,
                  "title": f"{username} is now {'privately ' if privacy_level == 'private' else ''}sponsoring for {tier_name}",
                  "author": {
                    "name": username,
                    "icon_url": supporter_icon,
                    "url": supporter_url_html
                  }
                }
              ]
            }
            requests.post(f"https://discord.com/api/webhooks/{webhook_id}/{webhook_auth}", json=webhook_send_json)
            return "Successfully sent webhook to Discord!"
    except Exception as e:
        if data["hook"]["type"] == "SponsorsListing":
            send_json = {
                "content": "GitHub Sponsors webhook has successfully been added! (Forked from https://github.com/NexInfinite/supporter-discord-webhook)"
            }
            requests.post(f"https://discord.com/api/webhooks/{webhook_id}/{webhook_auth}", json=send_json)
            return "Setup complete! You will now receive notifications when someone sponsors you on GitHub!"
        else:
            return e


if __name__ == "__main__":
    app.run(host="localhost", port="8084")
