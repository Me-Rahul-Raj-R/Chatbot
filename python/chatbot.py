import http.server
import socketserver
import json
import os
import urllib.request
import urllib.error
from urllib.parse import urlparse
from typing import Dict, List, Any

# Import knowledge base logic
from python.knowledge_base import (
    normalize_text,
    retrieve_local_answer,
    get_varied_fallback
)

# In-memory session context storage for follow-up questions
SESSION_CONTEXT: Dict[str, Dict[str, Any]] = {}

def get_session_context(session_id: str) -> Dict[str, Any]:
    """Retrieve or initialize session state for context tracking."""
    if session_id not in SESSION_CONTEXT:
        SESSION_CONTEXT[session_id] = {
            "last_topic": None,
            "history": [] # bounded list of recent (user, bot) turns
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


# ---------- Gemini API Fallback Integration ----------
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-1.5-flash' # modern standard fallback model
GEMINI_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'

def get_gemini_reply(user_message: str, history: List[Dict[str, str]] = None) -> str:
    """
    Send query to Gemini API with strict system instructions when GEMINI_API_KEY is configured.
    Receives bounded recent conversation history for natural follow-ups.
    """
    if not GEMINI_API_KEY:
        return None

    system_instruction = (
        "You are an educational assistant built inside a student's Conversational Chatbot project. "
        "Explain technical concepts (Python, Web Development, Databases, CS Fundamentals) clearly, "
        "concisely, and using beginner-friendly language. "
        "Keep simple definitions to 2-4 sentences. For code questions, provide short, safe, working code snippets. "
        "Never claim to be ChatGPT or mention internal model details or API keys."
    )

    contents = []
    # Include up to last 3 context turns
    if history:
        for turn in history[-3:]:
            contents.append({"role": "user", "parts": [{"text": turn["user"]}]})
            contents.append({"role": "model", "parts": [{"text": turn["bot"]}]})
    
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    request_payload = {
        "contents": contents,
        "systemInstruction": {
            "role": "system",
            "parts": [{"text": system_instruction}]
        }
    }

    try:
        url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
        data_bytes = json.dumps(request_payload).encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            candidate = res_json.get('candidates', [])[0]
            parts = candidate.get('content', {}).get('parts', [])
            if parts and 'text' in parts[0]:
                return parts[0]['text'].strip()
    except Exception as e:
        # Log server-side silently without breaking or exposing secrets to client
        print("[Server] Gemini API call failed or unavailable:", e)
    
    return None


# ---------- Process Message Pipeline ----------
def process_user_message(message: str, session_id: str = "default") -> str:
    """
    Hybrid Answering Architecture Pipeline:
    1. Check local normalized knowledge base.
    2. If local answer exists, return it.
    3. If local answer is missing AND Gemini API key is configured, query Gemini API.
    4. Otherwise, return a polite, varied fallback response listing available topics.
    """
    if not message or not message.strip():
        return ""

    ctx = get_session_context(session_id)
    
    # Check local knowledge base first
    local_reply, topic = retrieve_local_answer(message, ctx)
    if local_reply:
        update_session_context(session_id, message, local_reply, topic)
        return local_reply

    # Try Gemini fallback if configured
    gemini_reply = get_gemini_reply(message, ctx.get("history"))
    if gemini_reply:
        update_session_context(session_id, message, gemini_reply, "gemini_ai")
        return gemini_reply

    # Friendly fallback
    fallback_reply = get_varied_fallback()
    update_session_context(session_id, message, fallback_reply)
    return fallback_reply


# ---------- HTTP Server Handler ----------
class ChatHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static frontend files and handles POST /chat requests."""

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
                err_bytes = json.dumps({'reply': 'Sorry, the server encountered an internal error processing your request.'}).encode('utf-8')
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
        print(f"Chatbot server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    run_server()
