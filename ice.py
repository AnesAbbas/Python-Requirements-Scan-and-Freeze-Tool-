import os
import subprocess
import re

# -------------------------
# CONFIGURATION
# -------------------------
# Current project directory
PROJECT_PATH = os.getcwd()

# Path to the Python executable of the virtual environment
VENV_PY = r"C:\Users\Win\Documents\python-core\Scripts\python.exe"

# Path to the output requirements.txt file
REQ_FILE = os.path.join(PROJECT_PATH, "requirements.txt")

# Map import names to PyPI package names (for cases where they differ)
IMPORT_PACKAGE_MAP = {
    "pil": "Pillow",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "lxml": "lxml",
    # Add more mappings as needed
}

# -------------------------
# GET INSTALLED PACKAGES IN THE VENV
# -------------------------
# Use pip freeze to get a list of installed packages and versions
freeze_output = subprocess.check_output([VENV_PY, "-m", "pip", "freeze"], text=True)

# Store installed packages in a dictionary: {package_name_lower: "package==version"}
installed = {}
for line in freeze_output.strip().splitlines():
    if "==" in line:
        pkg, ver = line.split("==")
        installed[pkg.lower()] = line

# -------------------------
# SCAN PYTHON FILES FOR IMPORTS
# -------------------------
# Sets to store detected module names
imports = set()
dynamic_imports = set()

# Walk through all files in the project directory recursively
for root, dirs, files in os.walk(PROJECT_PATH):
    for file in files:
        if file.endswith(".py"):  # Only process Python files
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # -------------------------
                    # STATIC IMPORTS
                    # -------------------------
                    for line in content.splitlines():
                        line = line.strip()
                        if line.startswith("import "):
                            # Example: "import requests" → "requests"
                            imports.add(line.split()[1].split(".")[0].lower())
                        elif line.startswith("from "):
                            # Example: "from flask import Flask" → "flask"
                            imports.add(line.split()[1].split(".")[0].lower())
                    # -------------------------
                    # DYNAMIC IMPORTS
                    # -------------------------
                    # Detect __import__("module_name") calls
                    matches = re.findall(r'__import__\(["\']([\w\d_]+)["\']\)', content)
                    dynamic_imports.update(m.lower() for m in matches)
                    # Detect importlib.import_module("module_name") calls
                    matches = re.findall(r'importlib\.import_module\(["\']([\w\d_]+)["\']\)', content)
                    dynamic_imports.update(m.lower() for m in matches)
            except Exception:
                # Skip files that cannot be read
                continue

# Merge dynamic imports into the main imports set
imports.update(dynamic_imports)

# -------------------------
# MATCH IMPORTS TO INSTALLED PACKAGES
# -------------------------
# Prepare list of requirements by checking if detected imports exist in the virtual environment
requirements = []
for mod in sorted(imports):
    # Map tricky imports to actual PyPI package names
    pkg_name = IMPORT_PACKAGE_MAP.get(mod, mod)
    if pkg_name.lower() in installed:
        requirements.append(installed[pkg_name.lower()])

# -------------------------
# WRITE requirements.txt
# -------------------------
with open(REQ_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(requirements))

print(f"requirements.txt created at {REQ_FILE}\n")

# -------------------------
# PRINT CONTENTS OF requirements.txt
# -------------------------
print("----- requirements.txt -----")
with open(REQ_FILE, "r", encoding="utf-8") as f:
    print(f.read())
print("----------------------------")
