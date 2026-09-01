#!/usr/bin/env python3
"""Deploy to GitHub Pages by pushing to main branch"""
import subprocess
import os
import sys

os.chdir(r"c:\Users\USER\Documents\vigilor")

print("=" * 70)
print("VIGIL-OR GitHub Pages Deployment")
print("=" * 70)

# Check git status
print("\n📋 Checking repository status...")
result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
if result.stdout:
    print(result.stdout)
else:
    print("✓ No uncommitted changes")

# Add all changes
print("\n📦 Adding changes...")
subprocess.run(["git", "add", "."], check=True)
print("✓ Changes added")

# Commit
print("\n💾 Committing changes...")
result = subprocess.run(
    ["git", "commit", "-m", "Configure GitHub Pages deployment workflow"],
    capture_output=True,
    text=True
)
if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
    print("ℹ  No new changes to commit")
else:
    print(result.stdout if result.stdout else result.stderr)

# Push to main
print("\n🚀 Pushing to GitHub (main branch)...")
result = subprocess.run(
    ["git", "push", "origin", "main"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print(result.stdout if result.stdout else "✓ Push successful")
    print("\n" + "=" * 70)
    print("✅ DEPLOYMENT INITIATED")
    print("=" * 70)
    print("\n🔗 GitHub Actions Workflow:")
    print("   https://github.com/sudhir61127/vigilor/actions")
    print("\n📊 Watch the 'Deploy to GitHub Pages' workflow")
    print("   - Build step: Installs & builds frontend")
    print("   - Deploy step: Pushes to GitHub Pages")
    print("   Typical time: 2-5 minutes")
    print("\n🌐 Live Site (after deployment):")
    print("   https://sudhir61127.github.io/vigilor/")
    print("\n" + "=" * 70)
else:
    print("❌ Push failed:")
    print(result.stderr)
    sys.exit(1)
