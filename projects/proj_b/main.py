import os

from flask import Flask
from hello import hello

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return hello("World")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
