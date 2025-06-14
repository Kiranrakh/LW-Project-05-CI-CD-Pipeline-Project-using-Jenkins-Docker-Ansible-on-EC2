from flask import Flask, render_template, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", hostname=socket.gethostname())

@app.route('/health')
def health():
    return jsonify(status="UP", app="Flask CI-CD App", container=socket.gethostname())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
