from flask import Flask
app = Flask(__name__)
from engine.uploadServcie import uploadFileMetadata

@app.route("/upload", methods=['POST'])
def upload_file(request):
    print("viewst")
    uploadFileMetadata(request)
    return ('', 200)

@app.route("/validate", methods=['POST'])
def validate_file():
    return ('', 200)

@app.route("/process", methods=['POST'])
def upload_file():
    return ('', 200)

@app.route("/receipts", methods=['GET'])
def upload_file():
    return ('', 200)

@app.route("/receipts/id", methods=['GET'])
def upload_file():
    return ('', 200)