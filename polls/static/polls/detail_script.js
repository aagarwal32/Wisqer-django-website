// textarea auto expand handling
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

document.addEventListener('DOMContentLoaded', function () {
    const textareas = document.querySelectorAll('textarea.autoExpand');

    textareas.forEach(function (textarea) {
        autoResizeTextarea(textarea); // initial resize
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