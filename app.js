const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const chatLog = document.getElementById("chat-log");

function addBubble(author, text) {
  const item = document.createElement("article");
  item.className = `bubble ${author}`;
  item.innerHTML = `<p class="author">${author === "user" ? "Você" : "NeuroELIZA"}</p><p>${text}</p>`;
  chatLog.appendChild(item);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function bootstrapConversation() {
  addBubble(
    "bot",
    "Oi! Eu sou a NeuroELIZA ✨. Posso te ouvir com calma, refletir o que você trouxer e te ajudar a aprofundar sem julgamentos."
  );
}

async function sendMessage(message) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || "Falha ao responder.");
  }

  return payload.reply;
}

chatForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  addBubble("user", message);
  messageInput.value = "";
  messageInput.focus();

  try {
    const reply = await sendMessage(message);
    addBubble("bot", reply);
  } catch (error) {
    addBubble("bot", `Deu um erro aqui: ${error.message}`);
  }
});

bootstrapConversation();
