#!/usr/bin/env python3
"""
Deploy VIGIL-OR to GitHub Pages
This script handles pushing changes and verifying deployment
"""
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ {description} successful")
            if result.stdout.strip():
                print(result.stdout.strip())
            return True
        else:
            print(f"✗ {description} failed")
            if result.stderr.strip():
                print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 80)
    print("VIGIL-OR GitHub Pages Deployment Fix")
    print("=" * 80)
    
    import os
    os.chdir(r"c:\Users\USER\Documents\vigilor")
    
    # Step 1: Configure git
    print("\n[1/5] Configuring Git...")
    run_command('git config user.email "vigilor@github.com"', "Set git email")
    run_command('git config user.name "VIGIL-OR Deployment"', "Set git name")
    
    # Step 2: Check status
    print("\n[2/5] Checking repository status...")
    result = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("Files to commit:")
        print(result.stdout)
    else:
        print("✓ No uncommitted changes")
    
    # Step 3: Add and commit
    print("\n[3/5] Adding and committing changes...")
    run_command("git add .", "Stage all files")
    run_command(
        'git commit -m "Deploy VIGIL-OR to GitHub Pages with automated workflow" --allow-empty',
        "Commit changes"
    )
    
    # Step 4: Push to GitHub
    print("\n[4/5] Pushing to GitHub...")
    if run_command("git push origin main", "Push to main branch"):
        print("\n✓ Push successful!")
    else:
        print("\n✗ Push failed - check your GitHub credentials")
        return False
    
    # Step 5: Instructions
    print("\n" + "=" * 80)
    print("✓ DEPLOYMENT PUSHED TO GITHUB")
    print("=" * 80)
    print("\n📋 NEXT STEPS - Enable GitHub Pages in Repository Settings:")
    print("\n1. Go to: https://github.com/sudhir61127/vigilor/settings/pages")
    print("\n2. Under 'Build and deployment':")
    print("   - Source: Select 'GitHub Actions' from dropdown")
    print("   - Click 'Save'")
    print("\n3. Go to: https://github.com/sudhir61127/vigilor/settings/actions/general")
    print("   - Workflow permissions: Select 'Read and write permissions'")
    print("   - Check: 'Allow GitHub Actions to create and approve pull requests'")
    print("   - Click 'Save'")
    print("\n4. Watch deployment at:")
    print("   https://github.com/sudhir61127/vigilor/actions")
    print("\n5. After 2-5 minutes, visit:")
    print("   https://sudhir61127.github.io/vigilor/")
    print("\n" + "=" * 80)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
