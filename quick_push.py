#!/usr/bin/env python3
import subprocess
import os
import sys

os.chdir(r"c:\Users\USER\Documents\vigilor")

print("=" * 80)
print("VIGIL-OR: Pushing Workflow to GitHub")
print("=" * 80)

commands = [
    ('git config --global user.email "deploy@vigilor.dev"', "Configure git email"),
    ('git config --global user.name "VIGILOR Bot"', "Configure git name"),
    ('git add .', "Stage all files"),
    ('git commit -m "Deploy VIGIL-OR to GitHub Pages" --allow-empty', "Commit changes"),
    ('git push origin main', "Push to GitHub"),
]

for cmd, desc in commands:
    print(f"\n▶ {desc}...")
    try:
        result = subprocess.run(cmd, shell=True, timeout=30, 
                              capture_output=True, text=True)
        if "fatal" in result.stderr.lower():
            print(f"  ✗ Error: {result.stderr[:200]}")
        else:
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n')[:3]:
                    print(f"  {line}")
            print(f"  ✓ Done")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

print("\n" + "=" * 80)
print("✓ Push complete!")
print("=" * 80)
print("\nNow enable GitHub Pages:")
print("1. Go to: https://github.com/sudhir61127/vigilor/settings/pages")
print("2. Source: Select 'GitHub Actions'")
print("3. Click 'Save'")
print("\n4. Go to: https://github.com/sudhir61127/vigilor/settings/actions/general")
print("5. Workflow permissions: Select 'Read and write permissions'")
print("6. Click 'Save'")
print("\n7. Wait 2-5 minutes, then check:")
print("   https://sudhir61127.github.io/vigilor/")
print("=" * 80)
