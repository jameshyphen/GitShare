import base64
from json.decoder import JSONDecodeError
from typing import List
from flask import Flask, Response, jsonify, render_template, request
import requests
import json

app = Flask(__name__)

def make_SVG(theme, posts):
    data_dict = {
        "posts": posts,
        "theme": theme
    }

    return render_template("index.html", **data_dict)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    theme = request.args.get("theme") or "default"
    image = request.args.get("image") or "default"
    user = request.args.get("user") or "GitShareUser"

    url = f"https://raw.githubusercontent.com/{user}/{user}/master/GitShare.json"

    response = requests.get(url)
    try:
        posts = response.json()["Posts"]
        print(posts)

    except JSONDecodeError as e:
        posts = [{
                    "title": "Error",
                    "description": "GitShare json on your personal profile is either invalid or missing.",
                    "image": "https://i.imgur.com/TxAh3ln.png"
        }]
        print("CRASHED")
        print(e)

    svg = make_SVG(theme, posts)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-control"] = "s-maxage=1"

    return resp

if __name__ == "__main__":
    app.run(debug=True)