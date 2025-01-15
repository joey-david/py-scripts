from flask import Flask, request, jsonify, Response, stream_with_context  # For handling cross-origin requests
import utilities
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Basic route
@app.route('/llm', methods=['POST'])
def get_llm_analysis():
    correctInput, filetype = checkOnReceive(request)
    if not correctInput:
        raise Exception("Invalid file upload : checkOnReceive failed")  # Changed line
    # print the contents of the files
    print(request.files.getlist('files'))
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
        raise Exception("Invalid file upload : checkOnReceive failed")  # Changed line
    if fileType == 'text':
        response = utilities.getTextMetadata(files)
    elif fileType == 'audio':
        raise NotImplementedError
    elif fileType == 'image':
        raise NotImplementedError
    else:
        raise Exception("Unsupported file type")
    return response

@app.route('/analysis-progress', methods=['GET'])
def progress():
    def generate():
        yield "data: {\"status\": \"processing\"}\n\n"
        yield "data: {\"status\": \"compressing\"}\n\n"
        yield "data: {\"status\": \"metadata\"}\n\n"
        yield "data: {\"status\": \"analysis\"}\n\n"
        yield "data: {\"status\": \"done\"}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/event-stream',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    )

def checkOnReceive(request):
    '''Detects the type of files in the provided list of files from an HTTP POST.'''
    files = request.files.getlist('files')

    general_type = files[0].content_type.split('/')[0]

    for file in files:
        if file.content_type.split('/')[0] != general_type:
            return False, f"File type mismatch: {file.content_type} and {general_type}."
    
    return True, general_type

if __name__ == '__main__':
    app.run(debug=True)