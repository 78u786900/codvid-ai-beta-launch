#!/usr/bin/env python3
"""
Instagram Analytics Dashboard - Run Script

This script provides an easy way to run the Streamlit web app.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    print("🚀 Starting CodVid.AI Instagram Analytics Platform...")
    print("📱 Premium, mobile-optimized web app for Instagram analytics")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        print("Please run this script from the web_app directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import streamlit
        import requests
        import pandas
        import plotly
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the Streamlit app
    try:
        print("🌐 Starting Streamlit server...")
        print("📱 The app will open in your browser at http://localhost:8501")
        print("🔄 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 