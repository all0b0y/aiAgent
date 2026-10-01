"""mini_agent.py — минимальный, но настоящий агент (~120 строк, только stdlib).

Что здесь есть — ровно то же ядро, что у Claude Code / Codex / Hermes:
  1. системный промпт   2. инструменты (JSON-схемы)   3. цикл «модель → инструмент → результат → модель»
  4. лимит шагов        5. подтверждение опасных действий (human-in-the-loop)
  6. обрезка длинного вывода (бережём контекст)

Работает с любым OpenAI-совместимым API (OpenAI, OpenRouter, локальный llama.cpp / Ollama / LM Studio).
Запуск:
  export LLM_BASE_URL=https://openrouter.ai/api/v1   # или http://localhost:11434/v1
  export LLM_API_KEY=...                              # для локальной модели можно любое значение
  export LLM_MODEL=openai/gpt-5-mini                   # любая модель с поддержкой tools
  python3 mini_agent.py "Найди все TODO в этой папке и сведи их в TODO.md"
"""
import json, os, subprocess, sys, urllib.request
from pathlib import Path

BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
API_KEY = os.environ.get("LLM_API_KEY", "")
MODEL = os.environ.get("LLM_MODEL", "gpt-5-mini")
MAX_STEPS = 25            # предохранитель от бесконечного цикла
MAX_TOOL_OUTPUT = 8_000   # символов; длинный вывод режем — контекст не резиновый

SYSTEM = f"""You are a careful coding agent working in {os.getcwd()}.
Work in small verified steps: look before you change, run a check after you change.
Use tools instead of guessing file contents. When the task is done, reply with a short
report: what changed, how you verified it, what is left. Do not call tools after that."""

# ── 1. Инструменты: схема (что видит модель) + реализация (что делает код) ──────────
TOOLS = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read a UTF-8 text file. Use before editing or answering about a file.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Path relative to the working dir"}},
            "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Create or fully overwrite a text file. Read it first if it exists.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"]}}},
    {"type": "function", "function": {
        "name": "bash",
        "description": "Run a shell command (ls, grep, tests, git status). Returns stdout+stderr "
                       "and exit code. Avoid interactive commands.",
        "parameters": {"type": "object", "properties": {
            "command": {"type": "string"}}, "required": ["command"]}}},
]

DANGEROUS = ("rm ", "rm -", "git push", "git reset --hard", "sudo", "mkfs", "> /dev/")


def clip(text: str) -> str:
    if len(text) <= MAX_TOOL_OUTPUT:
        return text
    half = MAX_TOOL_OUTPUT // 2
    return text[:half] + f"\n…[обрезано {len(text) - MAX_TOOL_OUTPUT} символов]…\n" + text[-half:]


def run_tool(name: str, args: dict) -> str:
    """Ошибки возвращаем модели текстом — это её шанс исправиться, а не повод упасть."""
    try:
        if name == "read_file":
            return clip(Path(args["path"]).read_text(encoding="utf-8"))
        if name == "write_file":
            p = Path(args["path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"], encoding="utf-8")
            return f"OK: wrote {len(args['content'])} chars to {p}"
        if name == "bash":
            cmd = args["command"]
            if any(d in cmd for d in DANGEROUS):           # human-in-the-loop
                if input(f"\n⚠️  Агент хочет выполнить: {cmd}\nРазрешить? [y/N] ").lower() != "y":
                    return "DENIED by user. Choose a safer approach or ask the user."
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            return clip(f"exit={r.returncode}\n{r.stdout}{r.stderr}")
        return f"ERROR: unknown tool {name}"
    except Exception as e:  # noqa: BLE001 — любая ошибка превращается в наблюдение
        return f"ERROR: {type(e).__name__}: {e}"


# ── 2. Вызов модели ────────────────────────────────────────────────────────────────
def call_llm(messages: list) -> dict:
    body = json.dumps({"model": MODEL, "messages": messages, "tools": TOOLS}).encode()
    req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=body, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp)["choices"][0]["message"]


# ── 3. Агентный цикл — это и есть «агент» ───────────────────────────────────────────
def agent(task: str) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
    for step in range(1, MAX_STEPS + 1):
        msg = call_llm(messages)
        messages.append(msg)                          # ответ модели — часть истории
        calls = msg.get("tool_calls") or []
        if not calls:                                 # нет вызовов → модель считает, что закончила
            return msg.get("content") or ""
        for c in calls:
            name = c["function"]["name"]
            args = json.loads(c["function"]["arguments"] or "{}")
            print(f"[{step}] {name}({json.dumps(args, ensure_ascii=False)[:120]})")
            messages.append({"role": "tool", "tool_call_id": c["id"],
                             "content": run_tool(name, args)})
    return "Остановлено: исчерпан лимит шагов. Сузь задачу или подними MAX_STEPS."


if __name__ == "__main__":
    print(agent(" ".join(sys.argv[1:]) or "Опиши, что лежит в текущей папке."))
