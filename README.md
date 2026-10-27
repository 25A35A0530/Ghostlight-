# 👻 Ghostlight — Memories That Stay

**Ghostlight** is a local AI-powered memory-writing app that transforms personal memories into meaningful written pieces. Enter a memory, choose a writing style, and let a locally running AI help you preserve it.

The project uses **Ollama** to generate text locally, allowing your memories to stay on your own computer instead of being sent to a cloud AI API.

## ✨ Features

- 📝 Transform personal memories into AI-assisted writing.
- 🎭 Choose from four writing styles:
  - Heartfelt Letter
  - Short Story
  - Remembrance Note
  - Spooky Tale
- 💾 Save generated memories with a custom title.
- 📚 Browse saved memories in your personal library.
- 🔍 Read the original memory alongside the generated writing.
- 📋 Copy generated text to use elsewhere.
- 🔒 Local-first design using Ollama on your computer.

## 🧰 Tech Stack

- **Python** — Local server and API endpoints
- **HTML, CSS, JavaScript** — User interface
- **Ollama** — Local AI model runtime
- **Qwen2.5-Coder 3B** — Configured language model
- **JSON** — Local storage for saved memories

## 📁 Project Structure

```text
Ghostlight/
├── server.py
├── index.html
└── memories/
    └── saved memory JSON files
```

The `memories/` folder stores saved entries and may be empty before you save your first memory.

## ✅ Requirements

- Python installed on your computer
- Ollama installed and running
- The `qwen2.5-coder:3b` model

## 🚀 Setup and Run

### Step 1: Install Ollama

Download and install Ollama from:

https://ollama.com/

### Step 2: Download the AI Model

Open Command Prompt or a terminal and run:

```bash
ollama pull qwen2.5-coder:3b
```

Ensure Ollama is running before using Ghostlight.

### Step 3: Open the Project Folder

On Windows, open Command Prompt and run:

```bat
cd /d "C:\Users\Spandana\OneDrive\Desktop\Ghostlight"
```

If your project is saved elsewhere, replace the path with your actual project location.

### Step 4: Start the Server

Run:

```bash
python server.py
```

### Step 5: Open the Application

Open your browser and visit:

http://127.0.0.1:8000

Keep the terminal running while you use the application. Press `Ctrl+C` in the terminal to stop the server.

## 🕯️ How to Use

1. Open Ghostlight in your browser.
2. Enter a personal memory in the text area.
3. Select a writing style.
4. Generate the writing.
5. Review the generated result and enter a title.
6. Save the memory to your library.
7. Open saved entries to view the original memory and generated writing.

## 📝 Example Memory

"When I was in school, my best friend and I used to share our lunch every day. We laughed about silly things, helped each other with homework, and walked home together after school. Even though life gets busy now, I still smile whenever I remember those simple and happy days."

**Example Title:** The Little Things We Shared

## 💾 Where Are Memories Saved?

Saved entries are stored as JSON files inside the project's `memories/` directory.

Keep a backup of this folder if you want to preserve your saved entries when moving or copying the project.

## 🔐 Privacy Notes

Ghostlight is designed for local use and sends generation requests to the Ollama service running on your computer. The configured workflow does not require a cloud AI API.

- Avoid entering highly sensitive information unless you are comfortable storing it on your computer.
- Saved memories are stored as local files and may be readable by anyone who has access to those files.
- AI-generated writing may contain inaccurate details. Review the result before saving or sharing it.
- This project has not been independently security-audited.

## 🛠️ Troubleshooting

### The Page Does Not Open

- Check that `python server.py` is still running.
- Confirm the browser address is `http://127.0.0.1:8000`.
- Check the terminal for Python errors.

### Ollama or Model Error

Run:

```bash
ollama list
```

Confirm that `qwen2.5-coder:3b` appears in the list and that Ollama is running.

If necessary, download the model again:

```bash
ollama pull qwen2.5-coder:3b
```

### Saved Memories Will Not Load

- Stop the server using `Ctrl+C`.
- Restart it using `python server.py`.
- Refresh the browser using `Ctrl+F5`.
- If your current version supports the saved memories API, visit `http://127.0.0.1:8000/api/memories` and check whether it returns JSON.
- If it displays an HTML page instead, check that `server.py` contains the `/api/memories` route.

## 🌱 Project Goal

Ghostlight explores how local AI can help people preserve personal experiences through writing while keeping the process simple, personal, and accessible.

## 📌 Project Status

Ghostlight is a local prototype. Available features depend on the versions of `server.py` and `index.html` in the project folder.

Test memory generation, saving, and library loading in your local setup.

## 📄 License

No license has been specified yet. Add a license file if you plan to publish the project for reuse by others.
