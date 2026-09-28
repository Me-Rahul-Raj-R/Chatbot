import http.server
import socketserver
import json
import os
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse

# ----- Chatbot logic -----

# Define keyword groups and their responses
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
    with socketserver.ThreadingTCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Chatbot server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    run_server()
