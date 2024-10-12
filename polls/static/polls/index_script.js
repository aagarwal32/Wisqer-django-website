document.addEventListener('DOMContentLoaded', function() {
    var questionTextInputId = document.getElementById('questionTextInputId').value;
    var questionTextInput = document.getElementById(questionTextInputId);
    var questionBodyCollapse = new bootstrap.Collapse(
        document.getElementById('questionBodyCollapse'), {
            toggle: false
        });
    
    // show question body upon question text input focus
    questionTextInput.addEventListener('focus', function() {
        questionBodyCollapse.show();
    });

    // auto-resize textareas
    function autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }
    var textareas = document.querySelectorAll('textarea.autoExpand');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(textarea);
        });
        // adjust height on page load
        autoResizeTextarea(textarea);
    });
});