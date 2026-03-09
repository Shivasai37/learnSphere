import requests
import os
import time

def get_groq_key():
    try:
        with open('.env') as f:
            for line in f:
                if line.startswith('GROQ_API_KEY'):
                    return line.strip().split('=', 1)[1]
    except:
        pass
    return os.environ.get('GROQ_API_KEY', '')

def call_groq(prompt):
    api_key = get_groq_key()
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2048
    }
    response = requests.post(url, json=body, headers=headers, timeout=60)
    data = response.json()
    if "choices" not in data:
        raise Exception("Groq API error")
    return data["choices"][0]["message"]["content"]

def generate_diagram_code(topic):
    prompt = f"""
Generate Python code using matplotlib to create a clear educational diagram about: {topic}

Rules:
- Use matplotlib and numpy only
- White background
- Clear labels and title
- Use plt.savefig('output.png', dpi=150, bbox_inches='tight', facecolor='white')
- Do NOT use plt.show()
- Make it look like a textbook diagram
- Return ONLY the Python code, no explanation, no markdown

Example structure:
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(...)
# draw diagram
plt.savefig('output.png', dpi=150, bbox_inches='tight', facecolor='white')
"""
    return call_groq(prompt)

def generate_educational_image(prompt, topic):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        timestamp = int(time.time())
        filename = f"image_{timestamp}.png"
        filepath = os.path.join("generated", "images", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Get diagram code from Groq
        code = generate_diagram_code(topic)

        # Clean code - remove markdown if present
        code = code.replace('```python', '').replace('```', '').strip()

        # Replace output path with our path
        code = code.replace("'output.png'", f"'{filepath}'")
        code = code.replace('"output.png"', f'"{filepath}"')

        # Execute the generated code
        exec_globals = {
            'plt': plt,
            'np': np,
            'matplotlib': matplotlib
        }
        exec(code, exec_globals)
        plt.close('all')

        if os.path.exists(filepath):
            return filename, filepath

        return None, None

    except Exception as e:
        # Fallback: generate a simple default diagram
        return generate_fallback_diagram(topic, filepath, filename)

def generate_fallback_diagram(topic, filepath, filename):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')

        # Draw simple flow boxes
        boxes = [
            (1, 2.5, 'Input\nData'),
            (3.5, 2.5, 'Processing\nLayer'),
            (6, 2.5, 'Feature\nExtraction'),
            (8.5, 2.5, 'Output'),
        ]
        colors = ['#4f8ef7', '#7c5cfc', '#22d3a5', '#f59e42']

        for i, (x, y, label) in enumerate(boxes):
            rect = mpatches.FancyBboxPatch(
                (x - 0.8, y - 0.6), 1.6, 1.2,
                boxstyle="round,pad=0.1",
                facecolor=colors[i], edgecolor='white', linewidth=2
            )
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center',
                   fontsize=9, color='white', fontweight='bold')

            if i < len(boxes) - 1:
                ax.annotate('', xy=(boxes[i+1][0] - 0.8, boxes[i+1][1]),
                           xytext=(x + 0.8, y),
                           arrowprops=dict(arrowstyle='->', color='#333', lw=2))

        ax.set_title(f'{topic} — Architecture Overview',
                    fontsize=13, fontweight='bold', pad=20, color='#1a1a2e')

        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close('all')

        if os.path.exists(filepath):
            return filename, filepath
        return None, None

    except Exception as e:
        return None, None
