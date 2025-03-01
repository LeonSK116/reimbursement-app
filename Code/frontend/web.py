from flask import Flask, render_template, request, jsonify
import requests
import os
import uuid
app = Flask(__name__)

# Backend URLs for write and read operations
# Example: URL_WRITE=http://localhost:5001/api/submit, URL_READ=http://localhost:5002/api/data
API_DB_WRITE = os.environ.get("URL_WRITE")
API_DB_READ = os.environ.get("URL_READ")
API_UPLOAD = os.environ.get("URL_UPLOAD")

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

# Route to handle file uploads
@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        category = request.form['category']
        if category not in ['food', 'transportation', 'mobile']:
            return jsonify({'error': 'Invalid category'}), 400

        # Create a unique filename
        filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
        # Construct file path based on category. Do not include BUCKET name here.
        file_location = f'/{category}/{filename}'

        # Forward the request to the backend upload API
        try:
            upload_response = requests.post(f"{API_UPLOAD}", files={'file': file}, data={'category': category})
            upload_response.raise_for_status()
            return jsonify(upload_response.json()), upload_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
