# app.py
from flask import Flask, request, jsonify
from src.main import process_pdf

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files["file"]
    file.save("data/input_pdfs/uploaded.pdf")
    result = process_pdf("data/input_pdfs/uploaded.pdf")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)