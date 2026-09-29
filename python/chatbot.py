import http.server
import socketserver
import json
import os
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse

# ----- Chatbot logic -----

# Define keyword groups, knowledge base, and intent handling
import difflib

# ---------- Knowledge Base ----------
# Structured as {topic: {intent: answer}}
KB = {
    "general_programming": {
        "definition": {
            "what is programming": "Programming is the process of creating a set of instructions that tell a computer how to perform a task.",
            "what is a programming language": "A programming language is a formal language comprising a set of instructions that produce various kinds of output."
        },
        "concepts": {
            "what is a variable": "A variable stores a value that can be changed during program execution.",
            "what is a function": "A function is a reusable block of code that performs a specific task and can be called multiple times.",
            "what is a loop": "A loop repeats a block of code while a condition is true or for a set number of iterations.",
            "what is recursion": "Recursion is a function calling itself to solve smaller instances of a problem."
        }
    },
    "python": {
        "definition": {
            "what is python": "Python is a high‑level, interpreted programming language known for its readable syntax and versatility.",
            "why is python popular": "Python is popular because it has simple syntax, a massive ecosystem of libraries, and strong community support."
        },
        "concepts": {
            "what is a python variable": "In Python, a variable is created by assigning a value to a name, e.g., `x = 5`.",
            "what is a list": "A list is an ordered, mutable collection of items, defined with square brackets, e.g., `[1, 2, 3]`.",
            "what is a tuple": "A tuple is an ordered, immutable collection, defined with parentheses, e.g., `(1, 2, 3)`.",
            "what is a dictionary": "A dictionary stores key‑value pairs, defined with curly braces, e.g., `{'a': 1, 'b': 2}`.",
            "what is a for loop": "A `for` loop iterates over items of a sequence, e.g., `for x in range(5): print(x)`.",
            "what is a while loop": "A `while` loop repeats as long as a condition is true, e.g., `while i < 5: i += 1`.",
            "what is lambda": "A lambda creates an anonymous function, e.g., `lambda x: x * 2`.",
            "what is a module": "A module is a file containing Python definitions and statements that can be imported.",
            "what is a package": "A package is a directory of Python modules with an `__init__.py` file.",
            "what is exception handling": "Exception handling uses `try`, `except`, and optionally `finally` to manage errors gracefully."
        }
    },
    "html": {
        "definition": {
            "what is html": "HTML (HyperText Markup Language) is the standard language for creating web pages.",
            "what does html stand for": "HTML stands for HyperText Markup Language."
        },
        "elements": {
            "what is an html tag": "An HTML tag defines the start and end of an element, e.g., `<p>` and `</p>`.",
            "what is a heading": "Headings are defined with `<h1>` to `<h6>` tags to structure page hierarchy."
        }
    },
    "css": {
        "definition": {
            "what is css": "CSS (Cascading Style Sheets) describes how HTML elements are displayed on screen.",
            "what does css stand for": "CSS stands for Cascading Style Sheets."
        },
        "layout": {
            "what is flexbox": "Flexbox is a CSS layout model that arranges items along a single axis, providing flexible alignment.",
            "what is css grid": "CSS Grid is a two‑dimensional layout system that lets you position items in rows and columns."
        }
    },
    "javascript": {
        "definition": {
            "what is javascript": "JavaScript is a scripting language that enables interactive web pages."
        },
        "basics": {
            "what is a variable in javascript": "Variables can be declared using `var`, `let`, or `const`.",
            "difference between let and var": "`let` is block‑scoped, while `var` is function‑scoped."
        }
    },
    "sql": {
        "definition": {
            "what is sql": "SQL (Structured Query Language) is used to manage and query relational databases."
        },
        "commands": {
            "what is select": "`SELECT` retrieves data from one or more tables.",
            "what is where": "`WHERE` filters rows based on a condition.",
            "what is join": "`JOIN` combines rows from two or more tables based on a related column."
        }
    },
    "c": {
        "definition": {
            "what is c": "C is a general-purpose, procedural programming language developed in the 1970s, known for its efficiency and close-to-hardware capabilities."
        },
        "concepts": {
            "what is a c variable": "In C, a variable must be declared with a type before use, e.g., `int x = 5;`.",
            "what is a c loop": "C supports `for`, `while`, and `do-while` loops for iteration. Example: `for(int i=0; i<10; i++) { /*...*/ }`."
        }
    },
    "regex": {
        "definition": {
            "what is regex": "Regex (regular expression) is a pattern describing a set of strings, used for matching and manipulating text."
        },
        "examples": {
            "regex example": "A simple regex to match an email: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}`."
        }
    }
}

