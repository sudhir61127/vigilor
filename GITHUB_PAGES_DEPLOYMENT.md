# GitHub Pages Deployment Guide

This document explains how to set up and configure GitHub Pages deployment for the VIGIL-OR project.

## Overview

The project uses GitHub Actions to automatically build and deploy the React frontend to GitHub Pages whenever changes are pushed to the `main` branch.

**Build Tool**: Vite (React)  
**Build Command**: `npm run build`  
**Build Output**: `frontend/dist/`  
**Deployment Target**: GitHub Pages

## Automated Workflow

The workflow file `.github/workflows/deploy-pages.yml` handles:
1. ✅ Checkout code from main branch
2. ✅ Setup Node.js 18
3. ✅ Install npm dependencies in `/frontend`
4. ✅ Build the frontend with `npm run build`
5. ✅ Upload build artifacts to GitHub Pages
6. ✅ Deploy to GitHub Pages

**Trigger**: Automatically runs on every push to `main` branch

## Required GitHub Repository Configuration

### Step 1: Enable GitHub Pages

1. Go to your repository: `sudhir61127/vigilor`
2. Navigate to **Settings** → **Pages**
3. Under "Build and deployment":
   - **Source**: Select "GitHub Actions" (not "Deploy from a branch")
   - Click "Save"

### Step 2: Verify Permissions

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - ✅ Select "Read and write permissions"
   - ✅ Check "Allow GitHub Actions to create and approve pull requests"
   - Click "Save"

## Initial Deployment

After configuring GitHub Pages:

1. Push any change to the `main` branch:
   ```bash
   git add .
   git commit -m "Enable GitHub Pages deployment"
   git push origin main
   ```

2. Monitor the deployment:
   - Go to your repository
   - Click on **Actions** tab
   - Watch the "Deploy to GitHub Pages" workflow
   - Wait for both "build" and "deploy" jobs to complete

3. Access your deployed site:
   ```
   https://sudhir61127.github.io/vigilor/
   ```

## Environment Configuration

### API Endpoint Configuration

The workflow sets `VITE_API_URL` during the build. By default, it's set to:
```
https://vigilor-api.example.com
```

**To change the API endpoint for production:**

1. Edit `.github/workflows/deploy-pages.yml`
2. Find the `env:` section under "Build project" step:
   ```yaml
   env:
     VITE_API_URL: https://your-api-endpoint.com
   ```
3. Update with your actual API endpoint
4. Push the change to `main`

**Important**: The frontend will use this URL to communicate with the backend API.

## Troubleshooting

### Workflow Failed to Run

**Issue**: The workflow doesn't start when pushing to main

**Solution**:
1. Verify the workflow file is in `.github/workflows/deploy-pages.yml`
2. Check that the file syntax is valid YAML
3. Ensure branch protection rules aren't blocking the workflow
4. Go to **Settings** → **Actions** → **General** and verify permissions are set correctly

### Build Failed

**Issue**: The "Build project" step fails

**Common causes**:
- Missing dependencies: Run `npm install` locally to test
- Incorrect Node.js version: Workflow uses Node.js 18 (should match your development environment)
- Build errors: Run `npm run build` locally to identify issues

**Solution**:
```bash
cd frontend
npm install
npm run build
```

### Deploy Step Failed

**Issue**: Build succeeds but deployment fails

**Possible causes**:
- GitHub Pages not enabled (see Step 1 above)
- Insufficient permissions (see Step 2 above)
- Artifact upload corrupted

**Solution**:
1. Re-enable GitHub Pages (Settings → Pages → Select "GitHub Actions")
2. Verify workflow permissions are set to "Read and write"
3. Re-run the failed workflow: Go to **Actions** → Click workflow → Click "Re-run jobs"

### Site Shows 404 on GitHub Pages

**Issue**: Deployment succeeds but site shows 404 error

**Possible causes**:
- Browser cache
- Incorrect domain

**Solution**:
1. Hard refresh browser: Ctrl+Shift+Del (or Cmd+Shift+Del on Mac)
2. Verify correct URL: `https://sudhir61127.github.io/vigilor/`
3. Check that `frontend/dist/index.html` exists in your build

## Local Testing Before Deployment

To verify the build works locally:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the project
npm run build

# Preview the built site
npm run preview
```

Then access: `http://localhost:4173`

## Important Notes

### About the Backend

The GitHub Pages workflow only deploys the **frontend** (React dashboard). The backend API must be hosted separately:

- **Frontend**: Deployed to GitHub Pages (static files)
- **Backend**: Deploy separately (e.g., Heroku, Railway, AWS, or your own server)

Update `VITE_API_URL` in the workflow to point to your backend deployment.

### Repository Access

Ensure your repository is:
- ✅ Public (required for free GitHub Pages)
- ✅ Or have GitHub Pages enabled for private repos (GitHub Pro feature)

### Build Caching

The workflow uses npm cache to speed up builds:
- Cache key: `frontend/package-lock.json`
- Automatically invalidated when dependencies change

## Continuous Deployment

After initial setup, the workflow operates automatically:

1. **Developer pushes to `main`**
   ↓
2. **GitHub Actions triggers workflow**
   ↓
3. **Workflow builds and tests**
   ↓
4. **Workflow deploys to GitHub Pages**
   ↓
5. **Site is live** at `https://sudhir61127.github.io/vigilor/`

Typical deployment time: **2-5 minutes**

## Monitoring and Logs

### View Workflow Runs

1. Go to repository
2. Click **Actions** tab
3. Select "Deploy to GitHub Pages" workflow
4. Click on individual run to view detailed logs

### Check Deployment Status

1. Go to **Settings** → **Pages**
2. Under "Your site is live at" you'll see:
   - ✅ Current deployment URL
   - 📅 Last deployment timestamp
   - 🔍 Deployment status

## Rollback

To revert to a previous deployment:

1. In GitHub, identify the commit to revert to
2. Push a new commit that reverts the changes:
   ```bash
   git revert <commit-hash>
   git push origin main
   ```
3. GitHub Actions will automatically rebuild and redeploy

The GitHub Pages site will update within 2-5 minutes.

## Advanced Configuration

### Custom Domain (Optional)

To use a custom domain instead of `github.io`:

1. Go to **Settings** → **Pages**
2. Under "Custom domain", enter your domain (e.g., `vigilor.example.com`)
3. Add DNS records to your domain provider:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
            185.199.109.153
            185.199.110.153
            185.199.111.153
   ```
4. Or use CNAME for subdomain:
   ```
   Type: CNAME
   Name: app
   Value: sudhir61127.github.io
   ```

### Scheduled Rebuilds (Optional)

To rebuild the site on a schedule (e.g., daily):

Edit `.github/workflows/deploy-pages.yml` and add:

```yaml
on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:
```

## Summary

✅ **Workflow created**: `.github/workflows/deploy-pages.yml`  
✅ **Ready for deployment**: Push to `main` to trigger automatic deployment  
✅ **Site URL**: `https://sudhir61127.github.io/vigilor/`  
✅ **Backend**: Configure `VITE_API_URL` in workflow for your backend API  

---

**For questions or issues**, refer to the GitHub Actions logs: Repository → Actions tab
