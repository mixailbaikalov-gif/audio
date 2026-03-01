# Audio -> Text transcription

Этот репозиторий теперь содержит CLI-скрипт `transcribe.py`, который расшифровывает аудиофайлы в текст (`.txt`) через OpenAI Audio Transcriptions API.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install openai
```

И задайте API-ключ:

```bash
export OPENAI_API_KEY="<ваш_ключ>"
```

## Использование

### 1) Один файл

```bash
python transcribe.py ./recording.mp3
```

Результат: рядом появится `recording.txt`.

### 2) Папка с аудио

```bash
python transcribe.py ./audio_folder
```

Скрипт найдёт все поддерживаемые аудио-файлы рекурсивно и создаст `.txt` для каждого.

### 3) Отдельная папка для результатов

```bash
python transcribe.py ./audio_folder --output-dir ./transcripts
```

### Дополнительные параметры

- `--model` — модель транскрибации (по умолчанию `gpt-4o-mini-transcribe`)
- `--language` — подсказка языка (`ru`, `en` и т.д.)
- `--prompt` — дополнительная инструкция для модели

## Поддерживаемые форматы

`mp3`, `wav`, `m4a`, `mp4`, `mpeg`, `mpga`, `webm`, `ogg`, `flac`

## Если `openai` не установлен

Теперь `python transcribe.py -h` работает даже без установленного пакета `openai` (чтобы можно было посмотреть помощь).

Но для самой расшифровки пакет обязателен. Если его нет, скрипт завершится с понятной ошибкой:

```text
Package 'openai' is not installed. Install it first: pip install openai
```