# ---------- Intent & Topic Mapping ----------
INTENT_KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"],
    "introduction": ["who are you", "what are you", "introduce yourself"],
    "definition": ["what is", "define", "explain"],
    "explanation": ["explain", "describe", "tell me about"],
    "example": ["example", "sample", "show me"],
    "comparison": ["vs", "difference between", "compare"],
    "why": ["why", "reason"],
    "how": ["how", "steps to"],
    "thanks": ["thank", "thanks"],
    "goodbye": ["bye", "goodbye", "see you"]
}

TOPIC_ALIASES = {
    "programming": ["programming", "program", "code", "coding"],
    "python": ["python", "py"],
    "html": ["html", "hypertext markup language"],
    "css": ["css", "cascading style sheets"],
    "javascript": ["javascript", "js"],
    "c": ["c", "c programming", "c language"]
    "sql": ["sql", "database", "dbms", "rdbms"]
}

# ---------- Normalization Helper ----------
def normalize(text: str) -> str:
    """Lower‑case, trim, collapse spaces, remove punctuation (except spaces)."""
    text = text.lower().strip()
    # Replace punctuation with space
    text = re.sub(r"[\.!?,'\";:()\[\]{}]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text

def detect_intent(norm: str) -> str:
    """Return the first matching intent based on keyword lists."""
    for intent, words in INTENT_KEYWORDS.items():
        for w in words:
            if w in norm:
                return intent
    return "unknown"

def detect_topic(norm: str) -> str:
    """Return the most probable topic based on aliases."""
    for topic, alist in TOPIC_ALIASES.items():
        for a in alist:
            if a in norm:
                return topic
    return "general_programming"

def retrieve_answer(topic: str, intent: str, norm: str) -> str | None:
    """Lookup answer from KB using topic, intent and fuzzy matching.
    Returns None if no suitable answer is found.
    """
    # Direct lookup
    if topic in KB and intent in KB[topic]:
        for key_phrase, answer in KB[topic][intent].items():
            if key_phrase in norm:
                return answer
    # Fallback to definition intent if specific not found
    if topic in KB and "definition" in KB[topic]:
        for key_phrase, answer in KB[topic]["definition"].items():
            if key_phrase in norm:
                return answer
    # Simple fuzzy match using difflib for near matches (typos)
    if topic in KB:
        for intent_group in KB[topic].values():
            for key_phrase, answer in intent_group.items():
                if difflib.SequenceMatcher(None, key_phrase, norm).ratio() > 0.85:
                    return answer
    return None

# ----- Chatbot logic (updated) -----
RESPONSES = [
    (['hello', 'hi', 'hey', 'good morning', 'good evening'], "Hello! How can I help you?"),
    (['who are you', 'what are you', 'introduce yourself'], "I am a simple scripted chatbot designed to interact with users through predefined conversation flows."),
    (['what is python', 'tell me about python', 'python'], "Python is a high‑level programming language known for its simple and readable syntax."),
    (['what is html', 'tell me about html', 'html'], "HTML is used to structure the content of web pages."),
    (['what is css', 'tell me about css', 'css'], "CSS is used to style and design web pages."),
    (['what is javascript', 'tell me about javascript', 'javascript'], "JavaScript is used to add interaction and dynamic behavior to web pages."),
    (['what is a chatbot', 'how does a chatbot work', 'chatbot'], "A scripted chatbot receives user input, checks it against predefined conversation logic, and returns an appropriate predefined response."),
    (['help', 'what can you do', 'what can i ask'], "You can ask me about Python, HTML, CSS, JavaScript, or basic chatbot concepts."),
    (['thank you', 'thanks', 'thank you so much'], "You're welcome!"),
    (['bye', 'goodbye', 'see you'], "Goodbye! Have a great day!")
]

FALLBACK = "I'm not able to answer that question right now because my AI response service is unavailable. You can try asking about Python, HTML, CSS, JavaScript, SQL, or programming concepts."

def process_message(message: str) -> str:
    """Hybrid answer workflow: normalize → detect topic/intent → local KB → Gemini fallback → friendly fallback."""
    norm = normalize(message)
    # 1️⃣ Try predefined simple responses (exact keyword groups)
    for keywords, reply in RESPONSES:
        for kw in keywords:
            if kw in norm:
                return reply
    # 2️⃣ Identify topic and intent
    topic = detect_topic(norm)
    intent = detect_intent(norm)
    # 3️⃣ Lookup in extended knowledge base
    answer = retrieve_answer(topic, intent, norm)
    if answer:
        return answer
    # 4️⃣ Gemini fallback if API key present
    if GEMINI_API_KEY:
        try:
            gemini_reply = get_gemini_reply(message)
            if gemini_reply:
                return gemini_reply
        except Exception as e:
            print('Gemini error:', e)
    # 5️⃣ Friendly fallback
    return FALLBACK

RESPONSES = [
    (['hello', 'hi', 'hey', 'good morning', 'good evening'], "Hello! How can I help you?"),
    (['who are you', 'what are you', 'introduce yourself'], "I am a simple scripted chatbot designed to interact with users through predefined conversation flows."),
    (['what is python', 'tell me about python', 'python'], "Python is a high-level programming language known for its simple and readable syntax."),
    (['what is html', 'tell me about html', 'html'], "HTML is used to structure the content of web pages."),
    (['what is css', 'tell me about css', 'css'], "CSS is used to style and design web pages."),
    (['what is javascript', 'tell me about javascript', 'javascript'], "JavaScript is used to add interaction and dynamic behavior to web pages."),
    (['what is a chatbot', 'how does a chatbot work', 'chatbot'], "A scripted chatbot receives user input, checks it against predefined conversation logic, and returns an appropriate predefined response."),
    (['help', 'what can you do', 'what can i ask'], "You can ask me about Python, HTML, CSS, JavaScript, or basic chatbot concepts."),
    (['thank you', 'thanks', 'thank you so much'], "You're welcome!"),
    (['bye', 'goodbye', 'see you'], "Goodbye! Have a great day!"),
]

FALLBACK = "I'm sorry, I don't have a predefined response for that query yet. Try asking me about Python, HTML, CSS, JavaScript, or chatbot concepts."

# Gemini configuration (read from environment, never exposed to frontend)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-pro'
GEMINI_ENDPOINT = f'https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent'

def normalize(text: str) -> str:
    """Lower‑case, trim, remove punctuation (except spaces)."""
    text = text.lower().strip()
    # Replace punctuation with spaces, then collapse multiple spaces
    text = re.sub(r"[\.!?,'\";:()\[\]{}]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def process_message(message: str) -> str:
    """Return a response for *message*.
    First try predefined keyword matches; if none, fall back to Gemini (if API key is set).
    """
    norm = normalize(message)
    # 1️⃣ Check predefined responses
    for keywords, reply in RESPONSES:
        for kw in keywords:
            if kw in norm:
                return reply
    # 2️⃣ No predefined match – try Gemini if the key is available
    if GEMINI_API_KEY:
        try:
            gemini_reply = get_gemini_reply(message)
            if gemini_reply:
                return gemini_reply
        except Exception as e:
            # Log server‑side, but do not expose details to the user
            print('Gemini error:', e)
    # 3️⃣ Either key missing or Gemini failed – friendly fallback
    return "I'm not able to answer that question right now because my AI response service is unavailable. You can try asking about Python, HTML, CSS, JavaScript, SQL, programming, or chatbot concepts."


# ----- HTTP server -----

class ChatHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files and handle POST /chat requests."""

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != '/chat':
            self.send_error(404, "Not Found")
            return
        # Read JSON payload
        content_length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(content_length)
        try:
            data = json.loads(raw.decode('utf-8'))
            user_msg = data.get('message', '')
            reply = process_message(user_msg)
            response = {'reply': reply}
            resp_bytes = json.dumps(response).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        except Exception as e:
            # Internal server error – log and respond with a friendly message
            print('Error handling /chat:', e)
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            err_msg = json.dumps({'reply': 'Sorry, the chatbot encountered an unexpected error.'}).encode('utf-8')
            self.send_header('Content-Length', str(len(err_msg)))
            self.end_headers()
            self.wfile.write(err_msg)

def get_gemini_reply(user_message: str) -> str:
    """Send *user_message* to Gemini and return the extracted answer.
    A minimal system instruction is included to keep responses beginner‑friendly.
    """
    system_prompt = (
        "You are a helpful educational assistant inside a student‑built chatbot. "
        "Answer the user's question clearly and concisely using beginner‑friendly language. "
        "For programming topics, give a short explanation and a simple example when appropriate. "
        "Do not mention the Gemini model or any internal implementation details."
    )
    request_body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": user_message}]}],
        "systemInstruction": {"role": "system", "parts": [{"text": system_prompt}]}
    }).encode('utf-8')
    url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url, data=request_body, method='POST')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp_data = json.loads(resp.read().decode('utf-8'))
        # The Gemini response format contains candidates[0].content.parts[0].text
        try:
            candidate = resp_data['candidates'][0]
            text = candidate['content']['parts'][0]['text']
            return text.strip()
        except (KeyError, IndexError):
            return None


def run_server(port: int = 5000):
    # Change working directory to project root so static files are served correctly
    script_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    os.chdir(project_root)
    handler = ChatHandler
    # Enable address reuse to avoid 'address already in use' errors on rapid restarts
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Chatbot server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    run_server()
