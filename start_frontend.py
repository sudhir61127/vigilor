#!/usr/bin/env python3
"""Start VIGIL-OR frontend dev server"""
import subprocess
import os

os.chdir(r"c:\Users\USER\Documents\vigilor\frontend")

# First, install dependencies
print("Installing frontend dependencies...")
subprocess.run("npm install --silent", shell=True, check=False)

# Start dev server
print("\n" + "="*60)
print("Starting VIGIL-OR Frontend Dev Server")
print("="*60)
print("Frontend will be available at: http://localhost:5173")
print("Backend API at: http://localhost:8000")
print("="*60 + "\n")

subprocess.run("npm run dev", shell=True, check=False)
