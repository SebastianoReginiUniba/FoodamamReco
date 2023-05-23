document.getElementById('chat-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const userInput = document.getElementById('user-input').value;
    sendMessageToRasa(userInput);
});

function sendMessageToRasa(message) {
    console.log('Inside function 1')
    // Replace 'http://localhost:5005' with your Rasa server URL
    const url = 'http://localhost:5005/webhooks/rest/webhook';
    const data = {
        "message": message,
        "sender": "user"
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {
        displayChatMessage(response[0].text, 'bot');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayChatMessage(message, sender) {
    console.log('Inside function 2')
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.classList.add(sender);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
