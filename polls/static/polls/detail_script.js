function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

document.addEventListener('input', function (event) {
    if (event.target.classList.contains('autoExpand')) {
        autoResizeTextarea(event.target);
    }
}, false);

document.addEventListener('DOMContentLoaded', function () {
    var textareas = document.querySelectorAll('textarea.autoExpand');
    textareas.forEach(function (textarea) {
        autoResizeTextarea(textarea);
    });
});