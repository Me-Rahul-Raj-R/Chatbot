# Conversational Chatbot — Educational Assistant

## Overview
This project implements a **Rule-Based Conversational Chatbot & Educational Assistant** built using standard HTML5, CSS3, Vanilla JavaScript, and a lightweight Python backend (`http.server`). It is designed for students preparing for technical interviews across **OOP, Python, Java, HTML, CSS, JavaScript, SQL, and CS Fundamentals**.

The application pipeline follows a structured, deterministic flow:
`User Input → JS Async Fetch → Python Server → Normalization → Topic/Intent Matcher → Canonical Knowledge Base → Response UI`.

It operates **100% locally** without requiring any external AI API keys, LLM calls, or network dependencies.

---

## Key Architectural Highlights
- **No External AI / LLM Dependencies**: Runs purely using local, curated rule-based pattern matching and concept mapping in Python standard library (`http.server`, `re`, `difflib`).
- **Input Normalization**:
  1. **Case & Space Normalization**: Converts queries to lowercase, trims whitespace, and collapses repeated spaces.
  2. **Contraction & Phrase Expansion**: Expands contractions (*"what's"* $\rightarrow$ *"what is"*) and maps question variations (*"pillars of oop"*, *"tell me about python"*, *"python meaning"*) to canonical concepts.
  3. **Typo Correction**: Safely corrects common technical typos (*"pyhton"*, *"javasript"*, *"htlm"*, *"jvaa"*, *"databse"*, *"oops"*).
  4. **Punctuation Stripping**: Cleans punctuation while preserving the original user message for display history.
- **Language & Concept Distinction**: Strictly distinguishes between distinct languages/domains (e.g., **Java $\neq$ JavaScript**, **HTML $\neq$ CSS**, **Python $\neq$ Java**).
- **Session Context Tracking**: Lightweight in-memory session tracking for resolving follow-up questions (*"advantages?"*, *"example?"*, *"code?"*).
- **Modern Responsive UI**:
  - Rendered `<code>` blocks and bold formatting.
  - Interactive suggestion buttons for quick topic testing.
  - Asynchronous typing indicator (*"Thinking..."*).
  - Clear Chat button that resets UI chat history and wipes server session context.

---

## Supported Knowledge Domains
1. **Object-Oriented Programming (OOP)**: Definition, Procedural vs OOP, Class vs Object, Attributes vs Methods, **4 Pillars of OOP** (Encapsulation, Abstraction, Inheritance, Polymorphism), Data Hiding, Method Overloading vs Overriding, Single/Multilevel/Multiple/Hierarchical/Hybrid Inheritance, Interface vs Abstract Class, Association/Aggregation/Composition, IS-A vs HAS-A.
2. **Python Domain**: Features, interpreted execution model, indentation, dynamic typing, mutability, Data Types (`int`, `float`, `str`, `bool`, `list`, `tuple`, `set`, `dict`, `None`), List/Dict Comprehensions, `*args` and `**kwargs`, `lambda`, exception handling (`try`/`except`/`else`/`finally`), `is` vs `==`.
3. **Java Domain (Core Java)**: Java definition, Platform Independence, **JDK vs JRE vs JVM**, Bytecode, Access Modifiers (`public`, `private`, `protected`, default), `String` vs `StringBuilder` vs `StringBuffer`, Checked vs Unchecked Exceptions, Java Collections (`List`, `Set`, `Map`, `ArrayList`, `LinkedList`, `HashMap`), Garbage Collection.
4. **HTML Domain**: Structure (`<!DOCTYPE>`, `html`, `head`, `body`), Tags vs Elements vs Attributes, Semantic HTML (`header`, `nav`, `main`, `article`, `section`, `footer`), `div` vs `span`, Block vs Inline elements, HTML5 features, Forms, Tables.
5. **CSS Domain**: Syntax, Selectors (Element, Class, ID, Universal, Pseudo-classes, Pseudo-elements), Inline vs Internal vs External, **Box Model** (Content, Padding, Border, Margin), `display` modes, Flexbox vs Grid, Positioning (`static`, `relative`, `absolute`, `fixed`, `sticky`), `z-index`, Responsive Design & Media Queries.
6. **JavaScript Domain**: `var` vs `let` vs `const`, Primitive vs Object Data Types, `==` vs `===` (Loose vs Strict Equality), Hoisting, Closures, DOM vs BOM, Promises, `async`/`await`, Array methods (`map`, `filter`, `reduce`).
7. **Cross-Language Comparisons**: Java vs JavaScript, Python vs Java, HTML vs CSS, Class vs Object, Encapsulation vs Abstraction, List vs Tuple.

