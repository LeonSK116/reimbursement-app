import os
import psycopg2
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST'),
        port=os.environ.get('PGPORT'),
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        database=os.environ.get('PGDATABASE')
    )
    return conn

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_reimbursement():
    try:
        data = request.form.to_dict()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO reimbursements (name, date, time, amount, reason, category, restaurant_name, destination, distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (data['name'], data['date'], data['time'], data['amount'], data['reason'], data['category'], data.get('restaurant_name'), data.get('destination'), data.get('distance')))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Reimbursement submitted successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
