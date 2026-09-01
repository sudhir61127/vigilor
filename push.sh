#!/bin/bash
# Direct push script without interactive prompts
cd c:\Users\USER\Documents\vigilor

# Set git credentials
git config --global user.email "deploy@vigilor.dev"
git config --global user.name "VIGILOR Deploy Bot"

# Stage and commit
git add .
git commit -m "Deploy VIGIL-OR to GitHub Pages with automated workflow" --no-edit

# Push to GitHub
git push origin main --force

# Check result
if [ $? -eq 0 ]; then
    echo "✓ Successfully pushed to GitHub!"
    echo "Workflow file should now be visible at:"
    echo "https://github.com/sudhir61127/vigilor/blob/main/.github/workflows/deploy-pages.yml"
else
    echo "✗ Push failed - check GitHub token/credentials"
fi
