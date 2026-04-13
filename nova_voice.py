#!/usr/bin/env python3
import subprocess
from core.brain import brain

def speak(text: str):
    text = (text or "").strip()
    if not text:
        return
    clean = text.replace('"', '').replace("'", "").replace("\n", " ")[:180]
    subprocess.Popen(
        ["espeak-ng", "-ven+f4", "-s118", "-a8", "-p75", "-k2", clean],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def main():
    print("🔊 NOVA3 Voice Mode Online")
    print("Type: hi / who are you / create website nova / open youtube / exit")

    while True:
        try:
            cmd = input("NOVA3 >> ").strip()
            if not cmd:
                continue

            if cmd.lower() in ["exit", "quit"]:
                speak("Going to sleep mode. Call me when you need me, Commander.")
                print("Bye.")
                break

            if cmd.lower().startswith("open "):
                site = cmd[5:].strip()
                print(f"Opening {site}...")
                speak(f"Opening {site}")
                subprocess.Popen(
                    ["bash", "-lc", f"xdg-open https://{site}.com >/dev/null 2>&1 &"]
                )
                continue

            result = brain.think(cmd)
            text = result.get("text", "No reply")
            print("NOVA:", text)
            speak(text)

        except KeyboardInterrupt:
            print("\nUse exit")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
