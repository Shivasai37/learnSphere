from gtts import gTTS
import os
import time
import tempfile

def generate_audio(script_text, topic):
    try:
        timestamp = int(time.time())
        filename = f"audio_{timestamp}.mp3"
        
        # Try local generated folder first, fallback to tmp
        local_dir = os.path.join(os.getcwd(), "generated", "audio")
        try:
            os.makedirs(local_dir, exist_ok=True)
            filepath = os.path.join(local_dir, filename)
        except:
            tmp_dir = tempfile.gettempdir()
            local_dir = os.path.join(tmp_dir, "audio")
            os.makedirs(local_dir, exist_ok=True)
            filepath = os.path.join(local_dir, filename)

        # Clean script - remove special characters that break gTTS
        clean_script = script_text.encode('ascii', 'ignore').decode('ascii')
        if not clean_script.strip():
            clean_script = script_text  # fallback to original

        tts = gTTS(text=clean_script, lang='en', slow=False)
        tts.save(filepath)
        
        return filename, filepath
    except Exception as e:
        raise Exception(f"Audio generation failed: {str(e)}")

def cleanup_old_audio(max_files=20):
    try:
        local_dir = os.path.join(os.getcwd(), "generated", "audio")
        if not os.path.exists(local_dir):
            return
        files = sorted(
            [os.path.join(local_dir, f) for f in os.listdir(local_dir) if f.endswith(".mp3")],
            key=os.path.getmtime
        )
        while len(files) > max_files:
            os.remove(files.pop(0))
    except:
        pass
