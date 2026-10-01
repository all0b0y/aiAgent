#!/usr/bin/env python3
"""PreToolUse-хук для Claude Code: блокирует опасные shell-команды и доступ к секретам.

Подключение (.claude/settings.json):
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash|Read|Edit|Write",
       "hooks": [{"type": "command",
                  "command": "python3 \\"${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.py\\""}]}
    ]
  }
}

Протокол: JSON события приходит в stdin. Выход с кодом 2 = заблокировать,
текст из stderr увидит модель как причину (и сможет выбрать безопасный путь).
Код 0 = решения нет, работает обычная проверка прав.
"""
import json, re, sys

BLOCK_COMMANDS = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r", "rm -rf запрещён: удаляй конкретные файлы или попроси человека"),
    (r"git\s+push\s+.*(--force|-f\b)", "force-push запрещён: создай новую ветку или попроси человека"),
    (r"git\s+reset\s+--hard", "git reset --hard запрещён: используй git stash или новую ветку"),
    (r"--no-verify", "обход pre-commit проверок запрещён: исправь причину падения"),
    (r"\bsudo\b", "sudo запрещён в агентной сессии"),
    (r"curl[^|]*\|\s*(ba)?sh", "запуск скрипта из интернета через pipe запрещён"),
]
SECRET_PATHS = re.compile(r"(^|/)(\.env(\.[\w-]+)?|id_rsa|id_ed25519|\.ssh/|\.aws/credentials|\.npmrc)$")


def main() -> int:
    event = json.load(sys.stdin)
    tool, inp = event.get("tool_name", ""), event.get("tool_input", {}) or {}
    if tool == "Bash":
        cmd = inp.get("command", "")
        for pattern, reason in BLOCK_COMMANDS:
            if re.search(pattern, cmd):
                print(f"BLOCKED by guard.py: {reason}", file=sys.stderr)
                return 2
    path = inp.get("file_path") or inp.get("path") or ""
    if path and SECRET_PATHS.search(path) and not path.endswith(".example"):
        print(f"BLOCKED by guard.py: {path} может содержать секреты. Используй .env.example "
              "или попроси пользователя.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
