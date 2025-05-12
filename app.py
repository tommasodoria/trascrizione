import os
from flask import Flask, request, render_template, send_file
import whisper
from deep_translator import GoogleTranslator
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def index():
    trascrizione = ""
    traduzione = ""
    if request.method == "POST":
        file = request.files["audio_file"]
        lang_source = request.form["lang_source"]
        lang_target = request.form["lang_target"]

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            result = model.transcribe(filepath, language=None if lang_source == "auto" else lang_source)
            trascrizione = result["text"]

            if lang_target != lang_source:
                traduzione = GoogleTranslator(source='auto', target=lang_target).translate(trascrizione)
            else:
                traduzione = trascrizione

    return render_template("index.html", trascrizione=trascrizione, traduzione=traduzione)

if __name__ == "__main__":
    app.run(debug=True)
