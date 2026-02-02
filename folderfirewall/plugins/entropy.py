# backend/plugins/entropy.py

import math
from plugins.base import Plugin

class EntropyScanner(Plugin):
    name = "entropy"
    severity = "high"

    def scan(self, file_path: str):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            if not data:
                return None

            # Count byte frequencies
            freq = [0] * 256
            for b in data:
                freq[b] += 1

            entropy = 0
            for count in freq:
                if count == 0:
                    continue
                p = count / len(data)
                entropy -= p * math.log2(p)

            # Threshold for suspiciously high entropy
            if entropy > 7.5:  
                return {
                    "plugin": self.name,
                    "issue": f"High entropy file ({entropy:.2f})",
                    "file": file_path
                }

        except Exception:
            pass

        return None
