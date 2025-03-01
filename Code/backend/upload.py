import os
import boto3
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# S3 client
aws_region = os.environ.get('AWS_REGION')
s3_client = boto3.client('s3', region_name=aws_region)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Get the file and category from the request
        file = request.files['file']
        category = request.form['category']

        # Validate the category
        if category not in ['food', 'transportation', 'mobile']:
            return jsonify({'error': 'Invalid category'}), 400

        # Create a unique filename
        filename = file.filename
        # Construct file path based on category.
        file_path = f'{category}/{filename}'

        # Get the bucket name from the environment variable
        bucket_name = os.environ.get('BUCKET_NAME')
        if not bucket_name:
            return jsonify({'error': 'BUCKET_NAME environment variable not set'}), 500

        # Upload the file to S3
        s3_client.upload_fileobj(file, bucket_name, file_path)

        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
