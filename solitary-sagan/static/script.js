document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const languageSelect = document.getElementById('language-select');

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });

    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.innerText = text;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    const toggleTyping = (show) => {
        const existing = document.querySelector('.typing-indicator');
        if (show && !existing) {
            const indicator = document.createElement('div');
            indicator.classList.add('typing-indicator');
            indicator.innerText = 'Bot is thinking...';
            chatWindow.appendChild(indicator);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        } else if (!show && existing) {
            existing.remove();
        }
    };

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        const language = languageSelect.value;
        addMessage(message, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';

        toggleTyping(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message, language }),
            });

            const data = await response.json();
            toggleTyping(false);

            if (data.status === 'success') {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, I encountered an error.', 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
            toggleTyping(false);
            addMessage('Could not connect to the server.', 'bot');
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
