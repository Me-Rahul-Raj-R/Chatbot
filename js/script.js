// script.js - frontend interaction for the chatbot

// DOM elements
const chatWindow = document.getElementById('chatWindow');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const suggestionContainer = document.getElementById('suggestions');

// Welcome message on load
window.addEventListener('load', () => {
  addBotMessage(
    "Hello! I'm your conversational chatbot. You can ask me about Python, HTML, CSS, JavaScript, or basic chatbot concepts."
  );
});

// Helper: create and append a message bubble
function addMessage(type, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', type);
  msgDiv.textContent = text;
  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addUserMessage(text) {
  addMessage('user', text);
}

function addBotMessage(text) {
  addMessage('bot', text);
}

// Send user message to backend
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) {
    // optional feedback – ignore empty input
    return;
  }
  addUserMessage(text);
  userInput.value = '';
  userInput.focus();

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    addBotMessage(data.reply);
  } catch (err) {
    console.error('Fetch error:', err);
    addBotMessage('Chatbot service is currently unavailable. Please make sure the Python application is running.');
  }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendMessage();
  }
});
clearBtn.addEventListener('click', () => {
  chatWindow.innerHTML = '';
  addBotMessage(
    "Hello! I'm your conversational chatbot. You can ask me about Python, HTML, CSS, JavaScript, or basic chatbot concepts."
  );
  userInput.value = '';
  userInput.focus();
});

// Suggestion buttons
if (suggestionContainer) {
  suggestionContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('suggest-btn')) {
      const question = e.target.getAttribute('data-question');
      userInput.value = question;
      sendMessage();
    }
  });
}
