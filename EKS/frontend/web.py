from flask import Flask, render_template, request, jsonify
import requests
import os
app = Flask(__name__)

# Backend URLs for write and read operations
# Example: URL_WRITE=http://localhost:5001/api/submit, URL_READ=http://localhost:5002/api/data
API_DB_WRITE = os.environ.get("URL_WRITE")
API_DB_READ = os.environ.get("URL_READ")

# Route for the main index page
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle form submissions
@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()
    try:
        # Send data to the backend write API
        response = requests.post(f"{API_DB_WRITE}", json=data)
        response.raise_for_status()
        return jsonify({"message": "Data submitted successfully"}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Route to handle data retrieval and display
@app.route('/api/data')
def view():
    try:
        # Fetch data from the backend read API
        response = requests.get(f'{API_DB_READ}')
        response.raise_for_status()
        data = response.json()
        # Render the data.html template with the retrieved data
        return render_template('data.html', data=data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
