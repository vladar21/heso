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


document.addEventListener('DOMContentLoaded', function() {
    var djangoMessagesContainer = document.getElementById('django-messages');
    if (djangoMessagesContainer) {
        var messages = djangoMessagesContainer.getElementsByClassName('django-message');
        for (var i = 0; i < messages.length; i++) {
            var message = messages[i];
            var type = message.getAttribute('data-type'); // 'success', 'error' и т.д.
            var text = message.getAttribute('data-message');
            showMessage(type, text);
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    var isStudentCheckbox = document.getElementById('id_is_student');
    var isTeacherCheckbox = document.getElementById('id_is_teacher');

    if (isStudentCheckbox && isTeacherCheckbox) {
        isStudentCheckbox.addEventListener('change', function() {
            if (this.checked) {
                isTeacherCheckbox.checked = false;
            }
        });

        isTeacherCheckbox.addEventListener('change', function() {
            if (this.checked) {
                isStudentCheckbox.checked = false;
            }
        });
    }
});


