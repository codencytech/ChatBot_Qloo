// Get references to input box, send button, and chat container
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatContainer = document.getElementById("chat-container");

// Add event listener for send button
sendBtn.addEventListener("click", handleUserMessage);

// Trigger send on Enter key
userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    handleUserMessage();
  }
});

// Function to handle sending user message and fake bot response
function handleUserMessage() {
  const message = userInput.value.trim();
  if (message === "") return;

  // Show user's message
  addMessage(message, "user");
  userInput.value = "";

  // Call backend Flask API
  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  })
    .then((res) => res.json())
    .then((data) => {
      const botReply = data.reply;
      addMessage(botReply, "bot");
    })
    .catch((error) => {
      console.error("Error:", error);
      addMessage("Oops! Failed to connect to the bot server.", "bot");
    });
}

// Function to create and append message bubble
function addMessage(text, sender) {
  const msgBubble = document.createElement("div");
  msgBubble.classList.add("message", sender);
  msgBubble.textContent = text;

  // Wrap in a container for alignment
  const msgWrapper = document.createElement("div");
  msgWrapper.classList.add("flex", "w-full");
  msgWrapper.classList.add(sender === "user" ? "justify-end" : "justify-start");
  msgWrapper.appendChild(msgBubble);

  // Add to chat
  chatContainer.appendChild(msgWrapper);

  // Auto-scroll to bottom
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
