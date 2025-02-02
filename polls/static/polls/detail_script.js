// textarea auto expand handling
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

document.addEventListener('DOMContentLoaded', function () {

    var charCountToggle = new bootstrap.Collapse(
        document.querySelector('.countChars-value'), {
            toggle: false
    });
    
    // show character count upon form focus
    const charCountForms = document.querySelectorAll('.countChars')
    const charCount = document.querySelector('.countChars-value');
    charCountForms.forEach(countForm => {
        countForm.addEventListener('focus', function() {
            charCountToggle.show();
        });

        countForm.addEventListener('hover', () => {
            countForm.style.backgroundColor = "rgba(0, 0, 0, .03)";
        })

        countForm.addEventListener('input', () => {
            const remainingChars = countForm.maxLength - countForm.value.length;
            charCount.textContent = remainingChars;
            //charCount.style.marginLeft = "4px";

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


    const textareas = document.querySelectorAll('textarea.autoExpand');

    textareas.forEach(function (textarea) {
        autoResizeTextarea(textarea); // initial resize
        textarea.addEventListener('click', function () {
            autoResizeTextarea(textarea);
        });
        textarea.addEventListener('input', function () {
            autoResizeTextarea(textarea);
        });
    });
});

// update modal post handling
document.addEventListener('DOMContentLoaded', function () {
    const updateForm = document.getElementById('updateModalForm');

    const formUrl = updateForm.getAttribute('data-url');
    const csrfToken = updateForm.getAttribute('data-csrf-token');

    updateForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(updateForm);
        fetch(formUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        }).then(response => response.json()).then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('updateModalQuestion'));
                modal.hide();
                location.reload();
            } else {
                console.error(data.errors);
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    });
});