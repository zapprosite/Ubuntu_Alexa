#!/usr/bin/env python3
import os
import sys
import time
import json
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

CONFIG_PATH = Path(__file__).parent / "config" / "assistant.yaml"


def load_config():
    cfg = {
        "language": "pt-BR",
        "stt": {"engine": os.getenv("ASSISTANT_STT", "vosk"), "enabled": False},
        "tts": {"engine": os.getenv("ASSISTANT_TTS", "piper"), "enabled": False},
        "llm": {
            "primary": os.getenv("ASSISTANT_MODEL_PRIMARY", "gpt-5"),
            "fallback": os.getenv("ASSISTANT_MODEL_FALLBACK", "llama3.1:8b-instruct"),
            "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        },
        "safety": {"confirm_destructive": True},
    }
    if yaml and CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                file_cfg = yaml.safe_load(f) or {}
                # shallow merge
                for k, v in file_cfg.items():
                    if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                        cfg[k].update(v)  # type: ignore
                    else:
                        cfg[k] = v
        except Exception:
            pass
    return cfg


def check_ollama(host: str) -> str:
    try:
        import requests  # type: ignore

        r = requests.get(host.rstrip("/") + "/api/tags", timeout=1.2)
        if r.ok:
            return "ollama:ok"
        return f"ollama:http_{r.status_code}"
    except Exception as e:
        return f"ollama:err:{type(e).__name__}"


def simulate_voice_to_intent(text: str) -> dict:
    t = text.strip().lower()
    if "abrir navegador" in t or "abrir browser" in t:
        return {"intent": "open_app", "args": {"app": "browser", "url": "http://localhost:3300"}}
    return {"intent": "unknown", "args": {"text": text}}


def exec_intent(intent: dict, confirm: bool = True):
    name = intent.get("intent")
    args = intent.get("args", {})
    if name == "open_app" and args.get("app") == "browser":
        if confirm:
            print("Assistant: Confirmar ação 'abrir navegador'? (s/N)", flush=True)
            ans = os.getenv("ASSISTANT_AUTOCONFIRM") or sys.stdin.readline().strip().lower()
            if ans not in ("s", "sim", "y", "yes"):  # deny by default
                print("Assistant: ação cancelada.")
                return
        url = args.get("url") or "about:blank"
        # Prefer xdg-open if available; fallback print
        try:
            import shutil
            if shutil.which("xdg-open"):
                os.system(f"xdg-open '{url}' >/dev/null 2>&1 &")
                print(f"Assistant: abrindo navegador em {url}")
            else:
                print(f"Assistant: (simulado) abrir {url}")
        except Exception:
            print(f"Assistant: (simulado) abrir {url}")
    else:
        print("Assistant: intenção desconhecida.")


def main():
    cfg = load_config()
    print("[assistant] config:", json.dumps(cfg, ensure_ascii=False))
    print("[assistant] checks:")
    print(" -", check_ollama(cfg["llm"].get("ollama_host", "http://localhost:11434")))
    print(" - TTS:", "enabled" if cfg["tts"]["enabled"] else "disabled")
    print(" - STT:", "enabled" if cfg["stt"]["enabled"] else "disabled")

    # CLI text-mode (safe default)
    print("Digite um comando (ex.: 'abrir navegador') e ENTER. CTRL+C para sair.")
    try:
        while True:
            sys.stdout.write("> ")
            sys.stdout.flush()
            line = sys.stdin.readline()
            if not line:
                time.sleep(0.1)
                continue
            intent = simulate_voice_to_intent(line)
            exec_intent(intent, confirm=cfg.get("safety", {}).get("confirm_destructive", True))
    except KeyboardInterrupt:
        print("\n[assistant] bye")


if __name__ == "__main__":
    main()

