"""SafeFarm Myanmar - Streamlit Cloud Entry Point"""

import sys
import os

# Add safefarm directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'safefarm'))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main()
