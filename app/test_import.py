import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app
    print("Application imported successfully")
except Exception as e:
    print(f"Error importing application: {e}")
    import traceback
    traceback.print_exc()