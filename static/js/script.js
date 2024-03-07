function showMessage(type, text) {

    var container = document.getElementById('messages-container');
    var message = document.createElement('div');
    message.classList.add('alert', 'alert-' + type);
    message.textContent = text;
    container.appendChild(message);

    setTimeout(function() {
        container.removeChild(message);
    }, 5000);
}