# Conversational Chatbot

## Overview
This project implements a **scripted, rule‑based chatbot** using only:
- HTML
- CSS
- JavaScript
- Python (standard library)

It demonstrates the basic flow of a conversational system:
`User input → JavaScript → Python logic → predefined response → JavaScript → UI`.

The chatbot does **not** use any AI, LLM, or external service – all answers are hard‑coded.

---

## Motivation
I was inspired by using ChatGPT and wanted to understand how a chatbot works under the hood. Building this simple, beginner‑friendly application lets me explain the whole pipeline during interviews.

---

## Features
- Clean modern UI (no external CSS/JS libraries)
- Responsive design for desktop, tablet, and mobile
- Predefined conversation categories (greetings, Python, HTML, CSS, JavaScript, chatbot basics, help, thanks, goodbye, fallback)
- Suggested question buttons that send a query automatically
- Clear chat button to restart the conversation
- Graceful handling of empty input and server‑unavailable errors

---

## Technologies Used
- **HTML5** – semantic structure
- **CSS3** – variables, flexbox, media queries, subtle animations
- **Vanilla JavaScript** – DOM manipulation, `fetch` API
- **Python 3** – `http.server` for a tiny HTTP server and chatbot logic (no third‑party packages)

---

## Project Structure
```
chatbot/
│
├─ index.html               # main page (header, chat area, input)
├─ css/
│   └─ style.css           # styling, responsive layout
├─ js/
│   └─ script.js           # UI interaction, request handling
├─ python/
│   └─ chatbot.py          # tiny HTTP server + rule‑based logic
├─ README.md                # this file
└─ .gitignore               # ignores caches, editor files, etc.
```

---

## How to Run
1. **Open a terminal** in the project root (`chatbot`).
2. Start the Python server:
   ```bash
   python -m python.chatbot
   ```
   (or `python python/chatbot.py` if `python -m` is not preferred)
   The server will listen on **http://localhost:5000**.
3. Open a web browser and navigate to the same address:
   `http://localhost:5000`
4. The welcome message appears automatically. Type a question, press **Enter** or click **Send**, and watch the bot respond.

---

## Testing the Conversation Flows
| Test | Input | Expected Bot Reply |
|------|-------|-------------------|
| 1 | `Hello` | Greeting response (`Hello! How can I help you?`) |
| 2 | `HELLO` | Same greeting (case‑insensitive) |
| 3 | `What is Python?` | Explanation of Python |
| 4 | `What is HTML?` | Explanation of HTML |
| 5 | `What is CSS?` | Explanation of CSS |
| 6 | `What is JavaScript?` | Explanation of JavaScript |
| 7 | `What is a chatbot?` | Short chatbot definition |
| 8 | `Thank you` | `You're welcome!` |
| 9 | `Bye` | Goodbye message |
|10 | `Random nonsense` | Fallback message |
|11 | (empty input) | No message is created |
|12 | Press **Enter** after typing – works |
|13 | Click **Clear Chat** – conversation resets to welcome message |
|14 | Resize the window – layout adapts for mobile |

---

## Future Improvements (optional)
- Expand the knowledge base with more patterns.
- Add simple context handling (e.g., follow‑up questions).
- Persist chat history to a file.
- Refine matching with regex or fuzzy search.

These are **future ideas only** – the current project stays strictly within the required stack.

---

## License
This project is released under the MIT License. Feel free to copy, modify, and share it.
