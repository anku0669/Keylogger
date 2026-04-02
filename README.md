# Keylogger
# 🔑 Universal Keylogger Pentest Tool

**Cross-platform credential capture for authorized pentesting**

## 🎯 Quick Deploy

**Linux/macOS:**
```bash
chmod +x deploy.sh && ./deploy.sh

Windows:
deploy.bat

📡 Usage
Terminal 1 - Capture:
bash
python keylogger.py
ESC stops capture

Terminal 2 - View:
bash
python viewer.py          # All logs
python viewer.py -l 50    # Last 50 lines

🛡️ Technical Details
Feature	Status
AES-256 Encryption	✅
Cross-platform	✅ Win/Linux/Mac
Special Keys	✅ Enter/Tab/Space/BS
Background Mode	✅
Stealth Logging	✅
Memory Safe	✅ Auto-flush

Files generated:
keystrokes.enc - Encrypted logs
key.key - Decryption key
keylog.out - Status
