"""Локальный тест mini_agent.py без платного API: фейковый OpenAI-совместимый сервер."""
import os, sys, threading, tempfile, json
sys.dont_write_bytecode = True  # не мусорить __pycache__ в хранилище Obsidian
from http.server import BaseHTTPRequestHandler, HTTPServer

SCRIPT = [  # что «модель» отвечает на каждом шаге
    {"tool_calls": [{"id": "1", "type": "function", "function": {"name": "bash", "arguments": json.dumps({"command": "ls"})}}]},
    {"tool_calls": [{"id": "2", "type": "function", "function": {"name": "write_file", "arguments": json.dumps({"path": "out/hello.txt", "content": "hi"})}}]},
    {"tool_calls": [{"id": "3", "type": "function", "function": {"name": "read_file", "arguments": json.dumps({"path": "out/hello.txt"})}}]},
    {"content": "Done: created out/hello.txt and verified its content."},
]
seen = []

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        seen.append(body)
        msg = {"role": "assistant", "content": None, **SCRIPT[len(seen) - 1]}
        out = json.dumps({"choices": [{"message": msg}]}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(out)
    def log_message(self, *a): pass

srv = HTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
os.environ.update(LLM_BASE_URL=f"http://127.0.0.1:{srv.server_port}/v1", LLM_API_KEY="x", LLM_MODEL="fake")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(tempfile.mkdtemp())
import mini_agent
result = mini_agent.agent("make hello file")
assert result.startswith("Done"), result
assert open("out/hello.txt").read() == "hi"
last = seen[-1]["messages"]
assert [m["role"] for m in last] == ["system", "user", "assistant", "tool", "assistant", "tool", "assistant", "tool"], [m["role"] for m in last]
assert last[-1]["content"] == "hi"
assert len(seen[0]["tools"]) == 3
print("OK:", result, "| requests:", len(seen))
