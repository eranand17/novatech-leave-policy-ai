const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");

const API_URL = "/ask";


function addMessage(type, content, sources = []) {
    const message = document.createElement("div");
    message.className = `message ${type}-message`;

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = type === "user" ? "You" : "NovaTech AI";

    const text = document.createElement("div");
    text.className = "message-content";
    text.innerHTML = content.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    message.appendChild(label);
    message.appendChild(text);

    if (sources.length) {
        const sourceBox = document.createElement("div");
        sourceBox.className = "sources";

        const title = document.createElement("div");
        title.className = "sources-title";
        title.textContent = "Sources";

        sourceBox.appendChild(title);

        sources.forEach(source => {
            const item = document.createElement("div");
            item.className = "source-item";
            item.textContent = `${source.section} — Page ${source.page}`;
            sourceBox.appendChild(item);
        });

        message.appendChild(sourceBox);
    }

    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function showLoading() {
    addMessage("assistant", "Thinking...");
}


function removeLoading() {
    const messages = chatMessages.querySelectorAll(".assistant-message");
    const last = messages[messages.length - 1];

    if (last && last.textContent.includes("Thinking...")) {
        last.remove();
    }
}


async function askQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage("user", question);

    questionInput.value = "";
    sendButton.disabled = true;

    showLoading();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();

        removeLoading();

        addMessage(
            "assistant",
            data.answer,
            data.sources || []
        );

    } catch (error) {
        removeLoading();

        addMessage(
            "assistant",
            "Sorry, I could not connect to the Leave Policy AI server."
        );

    } finally {
        sendButton.disabled = false;
        questionInput.focus();
    }
}


sendButton.addEventListener("click", askQuestion);


questionInput.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        askQuestion();
    }
});