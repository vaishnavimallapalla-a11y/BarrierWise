cd C:\Users\hichi\.gemini\antigravity\scratch\barrierwise\backend
.\venv\Scripts\activate
python seed.py
Start-Process "uvicorn" -ArgumentList "main:app --port 8000" -NoNewWindow
cd ..\frontend
Start-Process "npm.cmd" -ArgumentList "run dev" -NoNewWindow
