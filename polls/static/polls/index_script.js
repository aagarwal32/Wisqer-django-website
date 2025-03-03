// initialize all functions
function initIndexPage() {
    initializeCustomButtons();
    initializeTextAreaResize();
    initializeImagePreview();
}



// initializes functionality for previewing image attachments
function initializeImagePreview() {
    const previewAttachIconContainer = document.getElementById("imageAttachMarker");
    const previewAttachIcon = previewAttachIconContainer.querySelector(".bi-plus-lg");
    const previewCloseButton = previewAttachIconContainer.querySelector(".btn-close");
    const previewContainer = document.getElementById("imagePreview");
    const previewImage = previewContainer.querySelector(".image-preview__image");
    const inputFile = document.querySelector('input[type="file"][name="question_img"]');
    const loaderPreview = document.querySelector('#loaderPreview');

    // hide elements upon removal of image attachment
    function clearElements() {
        previewCloseButton.style.display = "none";
        previewAttachIcon.style.display = "none";
        loaderPreview.style.display = 'none';
        previewImage.style.display = null;
        previewImage.setAttribute("src", "");
        inputFile.value = "";
    }

    // check for new files
    inputFile.addEventListener("change", function() {
        const file = this.files[0];

        if (file) {
            const reader = new FileReader();

            loaderPreview.style.display = 'inline-block';

            // display image and other elements upon load
            reader.addEventListener("load", function(){
                previewImage.setAttribute("src", this.result);
                previewAttachIcon.style.display = "block";
                previewImage.style.display = "block";
                previewCloseButton.style.display = "block";
                loaderPreview.style.display = 'none';
            });

            reader.readAsDataURL(file);

        } else {
            clearElements();
        }
    });

    // close button that removes image attachment and clears preview
    previewCloseButton.addEventListener("click", function(){
        clearElements();
    });
}

// initialize question input form custom buttons
function initializeCustomButtons() {
    // image button functionality
    const questionImgButton = document.querySelector('input[type="file"][name="question_img"]');
    const customImageButton = document.querySelector('#customImageButton');

    customImageButton.addEventListener('click', function() {
        questionImgButton.click();
    });
}


// auto-resize textareas (helper)
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}
// auto-resize textareas
function initializeTextAreaResize() {
    var textareas = document.querySelectorAll('textarea.autoExpand');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(textarea);
        });
        // adjust height on page load
        autoResizeTextarea(textarea);
    });
}


/* initIndexPage - INITIALIZE ALL ABOVE FUNCTIONS UPON CONTENT LOAD */
document.addEventListener('DOMContentLoaded', initIndexPage);