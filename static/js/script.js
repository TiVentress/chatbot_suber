document.addEventListener("DOMContentLoaded", () => {
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotToggler = document.getElementById('chatbot-toggler');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const chatBody = document.getElementById('chatbot-body');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const API_URL = "http://127.0.0.1:5000/chat";

    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', `${sender}-message`);
        messageDiv.innerHTML = text;
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    };

    const handleUserMessage = async () => {
        const userText = userInput.value.trim();
        if (userText === "") return;

        addMessage(userText, 'user');
        userInput.value = ''; 

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userText }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            addMessage(data.response, 'bot');

        } catch (error) {
            console.error("Erro ao contatar a API:", error);
            addMessage("Desculpe, estou com problemas para me conectar. Tente novamente mais tarde.", 'bot');
        }
    };

    chatbotToggler.addEventListener('click', () => chatbotContainer.classList.toggle('show'));
    closeBtn.addEventListener('click', () => chatbotContainer.classList.remove('show'));
    sendBtn.addEventListener('click', handleUserMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleUserMessage();
        }
    });

    setTimeout(() => {
       addMessage("Olá! Sou a assistente virtual da SUBER. Como posso te ajudar?", 'bot');
    }, 1000);
});