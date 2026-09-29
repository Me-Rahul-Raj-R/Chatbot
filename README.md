# Conversational Chatbot — Educational Assistant

## Overview
This project implements a **Conversational Chatbot & Educational Assistant** built with a **Hybrid Answering Architecture**. It features a fast, comprehensive local Python knowledge base coupled with an optional **Google Gemini AI fallback** for complex queries, rendered through a responsive HTML5/CSS3/Vanilla JavaScript frontend interface.

The application pipeline follows a structured flow:
`User input → JS Async Request → Python Server → Internal Normalization → Topic/Intent Classifier → Local Knowledge Base → (Optional Gemini Fallback) → Rendered UI`.

---

## Key Features & Improvements
- **Hybrid Answering Architecture**:
  1. **Input Normalization**: Converts input to lowercase, strips trailing/leading whitespace, expands contractions ("what's" → "what is"), fixes technical typos ("pyhton" → "python", "javasript" → "javascript", "htmll" → "html", "databse" → "database"), and removes unnecessary punctuation.
  2. **Topic & Intent Recognition**: Recognizes single keywords ("python", "html", "sql", "process"), phrase variations ("tell me about python", "can you explain python", "python meaning"), and intents (definitions, comparisons, code examples, debugging, why/how questions).
  3. **Multi-Domain Local Knowledge Base**: Predefined, accurate educational answers covering 12 technical domains without requiring external API calls for core concepts.
  4. **Session Context & Follow-Up Handling**: Maintains bounded conversation context per session to resolve pronouns ("it", "this", "can you give an example?").
  5. **Optional Gemini AI Fallback**: If `GEMINI_API_KEY` is set in the server environment and local knowledge is insufficient, queries Gemini API with strict educational system instructions.
  6. **Friendly Graceful Fallback**: Returns a polite, varied fallback response listing supported topics if offline or unconfigured.
- **Modern UI & UX**:
  - Code syntax formatting (`<code>` blocks) and bold text rendering.
  - Interactive suggested topic pills across Python, HTML, CSS, JavaScript, SQL, Algorithms, and Networking.
  - Asynchronous typing indicator ("Thinking...") during backend processing.
  - Input field Enter key submission and duplicate submission prevention.
  - Clear Chat button that resets frontend chat history and wipes backend session context.
  - Strict security: `GEMINI_API_KEY` is kept strictly server-side and never exposed to client HTML/JS or logs.

---

