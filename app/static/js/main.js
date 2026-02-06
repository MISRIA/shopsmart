// Initialize Bootstrap Tooltips
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    console.log('ShopSmart Frontend Loaded');

    // Chatbot Logic
    const chatbotToggler = document.querySelector('.chatbot-toggler');
    const chatbotClose = document.querySelector('.chatbot-close');
    const chatbotInterface = document.querySelector('.chatbot-interface');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotMessages = document.getElementById('chatbot-messages');

    if (chatbotToggler) {
        chatbotToggler.addEventListener('click', () => {
            chatbotInterface.classList.toggle('d-none');
        });
    }

    if (chatbotClose) {
        chatbotClose.addEventListener('click', () => {
            chatbotInterface.classList.add('d-none');
        });
    }

    const appendMessage = (text, type) => {
        const div = document.createElement('div');
        div.className = `d-flex flex-row justify-content-${type === 'user' ? 'end' : 'start'} mb-2`;
        div.innerHTML = `<div class="chatbot-message-${type}">${text}</div>`;
        chatbotMessages.appendChild(div);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    };

    const sendMessage = async () => {
        const message = chatbotInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        chatbotInput.value = '';

        // Initial "thinking" state could be added here

        try {
            const response = await fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            appendMessage(data.response, 'bot');
        } catch (error) {
            console.error('Error:', error);
            appendMessage("Sorry, I'm having connection issues.", 'bot');
        }
    };

    if (chatbotSend) {
        chatbotSend.addEventListener('click', sendMessage);
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // Auto-dismiss alerts after 3 seconds
    setTimeout(function () {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 3000);
});
