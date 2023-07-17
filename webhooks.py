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
    data = json.loads(flask.request.data.decode())

    try:
        action = data["action"]
        if color is None:
            if action == "cancelled":
                color = 0xF72F2F
            else:
                color = 0xEC6CB9
        sponsorship = data["sponsorship"]
        username = sponsorship["sponsor"]["login"]
        tier_name = sponsorship["tier"]["name"]
        privacy_level = sponsorship["privacy_level"]
        if action == "created":
            title = f"{username} is now {'privately ' if privacy_level == 'private' else ''}sponsoring for {tier_name}"
        else:
            title = f"{username} {action} their {tier_name} {'private ' if privacy_level == 'private' else ''}subscription"
        supporter_icon = sponsorship["sponsor"]["avatar_url"]
        supporter_url_html = sponsorship["sponsor"]["html_url"]
        webhook_send_json = {
            "embeds": [
                {
                    "color": color,
                    "title": title,
                    "author": {
                        "name": username,
                        "icon_url": supporter_icon,
                        "url": supporter_url_html,
                    },
                }
            ]
        }
        requests.post(
            f"https://discord.com/api/webhooks/{webhook_id}/{webhook_auth}",
            json=webhook_send_json,
        )
        return "Successfully sent webhook to Discord!"
    except Exception as e:
        if data["hook"]["type"] == "SponsorsListing":
            send_json = {
                "content": "GitHub Sponsors webhook has successfully been added! (Forked from https://github.com/NexInfinite/supporter-discord-webhook)"
            }
            requests.post(
                f"https://discord.com/api/webhooks/{webhook_id}/{webhook_auth}",
                json=send_json,
            )
            return "Setup complete! You will now receive notifications when someone sponsors you on GitHub!"
        else:
            return e


if __name__ == "__main__":
    app.run(host="localhost", port="8084")
