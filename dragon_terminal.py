#!/usr/bin/env python3
import os
import sys
import subprocess

PINK = "\033[95m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"

class DragonTerminal:
    def __init__(self):
        self.commander = "ASLAM"
        self.voice_enabled = self.check_voice()

    def check_voice(self):
        try:
            subprocess.run(["which", "espeak-ng"], capture_output=True, check=True)
            return True
        except Exception:
            return False

    def speak(self, text):
        text = (text or "").strip()
        if not text:
            return

        clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
        clean_text = clean_text[:180]

        print(f"{CYAN}🗣️  NOVA: {text}{RESET}")

        if self.voice_enabled:
            try:
                subprocess.Popen(
                    ["espeak-ng", "-ven+f4", "-s118", "-a8", "-p75", "-k2", clean],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception as e:
                print(f"{GRAY}[voice error: {e}]{RESET}")

    def header(self):
        os.system("clear")
        print(f"{PINK}{'='*50}{RESET}")
        print(f"{PINK}⚡ UNIVERSAL DRAGON OS - FIELD TERMINAL v3.1 ⚡{RESET}")
        print(f"{CYAN}COMMANDER : {self.commander}{RESET}")
        print(f"{CYAN}BRAIN     : NOVA3 (Hybrid Core){RESET}")
        print(f"{CYAN}VOICE     : {'ON' if self.voice_enabled else 'OFF'}{RESET}")
        print(f"{PINK}{'='*50}{RESET}")
        print(f"{GRAY}Commands: create website <name> | create app <name> | open youtube | search python | exit{RESET}\n")

    def process(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return

        low = cmd.lower()

        if low in ["exit", "quit", "sleep"]:
            self.speak("Going to sleep mode. Call me when you need me, Commander.")
            sys.exit(0)

        if low == "clear":
            self.header()
            return

        if low.startswith("open "):
            site = cmd[5:].strip()
            self.speak(f"Opening {site}")
            os.system(f"xdg-open https://{site}.com >/dev/null 2>&1 &")
            return

        if low.startswith("search "):
            query = cmd[7:].strip()
            self.speak(f"Searching for {query}")
            os.system(f"xdg-open 'https://google.com/search?q={query}' >/dev/null 2>&1 &")
            return

        if low.startswith("run "):
            bash_cmd = cmd[4:].strip()
            self.speak(f"Executing {bash_cmd}")
            os.system(bash_cmd)
            return

        self.ai_chat(cmd)

    def ai_chat(self, msg):
        print(f"{YELLOW}🧠 NOVA3 thinking...{RESET}")
        try:
            from core.brain import brain
            result = brain.think(msg)
            text = result.get("text", "").strip()
            source = result.get("source", "unknown")

            if source == "error":
                print(f"{RED}❌ {text}{RESET}")
                return

            if "created" in result:
                created = result.get("created", [])
                print(f"{GREEN}✅ Created {len(created)} files:{RESET}")
                for f in created:
                    print(f"   📄 {f}")

            self.speak(text)

        except Exception as e:
            print(f"{RED}❌ Brain error: {e}{RESET}")

    def run(self):
        self.header()
        self.speak("NOVA3 online. Ready for your commands, Commander.")
        while True:
            try:
                cmd = input(f"{YELLOW}DRAGON >> {RESET}").strip()
                self.process(cmd)
            except KeyboardInterrupt:
                print(f"\n{RED}Use exit to quit properly.{RESET}")
            except EOFError:
                break

if __name__ == "__main__":
    DragonTerminal().run()
