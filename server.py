
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import urllib.request
import urllib.error
import uuid

BASE_DIR = Path(__file__).resolve().parent
MEMORIES_DIR = BASE_DIR / "memories"
MEMORIES_DIR.mkdir(exist_ok=True)

HOST = "127.0.0.1"
PORT = 8000
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5-coder:3b"


def generate_story(memory, style):
    prompts = {
        "Heartfelt letter": (
            "Write a warm, heartfelt letter based only on this memory. "
            "Do not invent personal facts."
        ),
        "Short story": (
            "Turn this memory into a gentle, engaging short story. "
            "Keep real details accurate and do not invent events."
        ),
        "Remembrance note": (
            "Write a respectful remembrance note using the supplied memory. "
            "Do not assume the person has died unless the user says so."
        ),
        "Spooky tale": (
            "Create a subtle, atmospheric spooky story inspired by the memory. "
            "Keep imagined details fictional and do not present supernatural "
            "events as real."
        ),
    }

    instruction = prompts.get(style, prompts["Heartfelt letter"])

    prompt = f"""
You are Ghostlight, a thoughtful personal memory-writing assistant.

{instruction}

Use natural language and preserve the meaning of the user's memory.
Do not claim to contact spirits or communicate with the dead.
Do not add names, dates, relationships, or events that were not supplied.

Memory:
{memory}

Write the finished piece with a suitable title.
"""

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result.get("response", "").strip()


def load_saved_memories():
    """Read saved memories and return the newest entries first."""
    records = []

    for file_path in MEMORIES_DIR.glob("*.json"):
        try:
            record = json.loads(file_path.read_text(encoding="utf-8"))

            # Ignore files that are not valid memory records.
            if not isinstance(record, dict):
                continue

            record.setdefault("id", file_path.stem)
            record.setdefault("title", "Untitled Memory")
            record.setdefault("memory", "")
            record.setdefault("story", "")
            record.setdefault("style", "Memory")

            record["_saved_at"] = file_path.stat().st_mtime
            records.append(record)

        except (json.JSONDecodeError, OSError):
            print(f"Could not read saved memory: {file_path.name}")

    records.sort(key=lambda item: item["_saved_at"], reverse=True)

    # Do not expose internal file paths or sorting metadata.
    for record in records:
        record.pop("_saved_at", None)

    return records


class GhostlightHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            file_path = BASE_DIR / "index.html"

            if not file_path.exists():
                self.send_error(404, "index.html not found")
                return

            body = file_path.read_bytes()
            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/health":
            try:
                payload = json.dumps({
                    "model": MODEL,
                    "prompt": "Reply with OK",
                    "stream": False
                }).encode("utf-8")

                request = urllib.request.Request(
                    OLLAMA_URL,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )

                with urllib.request.urlopen(request, timeout=30) as response:
                    response.read()

                self.send_json({
                    "available": True,
                    "model": MODEL,
                    "message": "Ghostlight and Ollama are connected."
                })

            except Exception:
                self.send_json({
                    "available": False,
                    "model": MODEL,
                    "message": (
                        "Start Ollama and check that the model is installed."
                    )
                }, 503)

        elif self.path == "/api/memories":
            try:
                memories = load_saved_memories()
                self.send_json({"memories": memories})

            except OSError as error:
                print("Could not load memories:", error)
                self.send_json({
                    "error": "Could not read the saved memories folder."
                }, 500)

        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        if self.path not in ("/api/create", "/api/save"):
            self.send_json({"error": "Endpoint not found."}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 20000:
                self.send_json({
                    "error": "Invalid request size."
                }, 400)
                return

            data = json.loads(
                self.rfile.read(length).decode("utf-8")
            )

            if not isinstance(data, dict):
                self.send_json({
                    "error": "Invalid request data."
                }, 400)
                return

            if self.path == "/api/create":
                memory = str(data.get("memory", "")).strip()
                style = str(data.get("style", "Heartfelt letter"))

                if len(memory) < 10:
                    self.send_json({
                        "error": (
                            "Please enter a little more detail about your memory."
                        )
                    }, 400)
                    return

                if len(memory) > 5000:
                    self.send_json({
                        "error": (
                            "Please keep your memory under 5,000 characters."
                        )
                    }, 400)
                    return

                allowed_styles = {
                    "Heartfelt letter",
                    "Short story",
                    "Remembrance note",
                    "Spooky tale"
                }

                if style not in allowed_styles:
                    style = "Heartfelt letter"

                story = generate_story(memory, style)

                if not story:
                    self.send_json({
                        "error": "The AI returned an empty story. Please try again."
                    }, 502)
                    return

                self.send_json({
                    "story": story,
                    "style": style
                })

            else:
                title = str(data.get("title", "")).strip()
                memory = str(data.get("memory", "")).strip()
                story = str(data.get("story", "")).strip()
                style = str(data.get("style", "")).strip()

                if not title or not memory or not story:
                    self.send_json({
                        "error": (
                            "A title, original memory, and story are required."
                        )
                    }, 400)
                    return

                if (
                    len(title) > 150
                    or len(memory) > 5000
                    or len(story) > 12000
                ):
                    self.send_json({
                        "error": "One or more fields are too long."
                    }, 400)
                    return

                record = {
                    "id": uuid.uuid4().hex,
                    "title": title,
                    "memory": memory,
                    "story": story,
                    "style": style
                }

                file_path = MEMORIES_DIR / f"{record['id']}.json"
                file_path.write_text(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                        indent=2
                    ),
                    encoding="utf-8"
                )

                self.send_json({
                    "message": "Memory saved on this computer.",
                    "id": record["id"]
                }, 201)

        except urllib.error.URLError:
            self.send_json({
                "error": "Cannot reach Ollama. Check that Ollama is running."
            }, 503)

        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json({
                "error": "Invalid JSON request."
            }, 400)

        except Exception as error:
            print("Request error:", error)
            self.send_json({
                "error": "Something went wrong. Check the server terminal."
            }, 500)

    def log_message(self, format, *args):
        print(f"[Ghostlight] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), GhostlightHandler)

    print("Ghostlight is running at http://127.0.0.1:8000")
    print(f"AI model: {MODEL}")
    print(f"Memory storage: {MEMORIES_DIR}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGhostlight stopped.")
    finally:
        server.server_close()
