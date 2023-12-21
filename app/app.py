import os
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
LOG_FILE = '/workspaces/codespaces-jupyter/notebooks/server.log'

def tail_log_file():
    with open(LOG_FILE, 'r') as file:
        file.seek(0, 2)  # Move to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly
                continue
            socketio.emit('log_update', {'data': line.strip()})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_logs')
def all_logs():
    try:
        with open(LOG_FILE, 'r') as file:
            logs = file.readlines()
    except FileNotFoundError:
        logs = ["Log file not found."]
    print(len(logs))
    return jsonify(logs)


if __name__ == '__main__':
    log_thread = threading.Thread(target=tail_log_file, daemon=True)
    log_thread.start()
    socketio.run(app)
