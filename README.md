# Universal Dragon — Local NOVA3 Prototype

Local Python assistant and voice-control experiments for Linux/Raspberry Pi environments.

## Repository map

| Path | Current role |
|---|---|
| dragon_terminal.py | interactive terminal, speech output, browser shortcuts, and command dispatch |
| core/brain.py | local Ollama/Gemini chat routing and small project generation |
| nova_voice.py | voice-facing NOVA launcher |
| voice_listen.py | offline Vosk audio transcription |
| wake_listener.py | Porcupine wake-word listener |
| launcher.sh / nova3_launcher.sh | local launch helpers |
| nova3_guard.sh | process guard/restart helper |
| models/vosk-en | bundled offline English speech model |
| projects | generated/example web and Python projects |

## AI routing

The brain prefers configured Gemini access when available and otherwise calls a local Ollama server using the configured local model path. These are software model integrations; no physical QPU is involved.

## Basic start

~~~bash
python3 -m venv .venv
. .venv/bin/activate
pip install requests vosk pvporcupine pvrecorder
python3 dragon_terminal.py
~~~

Voice features also require suitable audio packages/devices and optional espeak-ng.

## Important current limitations

- The terminal includes an unrestricted run command and shell-built open/search commands. Use only on a trusted local machine; do not expose it as a network service.
- Project names are not fully path-sanitized before file creation.
- Audio device/model configuration is machine-specific.
- The current speech function references the wrong variable name when calling espeak-ng, so spoken output needs a code fix.
- Wake-word access needs a valid locally supplied provider key.
- Generated project files are templates, not automatically reviewed production applications.

## Pi and hardware truth boundary

This repository can run software on a Raspberry Pi and use configured audio devices. It does not prove that every Pi service, GPIO device, camera, robot, or external integration is connected or active.

Before wider use, replace shell-string execution with fixed argument allowlists, validate project paths, add an approval gate, and test recovery/rollback.
