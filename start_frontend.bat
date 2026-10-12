@echo off
title OmniCommerce Frontend Server
echo Starting Vue 3 + Vite Frontend...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)
npm run dev
pause
