from flask import Flask, request, jsonify
from transcript_converter import convert_transcript_to_json
from pathlib import Path

app = Flask(__name__)

@app.post("/convert")
def convert_transcript():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    upload_path = Path("uploads") / file.filename
    Path("uploads").mkdir(exist_ok=True)
    file.save(upload_path)

    output_path = Path("parsed") / f"{Path(file.filename).stem}_logic.json"
    Path("parsed").mkdir(exist_ok=True)

    convert_transcript_to_json(upload_path, output_path)

    return jsonify({
        "message": "Transcript conversion complete",
        "output": str(output_path)
    })

if __name__ == "__main__":
    app.run(debug=True)
