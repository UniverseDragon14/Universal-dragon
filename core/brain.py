import os
import time
import requests
from typing import Dict

class NOVA3Brain:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
        self.ollama_host = "http://localhost:11434"
        self.commander = "Aslam"
        self.project = "Universal Dragon"
        self.identity = "NOVA3"
        self.offline_mode = True
        self._check_connectivity()

    def _check_connectivity(self):
        try:
            requests.get("https://generativelanguage.googleapis.com", timeout=3)
            self.offline_mode = False
        except Exception:
            self.offline_mode = True

    def think(self, prompt: str, context: str = "") -> Dict:
        q = (prompt or "").strip().lower()

        if q in ["who are you", "who r u", "what is your name", "un peru enna"]:
            return {
                "source": "nova_identity",
                "text": "I am NOVA3, the brain core of Universal Dragon. My creator and commander is Aslam.",
                "model": "nova_identity"
            }

        if "tamil" in q:
            return {
                "source": "nova_skill",
                "text": "Yes, I can understand Tamil and English. Konjam simple-ah kelunga, naan help pannuren.",
                "model": "nova_skill"
            }

        if "coding" in q or "code" in q or "programming" in q:
            return {
                "source": "nova_skill",
                "text": "Yes, I can help with coding, debugging, Python, HTML, CSS, JavaScript, and project building.",
                "model": "nova_skill"
            }

        if q.startswith("create website"):
            return self._create_project(prompt, "web")

        if q.startswith("create app"):
            return self._create_project(prompt, "app")

        return self._chat(prompt)

    def _chat(self, prompt: str) -> Dict:
        system_prompt = f"""
You are NOVA3, the AI brain core of Universal Dragon.
Creator and Commander: {self.commander}.

Rules:
- Speak naturally.
- Do NOT repeat your identity in every answer.
- Only mention creator/identity when the user asks who you are.
- Keep replies short, useful, and clear.
- You understand English and simple Tamil/Tanglish.
"""

        full_prompt = system_prompt + f"\nUser: {prompt}\nNOVA3:"

        if not self.offline_mode and self.gemini_key != "YOUR_API_KEY_HERE":
            try:
                return self._gemini_call(full_prompt)
            except Exception:
                return self._ollama_call(full_prompt)

        return self._ollama_call(full_prompt)

    def _sanitize_identity(self, text: str) -> str:
        if not text:
            return "NOVA3 online."

        low = text.lower()
        if "llama" in low or "meta ai" in low:
            return "I am NOVA3, the brain core of Universal Dragon. My creator and commander is Aslam."

        return text.strip()

    def _ollama_call(self, prompt: str, retries: int = 2) -> Dict:
        for attempt in range(retries):
            try:
                response = requests.post(
                    self.ollama_host + "/api/generate",
                    json={
                        "model": "llama3.2",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )
                result = response.json()
                text = self._sanitize_identity(result.get("response", ""))
                return {
                    "source": "ollama",
                    "text": text,
                    "model": "llama3.2"
                }
            except Exception as e:
                if attempt == retries - 1:
                    return {
                        "source": "error",
                        "text": f"NOVA3 temporary offline: {e}",
                        "model": "none"
                    }
                time.sleep(1)

    def _gemini_call(self, prompt: str) -> Dict:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + self.gemini_key
        response = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=15
        )
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        text = self._sanitize_identity(text)
        return {
            "source": "gemini",
            "text": text,
            "model": "gemini-1.5-flash"
        }

    def _create_project(self, prompt: str, ptype: str) -> Dict:
        name = prompt.lower().replace("create website", "").replace("create app", "").strip()
        name = name or "project"
        name = name.split()[0]

        base_path = os.path.expanduser(f"~/universal_dragon/nova3/projects/{name}_{ptype}")
        os.makedirs(base_path, exist_ok=True)
        created = []

        if ptype == "web":
            files = {
                "index.html": f"""<!DOCTYPE html>
<html>
<head><title>{name}</title><link rel="stylesheet" href="style.css"></head>
<body>
<h1>🐉 {name}</h1>
<p>Universal Dragon project created by NOVA3 for Aslam.</p>
<script src="app.js"></script>
</body>
</html>""",
                "style.css": "body{font-family:monospace;background:#0a0a0a;color:#ff00ff;text-align:center;padding-top:10vh;}",
                "app.js": f"console.log('NOVA3 created {name}');"
            }
        else:
            files = {
                "main.py": f"""#!/usr/bin/env python3
def main():
    print("NOVA3 app online: {name}")
if __name__ == "__main__":
    main()
""",
                "requirements.txt": "requests\n"
            }

        for fname, content in files.items():
            with open(os.path.join(base_path, fname), "w") as f:
                f.write(content)
            created.append(fname)

        return {
            "source": "nova_project_engine",
            "text": f"Created {ptype} project '{name}' for Commander Aslam.",
            "model": "nova_creator",
            "created": created
        }

brain = NOVA3Brain()
