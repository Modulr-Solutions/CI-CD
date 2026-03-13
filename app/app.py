from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "app": "demo-app",
        "version": "1.0.0",
        "status": "ok"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/hello/<name>")
def hello(name):
    return jsonify({"message": f"Bonjour, {name} !"}), 200

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)