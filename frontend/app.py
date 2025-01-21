from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://localhost:5001"  # Replace with your backend URL

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    try:
        response = requests.post(f"{BACKEND_URL}/submit", json=data)
        response.raise_for_status()
        return jsonify({"message": "Data submitted successfully"}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
