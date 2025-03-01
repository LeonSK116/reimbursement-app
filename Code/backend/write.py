import os
import psycopg2
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database connection using psycopg2 and environment variables
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST_WRITE'),
        port=os.environ.get('PGPORT'),
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        database=os.environ.get('PGDATABASE')
    )
    return conn

# Route to handle reimbursement submissions
@app.route('/api/submit', methods=['POST'])
def submit_reimbursement():
    try:
        # Explicitly check Content-Type header
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Invalid Content-Type'}), 400

        # Get data from the request body
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        # Check if 'name' field is present
        if 'name' not in data:
            return jsonify({'error': 'Name field is missing'}), 400

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()
        # Insert data into the reimbursements table, including file_location
        cur.execute("INSERT INTO reimbursements (name, date, time, amount, reason, category, restaurant_name, destination, distance, file_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (data['name'], data['date'], data['time'], data['amount'], data['reason'], data['category'], data.get('restaurant_name'), data.get('destination'), data.get('distance'), data.get('file_location')))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Reimbursement submitted successfully!'}), 201
    except psycopg2.Error as e:
        logging.exception(f"PostgreSQL error: {e}")
        return jsonify({'error': f"PostgreSQL error: {e}"}), 500
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
