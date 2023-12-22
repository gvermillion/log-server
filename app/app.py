import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
LOG_FILE = '/app/log/server.log'

def tail_log_file():
    with open(LOG_FILE, 'r') as file:
        file.seek(0, 2)  # Move to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly
                continue
            socketio.emit(
                'log_update', 
                {
                    'data': line.strip(),
                    'level': line.split('] ')[1].split(': ')[0].strip()
                }
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_logs')
def all_logs():
    filter_substring = request.args.get('filter', '')

    try:
        with open(LOG_FILE, 'r') as file:
            if filter_substring:
                logs = [line for line in file if filter_substring in line]
            else:
                logs = file.readlines()
    except FileNotFoundError:
        logs = ["Log file not found."]
    return jsonify(logs)
if __name__ == '__main__':
    open(LOG_FILE, 'a').close()
    log_thread = threading.Thread(target=tail_log_file, daemon=True)
    log_thread.start()
    socketio.run(
        app,
        allow_unsafe_werkzeug=True,
        host='0.0.0.0',
        port=5000
    )
