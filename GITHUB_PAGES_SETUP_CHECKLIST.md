# GitHub Pages Setup Checklist

Complete these steps to enable GitHub Pages deployment for the vigilor project.

## Pre-Deployment Checklist

### Files Created ✓
- [x] `.github/workflows/deploy-pages.yml` - GitHub Actions workflow
- [x] `GITHUB_PAGES_DEPLOYMENT.md` - Comprehensive deployment guide
- [x] Updated `frontend/vite.config.js` - GitHub Pages base path configured

### Project Configuration ✓
- [x] Build command: `npm run build`
- [x] Build output: `frontend/dist/`
- [x] Framework: React 18.2.0 + Vite 5.0.0
- [x] GitHub Pages base path: `/vigilor/`

## Repository Configuration (GitHub)

### Step 1: Enable GitHub Pages
**Time: 2-3 minutes**

1. Go to https://github.com/sudhir61127/vigilor
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Select **Source**: "GitHub Actions"
   - (Leave other options as default)
   - Page refreshes automatically

### Step 2: Verify Workflow Permissions
**Time: 1-2 minutes**

1. Still in **Settings**
2. Click **Actions** → **General** (left sidebar)
3. Scroll to "Workflow permissions"
4. Select: **✓ Read and write permissions**
5. Check: **✓ Allow GitHub Actions to create and approve pull requests**
6. Click **Save**

### Step 3: Trigger Initial Deployment
**Time: 5-10 minutes**

Option A: Push a change to main
```bash
cd vigilor
git add .
git commit -m "Configure GitHub Pages deployment"
git push origin main
```

Option B: Manual trigger (if already pushed)
1. Go to your repository
2. Click **Actions** tab
3. Find "Deploy to GitHub Pages" workflow on the left
4. Click **Run workflow** → **Run workflow**

### Step 4: Monitor Deployment
**Time: 2-5 minutes**

1. Go to **Actions** tab
2. Watch the "Deploy to GitHub Pages" workflow
3. You should see two jobs:
   - ✓ build (installs, builds frontend)
   - ✓ deploy (pushes to GitHub Pages)

### Step 5: Verify Live Site
**Time: 1 minute**

1. Go to **Settings** → **Pages**
2. You should see: "Your site is live at https://sudhir61127.github.io/vigilor/"
3. Click the link to visit your live site
4. Verify the VIGIL-OR dashboard loads

## Status After Setup

| Component | Status | Details |
|-----------|--------|---------|
| Workflow | ✅ Ready | `.github/workflows/deploy-pages.yml` |
| Build | ✅ Automatic | Runs on push to `main` |
| Deployment | ✅ Automatic | Deploys built files to GitHub Pages |
| Site URL | ✅ Live | https://sudhir61127.github.io/vigilor/ |
| Base Path | ✅ Configured | `/vigilor/` in vite.config.js |

## Next Steps

### Backend Configuration (Important!)
The GitHub Pages deployment is **frontend-only**. To make the dashboard fully functional:

1. **Deploy the backend API**:
   - Choose a hosting platform (Heroku, Railway, AWS, DigitalOcean, etc.)
   - Deploy the Python FastAPI backend
   - Get your backend URL (e.g., `https://vigilor-api.herokuapp.com`)

2. **Update the workflow with API endpoint**:
   - Edit `.github/workflows/deploy-pages.yml`
   - Find the `Build project` step's `env:` section
   - Change `VITE_API_URL` to your backend URL:
   ```yaml
   env:
     VITE_API_URL: https://your-backend-url.com
   ```
   - Commit and push

3. **Test the connection**:
   - Open the live site: https://sudhir61127.github.io/vigilor/
   - Navigate to any view that calls the backend
   - Verify data loads correctly

### Optional: Custom Domain
If you own a domain, you can use it instead of GitHub Pages:

1. Settings → Pages → Custom domain
2. Add your domain (e.g., `vigilor.example.com`)
3. Configure DNS records at your domain registrar
4. GitHub will auto-generate an SSL certificate

## Troubleshooting

### "GitHub Pages not enabled" error
- Go to Settings → Pages
- Ensure Source is set to "GitHub Actions"
- Click Save

### Workflow doesn't run
- Check file exists: `.github/workflows/deploy-pages.yml`
- Go to Actions tab to see any errors
- Verify you have write permissions to the repo

### Site shows 404
- Hard refresh browser (Ctrl+Shift+Del or Cmd+Shift+Del)
- Correct URL: https://sudhir61127.github.io/vigilor/
- Check that workflow completed successfully

### API calls fail on live site
- Verify backend is deployed and running
- Check `VITE_API_URL` in workflow file matches backend URL
- Check CORS is configured on backend for GitHub Pages domain

## Testing Locally

Before pushing to production, test the production build locally:

```bash
cd frontend

# Install dependencies
npm install

# Build for production (sets base path)
npm run build

# Preview production build locally
npm run preview
```

Then visit: http://localhost:4173

## Continuous Updates

After initial setup, the workflow runs automatically:

1. Make changes to frontend code
2. Push to `main` branch
3. GitHub Actions automatically:
   - Installs dependencies
   - Builds the project
   - Deploys to GitHub Pages
4. Live site updates within 2-5 minutes

## Important Notes

### Deployment Time
- First build: ~3-5 minutes
- Subsequent builds: ~2-3 minutes (with npm cache)

### Build Process
- Runs on Ubuntu latest
- Uses Node.js 18
- Installs only frontend dependencies
- Backend is not included in GitHub Pages deployment

### Automatic Updates
- Deploys on every push to `main`
- No manual deployment step needed
- Previous versions remain in GitHub repository history

### Browser Caching
- First visit: Page loads fresh from GitHub Pages
- Subsequent visits: May use browser cache
- Hard refresh (Ctrl+Shift+Del) to see latest version

## Support Resources

- GitHub Pages Docs: https://docs.github.com/en/pages
- GitHub Actions Docs: https://docs.github.com/en/actions
- Vite Docs: https://vitejs.dev/
- React Docs: https://react.dev/

## Quick Links

- 🔗 Live Site: https://sudhir61127.github.io/vigilor/
- 📋 Workflow File: `.github/workflows/deploy-pages.yml`
- 📖 Guide: `GITHUB_PAGES_DEPLOYMENT.md`
- ⚙️ Config: `frontend/vite.config.js`

---

**Setup Complete!** Your VIGIL-OR dashboard is ready for GitHub Pages deployment. ✨
