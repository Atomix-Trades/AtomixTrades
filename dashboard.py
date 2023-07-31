from flask import Flask, render_template
from bot import *

app = Flask(__name__)

@app.route('/')
def status():
    if trade_started:
        bot_status = "Running"
        status_color = "green"
    else:
        bot_status = "Stopped"
        status_color = "red"
    return render_template('botstatus.html', bot_status=bot_status, status_color=status_color)

if __name__ == "__main__":
    app.run()
