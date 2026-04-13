#!/usr/bin/env python3
import os
import subprocess
import pvporcupine
from pvrecorder import PvRecorder

ACCESS_KEY = "PUT_YOUR_PICOVOICE_ACCESS_KEY_HERE"
BUILTIN_KEYWORD = "jarvis"

def launch_nova3():
    subprocess.Popen(
        ["bash", "-lc", "cd ~/universal_dragon/nova3 && source venv/bin/activate && python3 dragon_terminal.py"],
        start_new_session=True
    )

def main():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=[BUILTIN_KEYWORD]
    )
    print("🎙️ Listening for wake word: jarvis")

    devices = PvRecorder.get_available_devices()
    for i, d in enumerate(devices):
        print(f"{i}: {d}")

    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    recorder.start()

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            if result >= 0:
                print("🔥 Wake word detected")
                os.system("espeak-ng -ven+f3 -s145 -k20 'Yes Commander' >/dev/null 2>&1 &")
                launch_nova3()
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        recorder.delete()
        porcupine.delete()

if __name__ == "__main__":
    main()