## Supported Knowledge Domains
1. **General Programming Fundamentals**: Algorithms, pseudocode, variables, constants, data types, operators, expressions, functions, parameters vs arguments, control flow, loops, recursion, debugging, syntax vs runtime vs logical errors, compilers vs interpreters.
2. **Python Domain**: Syntax, features, data types (`int`, `float`, `str`, `bool`, `list`, `tuple`, `set`, `dict`, `None`), casting, functions, `lambda`, modules, packages, exception handling (`try`/`except`/`finally`), OOP (`class`, `object`, `__init__`, `self`, inheritance, encapsulation, polymorphism, abstraction), list slicing, comprehensions, dictionary iteration.
3. **HTML Domain**: Document structure, tags, elements, attributes (`href`, `src`, `alt`, `id`, `class`), headings, paragraphs, links, images, forms, tables, lists, block vs inline (`div` vs `span`), semantic HTML (`header`, `nav`, `main`, `section`, `article`, `footer`).
4. **CSS Domain**: Selectors (element, class, ID, universal `*`), colors, background, fonts, box model (content, padding, border, margin), display modes (`block`, `inline`, `inline-block`, `flex`, `grid`), positioning, responsive design & media queries, hover transitions.
5. **JavaScript Domain**: Variables (`let` vs `const` vs `var`), arrow functions, arrays, objects, DOM manipulation (`getElementById`, `querySelector`), events & event listeners, JSON, `localStorage`, `sessionStorage`, `fetch()` API.
6. **SQL & Database Concepts**: SQL commands (`SELECT`, `FROM`, `WHERE`, `ORDER BY`, `GROUP BY`, `HAVING`, `LIMIT`, `INSERT`, `UPDATE`, `DELETE`), keys (primary, foreign, unique, candidate, composite), JOINs (`INNER`, `LEFT`, `RIGHT`, `FULL`), aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`), normalization (1NF, 2NF, 3NF), data integrity.
7. **Data Structures & Algorithms**: Arrays, linked lists, stacks (LIFO), queues (FIFO), trees, graphs, hash tables, searching (linear vs binary), sorting (bubble, selection, insertion), Big O notation, time vs space complexity.
8. **Computer Science Fundamentals & OS**: Operating system roles, processes vs threads, multitasking, multiprocessing, CPU scheduling, memory management, virtual memory, RAM vs ROM, cache, deadlocks, concurrency, synchronization.
9. **Computer Networking**: LAN, WAN, MAN, PAN, IP addresses (IPv4 vs IPv6), MAC address, routers, switches, modems, DNS, HTTP vs HTTPS, TCP vs UDP, ports, client-server model, REST APIs.
10. **Git & GitHub**: Distributed version control, repository, commit, branch, merge, clone, pull, push, pull request, `.gitignore`, `README.md`.
11. **Chatbot Architecture & Project Self-Awareness**: Rule-based vs AI chatbot, architecture explanation, project technology stack, internal normalization pipeline.
12. **General Educational Topics**: Percentages, averages, ratios, basic probability, statistics, and logical reasoning.

---

## Technologies Used
- **HTML5** – Semantic document layout & input controls.
- **CSS3** – CSS variables, flexbox, responsive design, pill buttons, code block styling.
- **Vanilla JavaScript** – Async `fetch` API, DOM manipulation, session context tracking, typing indicators.
- **Python 3 (Standard Library)** – `http.server`, `socketserver`, `json`, `re`, `urllib.request`, `difflib`. No mandatory third-party package dependencies required.

---

## Project Structure
```
chatbot/
│
├─ index.html               # Main page layout & suggestion pills
├─ css/
│   └─ style.css           # Modern chatbot styling, responsive design & code formatting
├─ js/
│   └─ script.js           # Frontend logic, async fetch, typing indicator, clear chat reset
├─ python/
│   ├─ chatbot.py          # HTTP server, POST /chat endpoint, Gemini API fallback
│   └─ knowledge_base.py   # Normalization engine, topic/intent mapping & local KB
├─ README.md                # Project documentation
└─ .gitignore               # Ignores caches, secrets, and environment files
```

---

## How to Run
1. **Open a terminal** in the project root directory (`Chatbot`).
2. Start the Python backend server:
   ```bash
   python python/chatbot.py
   ```
   (Optional: Set `GEMINI_API_KEY` in environment if you wish to enable the Gemini fallback for out-of-scope questions):
   - PowerShell: `$env:GEMINI_API_KEY="your_api_key"; python python/chatbot.py`
   - Linux/macOS: `GEMINI_API_KEY="your_api_key" python python/chatbot.py`
3. The server will launch at **http://localhost:5000**.
4. Open a web browser and navigate to `http://localhost:5000`.
5. Select suggestion buttons or type any question across Python, Web Dev, SQL, CS, or Networking!

---

## Testing Verification Matrix
| Test Case | Input Query | Recognized Intent / Topic | Verified Bot Response |
|-----------|-------------|---------------------------|-----------------------|
| 1 | `Hello` | Greeting | Friendly educational greeting |
| 2 | `WHAT IS PYTHON?` | Case Normalization / Python | High-level Python definition |
| 3 | `pyhton` | Typo Correction / Python | Matches Python definition |
| 4 | `tell me about python` | Phrase Variation / Python | Matches Python definition |
| 5 | `explain list comprehension` | Python Lists | Explains syntax with code example |
| 6 | `explain oop` | OOP Concepts | Explains 4 pillars of Object-Oriented Programming |
| 7 | `difference between let and var` | JavaScript Scope | Explains block vs function scoping |
| 8 | `what is a primary key` | SQL Database | Explains unique identification in tables |
| 9 | `what is dns` | Computer Networking | Explains domain name resolution |
| 10 | `how does this chatbot work` | Project Architecture | Explains 5-step hybrid answering pipeline |
| 11 | `python vs java` | Language Comparison | Compares typing, execution, and main use cases |
| 12 | (Click Clear Chat) | Frontend / Backend Reset | Clears history window and resets backend session |

---

## License
This project is released under the MIT License.
