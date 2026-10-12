@echo off
title OmniCommerce Django Backend
echo Starting Django Backend Server...
cd /d "%~dp0backend"
python manage.py migrate
python seed_data.py
python manage.py runserver
pause
