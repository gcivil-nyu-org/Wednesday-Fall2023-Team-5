


const USER_ID = document.getElementById("uid").value
let url = `ws://${window.location.host}/ws/socket-server/`;

const chatSocket = new WebSocket(url);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'chat') {
        let messageStr = `${data.username}: ${data.message} \n`;
        document.querySelector('#chat-log').value += messageStr;
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};