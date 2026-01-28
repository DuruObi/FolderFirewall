# backend/plugins/shebang.py

from plugins.base import Plugin

class ShebangScanner(Plugin):
    name = "shebang"
    severity = "medium"

    def scan(self, file_path: str):
        try:
            with open(file_path, "r", errors="ignore") as f:
                first_line = f.readline().strip()

            if first_line.startswith("#!"):
                return {
                    "plugin": self.name,
                    "issue": "Executable script detected",
                    "line": first_line
                }

        except Exception:
            pass

        return None
