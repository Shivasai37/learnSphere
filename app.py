from flask import Flask, render_template, request, jsonify, send_file

import os

from genai_utils import generate_text_explanation, generate_code_explanation, generate_audio_script, generate_image_prompts
from audio_utils import generate_audio, cleanup_old_audio
from code_executor import detect_dependencies, save_code_file, get_install_instructions
from image_utils import generate_educational_image



app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "learnsphere_default_key")

# ─── PAGES ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/text")
def text_page():
    return render_template("text.html")

@app.route("/code")
def code_page():
    return render_template("code.html")

@app.route("/audio")
def audio_page():
    return render_template("audio.html")

@app.route("/visual")
def visual_page():
    return render_template("visual.html")

# ─── API ROUTES ──────────────────────────────────────────
@app.route("/api/generate/text", methods=["POST"])
def api_text():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        complexity = data.get("complexity", "Intermediate")
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        explanation = generate_text_explanation(topic, complexity)
        return jsonify({"success": True, "content": explanation, "topic": topic})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate/code", methods=["POST"])
def api_code():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        complexity = data.get("complexity", "Intermediate")
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        code = generate_code_explanation(topic, complexity)
        dependencies = detect_dependencies(code)
        install_info = get_install_instructions(dependencies)
        filename, filepath = save_code_file(code, topic)
        return jsonify({
            "success": True,
            "code": code,
            "dependencies": dependencies,
            "install_instructions": install_info,
            "filename": filename,
            "topic": topic
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate/audio", methods=["POST"])
def api_audio():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        length = data.get("length", "Medium")
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        script = generate_audio_script(topic, length)
        filename, filepath = generate_audio(script, topic)
        cleanup_old_audio()
        return jsonify({
            "success": True,
            "script": script,
            "audio_file": filename,
            "topic": topic
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate/visual", methods=["POST"])
def api_visual():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        prompts_text = generate_image_prompts(topic)
        prompts = [p.strip() for p in prompts_text.split('\n') if p.strip() and p[0].isdigit()]
        
        images = []
        for prompt in prompts[:2]:
            try:
                filename, filepath = generate_educational_image(prompt, topic)
                if filename:
                    images.append(filename)
            except Exception:
                pass
        
        return jsonify({
            "success": True,
            "prompts": prompts,
            "images": images,
            "topic": topic
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─── DOWNLOAD ROUTES ─────────────────────────────────────
@app.route("/download/audio/<filename>")
def download_audio(filename):
    filepath = os.path.join("generated", "audio", filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route("/download/code/<filename>")
def download_code(filename):
    filepath = os.path.join("generated", "code", filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route("/serve/audio/<filename>")
def serve_audio(filename):
    filepath = os.path.join("generated", "audio", filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="audio/mpeg")
    return jsonify({"error": "File not found"}), 404

@app.route("/serve/image/<filename>")
def serve_image(filename):
    filepath = os.path.join("generated", "images", filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="image/png")
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    os.makedirs("generated/audio", exist_ok=True)
    os.makedirs("generated/code", exist_ok=True)
    os.makedirs("generated/images", exist_ok=True)
    app.run(debug=True, port=5000)
