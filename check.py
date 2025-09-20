#!/usr/bin/env python3
import importlib
import os
import sys

def main():
    print("Python:")
    print(sys.version.split(" ")[0])
    print("pip:")
    try:
        import pip  # type: ignore
        print(getattr(pip, "__version__", "unknown"))
    except Exception:
        print("(pip not found)")
    print("Packages:")
    mods = ["yaml","requests","pyautogui","webrtcvad"]
    for m in mods:
        try:
            importlib.import_module(m)
            print(f" - {m}: ok")
        except Exception as e:
            print(f" - {m}: missing ({type(e).__name__})")
    print("Env:")
    for k in ["OLLAMA_HOST","ASSISTANT_MODEL_PRIMARY","ASSISTANT_MODEL_FALLBACK"]:
        print(f" - {k} = {os.getenv(k,'')}")

if __name__ == "__main__":
    main()

