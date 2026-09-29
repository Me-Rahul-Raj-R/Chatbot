import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from typing import Dict, List, Any

# Import rule-based knowledge engine
from python.knowledge_base import (
    normalize_text,
    retrieve_local_answer,
    get_varied_fallback
)

# In-memory session context storage for context-aware follow-up questions
SESSION_CONTEXT: Dict[str, Dict[str, Any]] = {}

def get_session_context(session_id: str) -> Dict[str, Any]:
    """Retrieve or initialize session state for context tracking."""
    if session_id not in SESSION_CONTEXT:
        SESSION_CONTEXT[session_id] = {
            "last_topic": None,
            "history": [] # Bounded recent turns
        }
    return SESSION_CONTEXT[session_id]

def update_session_context(session_id: str, user_msg: str, bot_reply: str, topic: str = None):
    """Store recent turn in session context, bounded to last 5 turns."""
    ctx = get_session_context(session_id)
    if topic:
        ctx["last_topic"] = topic
    ctx["history"].append({"user": user_msg, "bot": bot_reply})
    if len(ctx["history"]) > 5:
        ctx["history"].pop(0)

def clear_session_context(session_id: str):
    """Reset session context on clear chat."""
    if session_id in SESSION_CONTEXT:
        SESSION_CONTEXT[session_id] = {"last_topic": None, "history": []}


# ---------- Process User Message Pipeline ----------
def process_user_message(message: str, session_id: str = "default") -> str:
    """
    Process incoming message using rule-based normalization and matching.
    1. Check for empty or whitespace input.
    2. Check local knowledge base for exact/alias/pattern match.
    3. Update session context if match found.
    4. Fall back to polite topic-guided fallback if query is unmapped.
    """
    if not message or not message.strip():
        return "Please ask a question! I am happy to help you with Python, Java, HTML, CSS, JavaScript, OOP, or SQL."

    ctx = get_session_context(session_id)
    
    # Check local knowledge base
    local_reply, topic = retrieve_local_answer(message, ctx)
    if local_reply:
        update_session_context(session_id, message, local_reply, topic)
        return local_reply

    # Polite fallback
    fallback_reply = get_varied_fallback()
    update_session_context(session_id, message, fallback_reply)
    return fallback_reply


# ---------- HTTP Server Handler ----------
class ChatHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static frontend files and handles POST /chat and POST /reset endpoints."""

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            
            try:
                payload = json.loads(raw_body.decode('utf-8'))
                user_msg = payload.get('message', '')
                session_id = payload.get('sessionId', 'default_session')
                
                reply = process_user_message(user_msg, session_id)
                response_data = {'reply': reply}
                resp_bytes = json.dumps(response_data).encode('utf-8')
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.end_headers()
                self.wfile.write(resp_bytes)
            except Exception as e:
                print("[Server Error] Error handling /chat request:", e)
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                err_bytes = json.dumps({'reply': 'Sorry, the server encountered an unexpected error processing your request.'}).encode('utf-8')
                self.send_header('Content-Length', str(len(err_bytes)))
                self.end_headers()
                self.wfile.write(err_bytes)

        elif parsed_path.path == '/reset':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            try:
                payload = json.loads(raw_body.decode('utf-8')) if raw_body else {}
                session_id = payload.get('sessionId', 'default_session')
                clear_session_context(session_id)
            except Exception:
                pass
            
            resp_bytes = json.dumps({'status': 'ok'}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        else:
            self.send_error(404, "Endpoint Not Found")

def run_server(port: int = 5000):
    script_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    os.chdir(project_root)
    
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), ChatHandler) as httpd:
        print(f"Conversational Chatbot server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    run_server()
