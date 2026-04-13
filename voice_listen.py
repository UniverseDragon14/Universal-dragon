#!/usr/bin/env python3
import json
import os
import wave
from vosk import Model, KaldiRecognizer

MODEL_PATH = os.path.expanduser("~/universal_dragon/nova3/models/vosk-en")
WAV_PATH = "/tmp/nova_cmd.wav"
MIC_DEV = "bluez_input.34:C7:39:24:68:8E"

def record_audio():
    print("🎤 Speak now...")
    os.system(f'timeout 6 parecord --device="{MIC_DEV}" --rate=16000 --channels=1 "{WAV_PATH}" >/dev/null 2>&1')

def transcribe():
    wf = wave.open(WAV_PATH, "rb")
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, wf.getframerate())
    parts = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = json.loads(rec.Result()).get("text", "")
            if part:
                parts.append(part)

    final = json.loads(rec.FinalResult()).get("text", "")
    if final:
        parts.append(final)

    return " ".join(parts).strip()

def normalize_text(text):
    t = (text or "").strip().lower()

    aliases = {
        "are you": "who are you",
        "who are": "who are you",
        "open you tube": "open youtube",
        "youtube": "open youtube",
        "open tube": "open youtube",
        "status": "who are you",
    }

    return aliases.get(t, t)

def main():
    if not os.path.isdir(MODEL_PATH):
        print("❌ Model not found")
        return

    record_audio()
    text = transcribe()
    text = normalize_text(text)

    print("📝 Heard:", text if text else "(nothing)")

    if not text:
        return

    from dragon_terminal import DragonTerminal
    DragonTerminal().process(text)

if __name__ == "__main__":
    main()
