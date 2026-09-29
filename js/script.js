// script.js - Frontend Interaction and Asynchronous Chat API Integration

// DOM Elements
const chatWindow = document.getElementById('chatWindow');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const suggestionContainer = document.getElementById('suggestions');

// Session ID for context tracking
const sessionId = 'session_' + Math.random().toString(36).substring(2, 9);

// Welcome message on load
window.addEventListener('load', () => {
  addBotMessage(
    "Hello! I am your educational assistant. Ask me anything about Python, HTML, CSS, JavaScript, SQL, Data Structures, Git, or CS Fundamentals!"
  );
});

// Helper: format message text (preserve line breaks, code blocks)
function formatMessageText(text) {
  if (!text) return '';
  // Basic HTML escaping
  let escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Format inline code blocks `code`
  escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Format bold text **text**
  escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Format line breaks
  escaped = escaped.replace(/\n/g, '<br/>');

  return escaped;
}

// Helper: create and append a message bubble
function addMessage(type, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', type);
  msgDiv.innerHTML = formatMessageText(text);
  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return msgDiv;
}

function addUserMessage(text) {
  return addMessage('user', text);
}

function addBotMessage(text) {
  return addMessage('bot', text);
}

// Send user message to backend /chat endpoint
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) {
    return;
  }

  // Prevent duplicate submission
  sendBtn.disabled = true;
  clearBtn.disabled = true;

  addUserMessage(text);
  userInput.value = '';
  userInput.focus();

  // Display typing indicator
  const typingElem = addBotMessage('Thinking...');

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, sessionId: sessionId })
    });

    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    const data = await response.json();
    typingElem.innerHTML = formatMessageText(data.reply);
  } catch (err) {
    console.error('Fetch error:', err);
    typingElem.innerHTML = formatMessageText(
      'The chatbot service is currently unreachable. Please make sure the Python server is running on http://localhost:5000.'
    );
  } finally {
    // Re-enable input buttons
    sendBtn.disabled = false;
    clearBtn.disabled = false;
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Clear Chat Action
clearBtn.addEventListener('click', async () => {
  chatWindow.innerHTML = '';
  addBotMessage(
    "Conversation cleared! How can I assist you next? Feel free to ask about Python, SQL, HTML/CSS, JS, or CS concepts."
  );
  userInput.value = '';
  userInput.focus();

  // Reset session context on backend
  try {
    await fetch('/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sessionId: sessionId })
    });
  } catch (e) {
    // Ignore reset network errors silently
  }
});

// Suggestion buttons click handler
if (suggestionContainer) {
  suggestionContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('suggest-btn')) {
      const question = e.target.getAttribute('data-question') || e.target.textContent;
      userInput.value = question;
      sendMessage();
    }
  });
}
