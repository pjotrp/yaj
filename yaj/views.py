from yaj import app

@app.route("/")
def main_page():
    return "Yet another journal! Well, early days!"
