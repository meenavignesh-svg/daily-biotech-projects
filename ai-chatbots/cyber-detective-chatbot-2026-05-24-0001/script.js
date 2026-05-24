const messages = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');

const replies = [
  {
    match: ['hello', 'hi', 'hey'],
    text: 'Detective Node reporting in. Drop a clue and I will trace the signal.'
  },
  {
    match: ['who', 'name'],
    text: 'I am Cyber Detective, a browser-based chatbot trained for suspicious patterns, missing context, and dramatic case names.'
  },
  {
    match: ['scan', 'clue', 'case'],
    text: 'Initial scan complete: look for repeated words, strange links, urgent language, and anything asking for secrets.'
  },
  {
    match: ['tip', 'cyber', 'security'],
    text: 'Cyber tip: never paste passwords, tokens, or one-time codes into a chat. Real investigators do not need your keys.'
  },
  {
    match: ['help', 'solve'],
    text: 'Build the timeline first: what happened, when it happened, what changed, and who touched the system last.'
  }
];

function addMessage(text, sender) {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender}`;
  bubble.textContent = text;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function getBotReply(text) {
  const clean = text.toLowerCase();
  const hit = replies.find((reply) => reply.match.some((word) => clean.includes(word)));

  if (hit) return hit.text;

  return `Interesting clue: "${text}". I would tag it, compare it with the timeline, and ask what evidence supports it.`;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  input.value = '';

  window.setTimeout(() => {
    addMessage(getBotReply(text), 'bot');
  }, 350);
});

addMessage('Case opened. What clue should we investigate first?', 'bot');
