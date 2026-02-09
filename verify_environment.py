import sys
import os
import importlib
import pathlib

# Ensure project root is in sys.path for script execution
project_root = pathlib.Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

print("========================================")
print("   RECEIPT VAULT ANALYZER DIAGNOSTICS   ")
print("========================================")
print(f"Python Executable: {sys.executable}")
print(f"Current Directory: {os.getcwd()}")
print(f"Project Root:      {project_root}")

required_packages = [
    "streamlit",
    "google.generativeai",
    "pandas",
    "pytesseract",
    "PIL",
    "plotly",
    "dotenv",
    "cv2",
    "numpy"
]

print("\n--- Checking Dependencies ---")
for package in required_packages:
    try:
        if package == "PIL":
            importlib.import_module("PIL")
        elif package == "dotenv":
            importlib.import_module("dotenv")
        else:
            importlib.import_module(package)
        print(f"✅ {package:20} imported successfully")
    except ImportError as e:
        print(f"❌ {package:20} FAILED to import: {e}")

print("\n--- Checking Local Project Modules ---")

def check_import(module_name: str):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name:20} imported successfully")
    except ImportError as e:
        print(f"❌ {module_name:20} FAILED to import: {e}")
        # Help diagnose why it failed
        parts = module_name.split('.')
        current_path = project_root
        for part in parts:
            current_path = current_path / part
            if not current_path.exists() and not current_path.with_suffix(".py").exists():
                print(f"   ↳ Path not found: {current_path}")

local_modules = [
    "ai.gemini_client",
    "ai.prompts",
    "ui.sidebar",
    "database.queries",
    "ocr.text_parser"
]

for module in local_modules:
    check_import(module)

print("\n--- Troubleshooting IDE Errors ---")
print("If you see red squiggles in VS Code but the checks above passed:")
print("1. Command Palette (Ctrl+Shift+P) -> 'Python: Select Interpreter'")
print(f"2. Ensure it is set to: {os.path.join(project_root, 'venv', 'Scripts', 'python.exe')}")
print("3. Command Palette -> 'Developer: Reload Window'")
print("========================================")
