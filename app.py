from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path

from config import Config
from backend.pdf_processor import PDFProcessor
from backend.connection_mapper import ConnectionMapper
from backend.exporter import export_connections

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object(Config)

processor = PDFProcessor()
mapper = ConnectionMapper()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "Brak pliku PDF."}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "Nie wybrano pliku."}), 400

    filename = secure_filename(uploaded_file.filename)
    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Dozwolone są tylko pliki PDF."}), 400

    upload_dir = Path(app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    uploaded_file.save(file_path)

    try:
        extracted_pages = processor.process_pdf(str(file_path))
        connections = mapper.extract_connections(extracted_pages)
        device_summary = mapper.build_device_summary(extracted_pages)

        export_connections(
            connections=connections,
            devices=device_summary,
            output_folder=Path(app.config["OUTPUT_FOLDER"]),
            base_name=file_path.stem,
        )

        payload = {
            "filename": filename,
            "pages": len(extracted_pages),
            "connections_count": len(connections),
            "devices_count": len(device_summary),
            "devices": device_summary,
            "connections": connections,
            "files": {
                "csv": f"/download/{file_path.stem}.csv",
                "xlsx": f"/download/{file_path.stem}_lista_polaczen.xlsx",
                "json": f"/download/{file_path.stem}.json",
            },
        }

        return jsonify(payload)

    except Exception as exc:
        return jsonify({"error": f"Błąd przetwarzania PDF: {str(exc)}"}), 500


@app.route("/download/<path:filename>")
def download_file(filename):
    output_dir = Path(app.config["OUTPUT_FOLDER"])
    return send_from_directory(output_dir, filename, as_attachment=True)


if __name__ == "__main__":
    print("Uruchamiam aplikację...")
    app.run(host="0.0.0.0", port=5000, debug=True)
