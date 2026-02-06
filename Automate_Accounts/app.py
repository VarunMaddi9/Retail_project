import os
from flask import Flask, jsonify, request
from PyPDF2 import PdfReader
import sqlite3
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)
from engine.getFileData import get_file_meta_data
from engine.uploadServcie import update_receipt_data, upload_file_metadata
from engine.processService import process_receipt


UPLOAD_FOLDER = "C:\\Users\\Varun Maddi\\Desktop\\Automate_Accounts_Project\\Automate_Accounts\\uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_file():
    # Get metadata from form
    file_id = request.form.get("id")
    
    # Get uploaded file
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "file not uploaded"}), 400
    if not file_id:
        return jsonify({"error": "id missing"}), 400

    # Secure filename and save
    file_name = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    file.save(file_path)

    # Save metadata (your DB logic)
    upload_file_metadata(
        id=file_id,
        file_name=file_name,
        file_path=file_path,
        is_valid=1,
        invalid_reason="N/A",
        is_processed=0
    )

    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

@app.route("/validate", methods=["POST"])
def validate_file():
    print('validate')
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body missing"}), 400

    file_id = data.get("id")
    file_name = data.get("file_name")

    if not file_id or not file_name:
        return jsonify({"error": "id or file_name missing"}), 400

    # Validate that the filename ends with .pdf
    if not file_name.lower().endswith(".pdf"):
        reason = "Filename must end with .pdf"
        update_receipt_data(file_id, reason)
        return jsonify({
            "is_valid": False,
            "invalid_reason": reason
        }), 200
    
    return jsonify({
            "is_valid": True
        }), 200

    

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    if not data or "id" not in data:
        return jsonify({"error": "id missing"}), 400

    result = process_receipt(data["id"])

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@app.route("/receipts", methods=["GET"])
def receipts():
    try:
        with sqlite3.connect("automate.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM receipt")
            rows = cursor.fetchall()

            receipts_list = [dict(row) for row in rows]

        return jsonify(receipts_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/receipts/<int:id>", methods=["GET"])
def receipts_by_id(id):
    try:
        with sqlite3.connect("automate.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM receipt WHERE id = ?", (id,))
            row = cursor.fetchone()

        if row is None:
            return jsonify({"error": "Receipt not found"}), 404

        receipt = dict(row)
        return jsonify(receipt), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
