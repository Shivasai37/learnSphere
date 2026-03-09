from gtts import gTTS
import os
import time

def generate_audio(script_text, topic):
    try:
        timestamp = int(time.time())
        filename = f"audio_{timestamp}.mp3"
        filepath = os.path.join("generated", "audio", filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        tts = gTTS(text=script_text, lang='en', slow=False)
        tts.save(filepath)
        
        return filename, filepath
    except Exception as e:
        raise Exception(f"Audio generation failed: {str(e)}")

def cleanup_old_audio(max_files=20):
    audio_dir = os.path.join("generated", "audio")
    if not os.path.exists(audio_dir):
        return
    files = sorted(
        [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".mp3")],
        key=os.path.getmtime
    )
    while len(files) > max_files:
        os.remove(files.pop(0))
