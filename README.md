# Ubuntu_Alexa — Assistant de Voz (Set/2025)

Repositório do assistant (voz/áudio) extraído do projeto Zappro via git subtree split — pasta agents/assistant virou a raiz deste repo.

## O que tem aqui
- assistant.py: modo CLI (texto), integra com LLM (Ollama/GPT) por variáveis de ambiente.
- check.py: diagnóstico de ambiente (Python, pacotes, variáveis).
- config/assistant.yaml: configura STT/TTS/LLM (vosk/piper opcionais).
- requirements.txt: dependências mínimas.

## Pré‑requisitos
- Python 3.10+ e venv.
- Opcional: ffmpeg, portaudio19-dev para TTS/STT locais.

## Como rodar (3 passos)
1) Criar venv e instalar dependências: make install
2) Diagnóstico rápido: make assistant-check
3) Iniciar (texto): make assistant-dev

## STT/TTS (opcionais)
- STT (vosk) e TTS (piper) podem ser instalados com pip e configurados no config/assistant.yaml.
- Ambiente Ubuntu (DevContainer com áudio): instale libs de áudio (ex.: portaudio19-dev).

## LLM
- Ollama local: exporte OLLAMA_HOST=http://localhost:11434
- GPT Enterprise: configure as variáveis do seu ambiente corporativo e ajuste assistant.yaml.

## Notas
- Este repo não inclui o Makefile do DevLoop. Os alvos acima são específicos do assistant.
- Histórico do assistant foi preservado no split. Ajustes de docs/UX podem ser feitos por PRs aqui.

