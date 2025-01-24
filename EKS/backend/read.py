import os
import psycopg2
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database connection using psycopg2 and environment variables
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST_READ'),
        port=os.environ.get('PGPORT'),
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        database=os.environ.get('PGDATABASE')
    )
    return conn

@app.route('/api/data', methods=['GET'])
def get_all_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reimbursements")
        rows = cur.fetchall()
        
        # Get column names from cursor description
        columns = [col[0] for col in cur.description]
        
        data = []
        for row in rows:
            # Convert row to dictionary using column names
            row_dict = dict(zip(columns, row))
            # Convert time object to string for JSON serialization
            if 'time' in row_dict and row_dict['time']:
                row_dict['time'] = str(row_dict['time'])
            data.append(row_dict)
        
        cur.close()
        conn.close()
        return jsonify(data)
    except psycopg2.Error as e:
        logging.exception(f"PostgreSQL error: {e}")
        return jsonify({'error': f"PostgreSQL error: {e}"}), 500
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
