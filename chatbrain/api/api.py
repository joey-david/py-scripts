# app.py or main.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # For handling cross-origin requests
import utilities
# backend imports

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Basic route
@app.route('/upload', methods=['POST'])
def upload_files():
    correctInput, _ = checkOnReceive(request)
    if not correctInput:
        raise "Invalid file upload : checkOnReceive failed"
    
    files = request.files.getlist('files')
    
    print(request)
    print(request.form)

    file = files[0]
    if file.content_type == 'text/plain':
        # process text file
        response, details = utilities.getTextResponse(
            files,
            request.form['start_date'], 
            request.form['end_date'], 
            request.form['start_time'], 
            request.form['end_time']
        )
        pass
    elif file.content_type == 'audio/mpeg':
        # process audio file
        raise NotImplementedError
    elif file.content_type == 'image/jpeg':
        # process image file
        raise NotImplementedError
    print(response)
    return response

def checkOnReceive(request):
    '''Detects the type of files in the provided list of files from an HTTP POST.'''
    files = request.files.getlist('files')

    general_type = files.pop().content_type

    for file in files:
        if file.content_type != general_type:
            return False, f"File type mismatch: {file.content_type} and {general_type}."
    
    return True, general_type;

if __name__ == '__main__':
    app.run(debug=True)