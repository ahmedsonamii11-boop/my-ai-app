@echo off
cd /d "%USERPROFILE%\Desktop"
start /b python -m streamlit run app.py >nul 2>&1
timeout /t 3 >nul
start http://localhost:8501