// initialize all functions
function initIndexPage() {
    initializeCustomButtons();
    initializeTextAreaResize();
    initializeQuestionInputForm();
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


function initializeQuestionInputForm() {
    // collapse question body field
    var questionTextInputId = document.getElementById('questionTextInputId').value;
    var questionTextInput = document.getElementById(questionTextInputId);
    var questionBodyCollapse = new bootstrap.Collapse(
        document.getElementById('questionBodyCollapse'), {
            toggle: false
        });

    // show character count upon form focus
    var charCountToggle = new bootstrap.Collapse(
        document.querySelector('.countChars-value'), {
            toggle: false
    });
    
    const charCountForms = document.querySelectorAll('.countChars');
    const questionInputBorder = document.querySelector('.question-inputs-border');
    const charCount = document.querySelector('.countChars-value');
    charCountForms.forEach(countForm => {
        countForm.addEventListener('focus', function() {
            questionBodyCollapse.show();
            // delay character count toggle to allow question input time to expand
            setTimeout(function() {
                charCountToggle.show();
            }, 300)
        });

        // add background color to question input upon mouseover
        questionInputBorder.addEventListener('mouseover', () => {
            countForm.style.backgroundColor = "rgba(0, 0, 0, .005)";
        });

        // update character count
        countForm.addEventListener('input', () => {
            const remainingChars = countForm.maxLength - countForm.value.length;
            charCount.textContent = remainingChars;

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
}


/* initIndexPage - INITIALIZE ALL ABOVE FUNCTIONS UPON CONTENT LOAD */
document.addEventListener('DOMContentLoaded', initIndexPage);