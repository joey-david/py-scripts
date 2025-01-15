# app.py or main.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # For handling cross-origin requests
import utilities
# backend imports

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Basic route
@app.route('/llm', methods=['POST'])
def upload_files():
    correctInput, filetype = checkOnReceive(request)
    if not correctInput:
        raise "Invalid file upload : checkOnReceive failed"
    
    files = request.files.getlist('files')
    
    if filetype == 'text':
        # process text file
        json, response = utilities.getTextAnalysis(
            files,
            request.form['start_date'], 
            request.form['end_date'], 
            request.form['start_time'], 
            request.form['end_time']
        )
        pass
    elif filetype == 'audio':
        # process audio file
        raise NotImplementedError
    elif filetype == 'image':
        # process image file
        raise NotImplementedError
    else :
        raise Exception("Unsupported file type")
    return json

@app.route('/metadata', methods=['POST'])
def get_metadata_analysis():
    files = request.files.getlist('files')
    correctInput, fileType = checkOnReceive(request)
    if not correctInput:
        raise "Invalid file upload : checkOnReceive failed"
    
    if fileType == 'text':
        response = utilities.getTextMetadata(files)
    elif fileType == 'audio':
        raise NotImplementedError
    elif fileType == 'image':
        raise NotImplementedError
    return response
    


def checkOnReceive(request):
    '''Detects the type of files in the provided list of files from an HTTP POST.'''
    files = request.files.getlist('files')

    general_type = files.pop().content_type.split('/')[0]
    print(f"General type: {general_type}")

    for file in files:
        if file.content_type != general_type:
            return False, f"File type mismatch: {file.content_type} and {general_type}."
    
    return True, general_type;

if __name__ == '__main__':
    app.run(debug=True)