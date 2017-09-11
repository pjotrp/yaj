from flask import Flask
app = Flask(__name__)

@app.route("/")
def main_page():
    return "Yet another journal! Well, early days"

if __name__ == "__main__":
    app.run()
