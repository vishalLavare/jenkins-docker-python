from flask import Flask, jsonify

app = Flask(__name__)

# Root route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"msg": "Welcome to the Flask App!"})

# /hello route
@app.route("/hello", methods=["GET"])
def say_hello():
    return jsonify({"msg": "Hello from Flask!"})

if __name__ == "__main__":
    # Debug should be disabled in production
    app.run(host="0.0.0.0", port=5000, debug=True)
