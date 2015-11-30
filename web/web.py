from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/classify")
def classify():
    text = "The sun is shining Let's go outside"
    return "punctuated text as json"

if __name__ == "__main__":
    app.run()
