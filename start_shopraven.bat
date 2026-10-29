@echo off
title ShopRaven AI Co-Founder - Local Server
echo ============================================================
echo      🦅 ShopRaven AI Co-Founder for nnstore.shop
echo ============================================================
echo.
echo [1/3] Starting ShopRaven Node.js Orchestrator (Port 4000)...
cd /d "%~dp0\orchestrator"
start "ShopRaven Orchestrator" cmd /k "node src/server.js"

echo [2/3] Opening Control Room Dashboard in your browser...
timeout /t 3 >nul
start http://localhost:4000/nnstore_ai_dashboard.html

echo [3/3] Setting up Free Public WhatsApp Tunnel...
echo.
echo ============================================================
echo  To give Wasender a public HTTPS URL for WhatsApp Webhooks,
echo  open a new terminal window and run ANY of these FREE tunnels:
echo.
echo  OPTION 1 (No install needed, built into Windows):
echo     ssh -p 443 -R0:localhost:4000 a.pinggy.io
echo.
echo  OPTION 2 (LocalTunnel):
echo     npx localtunnel --port 4000
echo.
echo  Copy the HTTPS link shown (e.g. https://xyz.a.pinggy.link)
echo  and paste into Wasender Webhook:
echo     https://xyz.a.pinggy.link/api/whatsapp/webhook
echo ============================================================
echo.
pause
