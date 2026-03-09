import ast
import os
import time

COMMON_PACKAGES = {
    'numpy': 'numpy', 'np': 'numpy', 'pandas': 'pandas', 'pd': 'pandas',
    'matplotlib': 'matplotlib', 'plt': 'matplotlib', 'seaborn': 'seaborn',
    'sklearn': 'scikit-learn', 'tensorflow': 'tensorflow', 'tf': 'tensorflow',
    'torch': 'torch', 'keras': 'keras', 'scipy': 'scipy', 'cv2': 'opencv-python',
    'PIL': 'Pillow', 'xgboost': 'xgboost', 'lightgbm': 'lightgbm'
}

def detect_dependencies(code_text):
    dependencies = set()
    try:
        tree = ast.parse(code_text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split('.')[0]
                    if root in COMMON_PACKAGES:
                        dependencies.add(COMMON_PACKAGES[root])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root = node.module.split('.')[0]
                    if root in COMMON_PACKAGES:
                        dependencies.add(COMMON_PACKAGES[root])
    except Exception:
        pass
    return list(dependencies)

def save_code_file(code_text, topic):
    timestamp = int(time.time())
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic)[:30]
    filename = f"{safe_topic}_{timestamp}.py"
    filepath = os.path.join("generated", "code", filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write(code_text)
    
    return filename, filepath

def get_install_instructions(dependencies):
    if not dependencies:
        return "No external dependencies required."
    pip_cmd = "pip install " + " ".join(dependencies)
    colab_cmd = "!pip install " + " ".join(dependencies)
    return {
        "local": pip_cmd,
        "colab": colab_cmd,
        "packages": dependencies
    }
