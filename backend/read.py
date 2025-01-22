import os
import psycopg2
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST'),
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
        conn.close()
        
        data = [dict(row) for row in rows]
        return jsonify(data)
    except psycopg2.Error as e:
        logging.exception(f"PostgreSQL error: {e}")
        return jsonify({'error': f"PostgreSQL error: {e}"}), 500
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
