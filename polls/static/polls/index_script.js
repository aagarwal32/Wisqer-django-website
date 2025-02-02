document.addEventListener('DOMContentLoaded', function() {
    var questionTextInputId = document.getElementById('questionTextInputId').value;
    var questionTextInput = document.getElementById(questionTextInputId);
    var questionBodyCollapse = new bootstrap.Collapse(
        document.getElementById('questionBodyCollapse'), {
            toggle: false
        });

    var charCountToggle = new bootstrap.Collapse(
        document.querySelector('.countChars-value'), {
            toggle: false
    });
    
    // show character count upon form focus
    const charCountForms = document.querySelectorAll('.countChars');
    const questionInputBorder = document.querySelector('.question-inputs-border');
    const charCount = document.querySelector('.countChars-value');
    charCountForms.forEach(countForm => {
        countForm.addEventListener('focus', function() {
            questionBodyCollapse.show();
            setTimeout(function() {
                charCountToggle.show();
            }, 300)
        });

        questionInputBorder.addEventListener('mouseover', () => {
            countForm.style.backgroundColor = "rgba(0, 0, 0, .005)";
        })

        countForm.addEventListener('input', () => {
            const remainingChars = countForm.maxLength - countForm.value.length;
            charCount.textContent = remainingChars;
            //charCount.style.marginLeft = "8px";

            if (remainingChars >= 50) {
                charCount.style.color = "rgba(0, 0, 0, .50)";
            }
            else if (remainingChars < 50 && remainingChars != 0) {
                charCount.style.color = "rgba(200, 120, 0, 0.75)";
            }
            else {
                charCount.style.color = "red";
            }
        });
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