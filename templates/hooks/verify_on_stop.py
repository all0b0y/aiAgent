#!/usr/bin/env python3
"""Stop-хук: не даёт агенту закончить ход, пока проверки проекта красные.

Подключение (.claude/settings.json):
{"hooks": {"Stop": [{"hooks": [{"type": "command",
   "command": "python3 \\"${CLAUDE_PROJECT_DIR}/.claude/hooks/verify_on_stop.py\\""}]}]}}

Поменяй CHECK под свой проект (pnpm check, pytest -q, cargo test…).
Выход 2 = «не останавливайся», stderr уходит модели как задание.
stop_hook_active=true значит, что мы уже продлевали ход: не зацикливаемся бесконечно.
"""
import json, os, subprocess, sys

CHECK = os.environ.get("AGENT_VERIFY_CMD", "pnpm -s check")


def main() -> int:
    event = json.load(sys.stdin)
    if event.get("stop_hook_active"):
        return 0  # уже давали второй шанс — отпускаем, решает человек
    r = subprocess.run(CHECK, shell=True, capture_output=True, text=True,
                       cwd=event.get("cwd") or None, timeout=600)
    if r.returncode == 0:
        return 0
    tail = (r.stdout + r.stderr)[-3000:]
    print(f"Проверка `{CHECK}` не прошла (exit {r.returncode}). Исправь до завершения "
          f"или честно объясни, почему не можешь.\n{tail}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
