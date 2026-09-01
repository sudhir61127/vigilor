# VIGIL-OR GitHub Pages Deployment - Manual Steps

Due to terminal execution constraints, please complete the deployment manually using these steps:

## Step 1: Commit and Push Changes

Open your terminal/command prompt and run:

```bash
cd c:\Users\USER\Documents\vigilor

# Add all changes
git add .

# Commit the deployment configuration
git commit -m "Configure GitHub Pages deployment with automated workflow"

# Push to GitHub
git push origin main
```

**Expected output**:
```
[main xxxxxxx] Configure GitHub Pages deployment with automated workflow
 3 files changed, 150 insertions(+), 5 deletions(-)
 create mode: .github/workflows/deploy-pages.yml
 create mode: GITHUB_PAGES_DEPLOYMENT.md
 create mode: GITHUB_PAGES_SETUP_CHECKLIST.md
 create mode: deploy.bat
 create mode: deploy_to_pages.py
```

## Step 2: Enable GitHub Pages in Repository Settings

1. Go to: https://github.com/sudhir61127/vigilor
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar under Code and automation)
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions" from dropdown
   - Click **Save**

## Step 3: Configure Workflow Permissions

1. In **Settings**, click **Actions** → **General** (left sidebar)
2. Scroll to "Workflow permissions"
3. Select: **✓ Read and write permissions**
4. Check: **✓ Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

## Step 4: Monitor Deployment

1. Go to your repository: https://github.com/sudhir61127/vigilor
2. Click **Actions** tab (top menu)
3. You should see "Deploy to GitHub Pages" workflow in progress
4. Click on it to watch the build progress
5. Wait for both jobs to complete:
   - ✓ **build** - Installs dependencies and builds frontend
   - ✓ **deploy** - Deploys to GitHub Pages

**Typical time**: 2-5 minutes

## Step 5: Verify Live Site

1. Go back to **Settings** → **Pages**
2. You should see a green checkmark with: "Your site is live at https://sudhir61127.github.io/vigilor/"
3. Click the link to visit your live VIGIL-OR dashboard

## What Was Configured

✅ **Workflow File**: `.github/workflows/deploy-pages.yml`
   - Automatically builds frontend on push to `main`
   - Deploys to GitHub Pages
   
✅ **Vite Configuration**: Updated `frontend/vite.config.js`
   - Sets correct base path: `/vigilor/`
   
✅ **Documentation**:
   - `GITHUB_PAGES_DEPLOYMENT.md` - Comprehensive guide
   - `GITHUB_PAGES_SETUP_CHECKLIST.md` - Quick reference

## Troubleshooting

### Workflow fails to run
- Ensure GitHub Pages is enabled (Settings → Pages → Source: "GitHub Actions")
- Check workflow permissions (Actions → General → "Read and write permissions")

### "Your site is live" not showing
- Wait 2-5 minutes for deployment to complete
- Refresh the Settings → Pages page
- Check Actions tab for any errors

### Site shows 404
- Hard refresh browser: Ctrl+Shift+Del (Windows) or Cmd+Shift+Del (Mac)
- Correct URL: https://sudhir61127.github.io/vigilor/

### API calls fail
- Backend API needs to be deployed separately
- Update `VITE_API_URL` in `.github/workflows/deploy-pages.yml` with your backend URL
- Redeploy by pushing another change to `main`

## Next: Configure Backend API

The frontend is now deployed to GitHub Pages. To make it fully functional:

1. **Deploy the backend** (Python FastAPI) to a service like:
   - Railway (recommended for free tier)
   - Render
   - Heroku
   - Your own server

2. **Get your backend URL** (e.g., `https://vigilor-api.railway.app`)

3. **Update the workflow**:
   - Edit `.github/workflows/deploy-pages.yml`
   - Find the "Build project" step and update:
   ```yaml
   env:
     VITE_API_URL: https://your-backend-url.com
   ```

4. **Commit and push**:
   ```bash
   git add .github/workflows/deploy-pages.yml
   git commit -m "Update API endpoint for production"
   git push origin main
   ```

5. **Redeploy**: Workflow runs automatically, site updates in 2-5 minutes

## Files Created/Modified

```
.github/
  workflows/
    deploy-pages.yml           ← New: GitHub Actions workflow
frontend/
  vite.config.js              ← Modified: Added base path for GitHub Pages
GITHUB_PAGES_DEPLOYMENT.md    ← New: Detailed deployment guide
GITHUB_PAGES_SETUP_CHECKLIST.md ← New: Quick setup reference
deploy.bat                     ← New: Windows batch deployment script
deploy_to_pages.py            ← New: Python deployment script
```

## Quick Links

- 🔗 Live Site: https://sudhir61127.github.io/vigilor/
- 📋 Repository: https://github.com/sudhir61127/vigilor
- 🔧 Actions: https://github.com/sudhir61127/vigilor/actions
- ⚙️ Pages Settings: https://github.com/sudhir61127/vigilor/settings/pages

---

**Status**: Ready for deployment ✅
**Next**: Complete manual steps above to activate GitHub Pages workflow
