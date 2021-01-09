from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

def make_SVG():
    # ...

    return render_template("index.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    theme = request.args.get("theme") or "default"
    image = request.args.get("image") or "default"
    user = request.args.get("user") or "GitShareUser"

    svg = make_SVG()

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-control"] = "s-maxage=1"

    return resp

if __name__ == "__main__":
    app.run(debug=True)