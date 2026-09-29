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

## How to Run
1. **Open a terminal** in the project root directory (`Chatbot`).
2. Start the Python server:
   ```bash
   python python/chatbot.py
   ```
3. Navigate to **http://localhost:5000** in your browser.
4. Click suggestion pills or type questions across OOP, Python, Java, HTML, CSS, JavaScript, or SQL!

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
