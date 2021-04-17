from flask import Flask, render_template

app = Flask(__name__)


@app.route("/index.html")
def hello_world():
    return render_template("index.html")


@app.route("/test.html")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
