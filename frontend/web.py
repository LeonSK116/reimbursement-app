from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL_WRITE = "http://localhost:5001"
BACKEND_URL_READ = "http://localhost:5002"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()
    try:
        response = requests.post(f"{BACKEND_URL_WRITE}/api/submit", json=data)
        response.raise_for_status()
        return jsonify({"message": "Data submitted successfully"}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data')
def view():
    try:
        response = requests.get(f'{BACKEND_URL_READ}/api/data')
        response.raise_for_status()
        data = response.json()
        return render_template('data.html', data=data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
