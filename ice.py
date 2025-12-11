import os
import subprocess

PROJECT_PATH = os.getcwd()
VENV_PY = r"C:\Users\Win\Documents\python-core\Scripts\python.exe"
REQ_FILE = os.path.join(PROJECT_PATH, "requirements.txt")

# Get installed packages in the venv
freeze_output = subprocess.check_output([VENV_PY, "-m", "pip", "freeze"], text=True)
installed = dict()
for line in freeze_output.strip().splitlines():
    if "==" in line:
        pkg, ver = line.split("==")
        installed[pkg.lower()] = line

# Scan .py files for top-level imports
imports = set()
for root, dirs, files in os.walk(PROJECT_PATH):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("import "):
                            imports.add(line.split()[1].split(".")[0].lower())
                        elif line.startswith("from "):
                            imports.add(line.split()[1].split(".")[0].lower())
            except Exception:
                continue

# Match imports to installed packages
requirements = [installed[mod] for mod in sorted(imports) if mod in installed]

# Write requirements.txt
with open(REQ_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(requirements))

print(f"requirements.txt created at {REQ_FILE}")
