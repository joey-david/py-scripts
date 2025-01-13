# app.py or main.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # For handling cross-origin requests
import utilities
# backend imports

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Basic route
@app.route('/api/files', methods=['GET'])
def globalHandle():
    # filetype = utilities.filedetect blablabla
    return jsonify({"message": "Hello World!"})

if __name__ == '__main__':
    app.run(debug=True)