---

## Technologies Used
- **HTML5** – Semantic document layout & input controls.
- **CSS3** – CSS variables, flexbox, responsive design, code formatting.
- **Vanilla JavaScript** – Async `fetch` API, DOM manipulation, session context tracking, typing indicators.
- **Python 3 (Standard Library)** – `http.server`, `socketserver`, `json`, `re`, `difflib`. Zero mandatory third-party framework dependencies.

---

## Project Structure
```
chatbot/
│
├─ index.html               # Main interface & suggestion pills
├─ css/
│   └─ style.css           # Chat styling, responsive layout & code syntax formatting
├─ js/
│   └─ script.js           # Frontend logic, async fetch, typing indicator, clear chat reset
├─ python/
│   ├─ chatbot.py          # Pure rule-based HTTP server & POST /chat endpoint
│   └─ knowledge_base.py   # Normalization engine, alias mapping & canonical knowledge base
├─ README.md                # Project documentation
└─ .gitignore               # Excludes virtual environments and temporary logs
```

---

## Development Journey & Step-by-Step Process Done
To meet the goal of expanding conversational chatbot knowledge and answering ability without relying on external AI APIs, the following steps were taken:
1. **Architecture Migration**: Transitioned from a hybrid architecture (local + Gemini API fallback) to a fully deterministic, purely rule-based engine in `knowledge_base.py`. This ensures high reliability, instant responses, and no 503 unavailability issues.
2. **Knowledge Base Expansion**: Incorporated comprehensive technical interview-prep content for OOP, Java, JavaScript, HTML, CSS, and Python.
3. **Concept Resolution Process**:
   - **Step 1: Input Normalization**: Raw user input is sanitized using regex. It converts queries to lowercase, removes punctuation, and collapses whitespace.
   - **Step 2: Typo Correction**: Matches common technical typos (e.g., "pyhton", "javasript") to their correct forms using a `TYPO_MAP`.
   - **Step 3: Alias Mapping**: Uses `ALIAS_RULES` to map varied user phrasing (e.g., "pillars of oop", "python meaning") to a canonical concept key.
   - **Step 4: Answer Retrieval & Fallback**: Exact matches are pulled from `CANONICAL_ANSWERS`. If no exact match is found, fuzzy matching is applied. A deterministic fallback response is provided if no match succeeds.
4. **Session Tracking**: Built an in-memory `SESSION_CONTEXT` dictionary keyed by `sessionId` in `chatbot.py` to correctly resolve follow-up pronouns (e.g., "why is it popular").
5. **Testing & Verification**: Created a robust `test_suite.py` with 29 test cases covering concept routing, typo correction, and language distinction, ensuring 100% accuracy.

---

## How to Run
1. **Prerequisites**: Ensure Python 3.x is installed on your system. No external packages are required!
2. **Open a terminal** (Command Prompt or PowerShell) in the project root directory (`Chatbot`).
3. Start the built-in Python HTTP server by running:
   ```bash
   python -m python.chatbot
   ```
4. Once the server starts, you will see a message indicating it is running on port 5000.
5. Open your preferred web browser and navigate to **http://localhost:5000**.
6. The Chatbot UI will load. You can start typing questions about OOP, Python, Java, HTML, CSS, or JavaScript, or use the quick suggestion pills provided on the screen!
7. To reset the conversation and clear session context, use the **Clear Chat** button in the UI.

---

## Test Verification Summary
Run the local test suite:
```bash
python scratch/test_suite.py
```
**Results**: 29 / 29 Tests Passed (100% Success).

---

## License
This project is released under the MIT License.
