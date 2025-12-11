`ice` is a Python utility that scans a project directory for top-level imports, matches them with packages installed in a specified Python virtual environment, and generates a `requirements.txt` file. It can be run from **any project folder** in Windows Command Line.

---

## Features

* Automatically scans all `.py` files in the project directory and subdirectories
* Detects `import` and `from ... import ...` statements
* Matches imports with packages installed in a virtual environment
* Creates or updates `requirements.txt`
* Prints the generated `requirements.txt` contents in the console
* Can be run globally from any project folder

---

## Prerequisites

* Python installed (tested with Python 3.11+)
* A Python virtual environment (any location)
* Windows OS

---

## Installation

1. **Save the Python script**

   Save `ice.py` in a folder, e.g.:

   ```
   C:\Users\Win\Documents\scripts\ice.py
   ```

2. **Create a wrapper `.bat` file**

   Create `ice.bat` in the same folder:

   ```bat
    @echo off
    :: Get the directory where this BAT file lives
    set SCRIPT_DIR=%~dp0

    :: Call Python from PATH and run genreq.py inside this same directory
    python "%SCRIPT_DIR%ice.py"
   ```

3. **Add folder to PATH**

   Add `C:\Users\Win\Documents\scripts\` to your system PATH.

---

## Usage

Open **Command Prompt** in any project folder:

```
cd C:\Projects\MyApp
ice
```

Example output:

```
requirements.txt created at C:\Projects\MyApp\requirements.txt

----- requirements.txt -----
requests==2.32.3
pillow==10.4.0
numpy==2.1.1
----------------------------
```

---

## Configuration

* **Python virtual environment**: Set `VENV_PY` in the script to point to the `python.exe` of your virtual environment:

```python
VENV_PY = r"C:\Users\Win\Documents\python-core\Scripts\python.exe"
```

* **Project directory**: The script automatically uses the current working directory (`os.getcwd()`).

---

## Limitations

* Package names must match the installed PyPI package name exactly (some imports like `PIL` → `Pillow` may need manual mapping inside ice.py file)
* Designed for **Windows CMD**; may need minor changes for Linux/macOS

---

## License

MIT License — free to use and modify.

---
