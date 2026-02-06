import os
from flask import Flask, jsonify, request
from PyPDF2 import PdfReader
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
from engine.getFileData import get_file_meta_data
from engine.uploadServcie import upload_file_metadata

UPLOAD_FOLDER = "C:\Users\Varun Maddi\Desktop\Automate_Accounts_Project\Automate_Accounts\uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_file():

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body missing"}), 400

    file_id = data.get("id")
    file_name = data.get("file_name")

    if not file_id or not file_name:
        return jsonify({"error": "id or file_name missing"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)

    upload_file_metadata(
        id=file_id,
        file_name=file_name,
        file_path=file_path,
        is_valid=0,
        invalid_reason="N/A",
        is_processed=0
    )

    return jsonify({"message": "Metadata inserted successfully"}), 200

@app.route("/validate", methods=["POST"])
def validate_file():
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body missing"}), 400
    
    file_path = get_file_meta_data(data.get("id"))

    file = os.read()
    
    if "file" not in request.files:
        return jsonify({
            "is_valid": False,
            "invalid_reason": "File not found"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "is_valid": False,
            "invalid_reason": "Empty filename"
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "is_valid": False,
            "invalid_reason": "Not a PDF file"
        }), 400

    try:
        reader = PdfReader(file)
        pages = len(reader.pages)

        if pages == 0:
            return jsonify({
                "is_valid": False,
                "invalid_reason": "PDF has no pages"
            }), 400

        return jsonify({
            "is_valid": True,
            "pages": pages,
            "message": "Valid PDF"
        }), 200

    except Exception:
        return jsonify({
            "is_valid": False,
            "invalid_reason": "Corrupted or unreadable PDF"
        }), 400

@app.route("/process", methods=['POST'])
def process():
    return ('', 200)

@app.route("/receipts", methods=["GET"])
def receipts():

    try:
        conn = sqlite3.connect("automate.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM receipt")
        rows = cursor.fetchall()

        receipts_list = []

        for row in rows:
            receipts_list.append({
                "id": row["id"],
                "purchased_at": row["purchased_at"],
                "merchant_name": row["merchant_name"],
                "total_amount": row["total_amount"],
                "file_path": row["file_path"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })

        conn.close()

        return jsonify(receipts_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/receipts/<int:id>", methods=["GET"])
def receipts_by_id(id):

    try:
        conn = sqlite3.connect("automate.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM receipt WHERE id = ?", (id,))
        row = cursor.fetchone()

        conn.close()

        if row is None:
            return jsonify({"error": "Receipt not found"}), 404

        receipt = {
            "id": row["id"],
            "purchased_at": row["purchased_at"],
            "merchant_name": row["merchant_name"],
            "total_amount": row["total_amount"],
            "file_path": row["file_path"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }

        return jsonify(receipt), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
