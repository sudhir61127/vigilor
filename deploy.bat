@echo off
cd /d c:\Users\USER\Documents\vigilor
echo.
echo ================================================================================
echo VIGIL-OR GitHub Pages Deployment
echo ================================================================================
echo.
echo Deploying to GitHub Pages...
echo.

REM Configure git if needed
git config --global user.email "vigilor@example.com" >nul 2>&1
git config --global user.name "VIGIL-OR Deployment" >nul 2>&1

REM Add all changes
echo [1/4] Adding changes...
git add .
if errorlevel 1 goto error

REM Commit changes
echo [2/4] Committing...
git commit -m "Configure GitHub Pages deployment workflow" --allow-empty
if errorlevel 1 if not errorlevel 128 goto error

REM Push to main
echo [3/4] Pushing to GitHub...
git push origin main
if errorlevel 1 goto error

echo.
echo [4/4] Complete!
echo.
echo ================================================================================
echo ^✅ DEPLOYMENT INITIATED
echo ================================================================================
echo.
echo GitHub Actions Workflow:
echo   https://github.com/sudhir61127/vigilor/actions
echo.
echo Watch the 'Deploy to GitHub Pages' workflow (2-5 minutes)
echo.
echo Live Site (after deployment):
echo   https://sudhir61127.github.io/vigilor/
echo.
echo ================================================================================
pause
exit /b 0

:error
echo.
echo ================================================================================
echo ^❌ ERROR: Deployment failed
echo ================================================================================
echo.
pause
exit /b 1
