// initialize functions for both index and detail pages
function initAppPage() {
    initializeInteractions();
    initializeOpenAI_ResponseHandling();
    initializeImageStyling();
    initializeQuestionInputForm();
}

// initialize and update rating from frontend
function initializeInteractions() {
    const updateInteractForms = document.querySelectorAll('.interactForm');
    updateInteractForms.forEach(form => {

        const formUrl = form.getAttribute('data-url');
        const csrfToken = form.getAttribute('data-csrf-token');

        const questionId = form.getAttribute('data-question-id');
        const replyId = form.getAttribute('data-reply-id');
        const accountId = form.getAttribute('data-account-id');

        const questionRatingCountSpan = form.querySelector('.question-rating-count');
        const replyRatingCountSpan = form.querySelector('.reply-rating-count');

        const questionRatingIcon = document.getElementById(`rating-${questionId}`);
        const replyRatingIcon = document.getElementById(`rating-reply-${replyId}`);
        
        const questionBookmarkIcon = document.getElementById(`bookmark-${questionId}`);
        const replyBookmarkIcon = document.getElementById(`bookmark-reply-${replyId}`);

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            // send form data to views handling rating
            fetch(formUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                }
            // check response for errors
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`)
                }
                return response.json();
            
            // process data
            }).then(data => {
                if (data.status.includes("rating")){ updateRating(data); } 
                else if (data.status.includes("follow")){ updateFollow(data, accountId); } 
                else {updateBookmark(data); }

            }).catch(error => {
                console.error('Error updating: ', error);
            });
        });

        // determines whether to add/remove rating on question/reply
        function updateRating(data) {
            if (data.status === 'add_question_rating') {
                const currentCount = parseInt(questionRatingCountSpan.textContent, 10) || 0;
                questionRatingCountSpan.textContent = currentCount + 1; // Increment count
                questionRatingIcon.classList.remove('bi-hand-thumbs-up');
                questionRatingIcon.classList.add('bi-hand-thumbs-up-fill');

            } else if (data.status === 'remove_question_rating') {
                const currentCount = parseInt(questionRatingCountSpan.textContent, 10) || 0;
                questionRatingCountSpan.textContent = Math.max(currentCount - 1, 0); // Decrement count
                questionRatingIcon.classList.remove('bi-hand-thumbs-up-fill');
                questionRatingIcon.classList.add('bi-hand-thumbs-up');
            
            } else if (data.status === 'add_reply_rating') {
                const currentCount = parseInt(replyRatingCountSpan.textContent, 10) || 0;
                replyRatingCountSpan.textContent = currentCount + 1; // Increment count
                replyRatingIcon.classList.remove('bi-hand-thumbs-up');
                replyRatingIcon.classList.add('bi-hand-thumbs-up-fill');

            } else if (data.status === 'remove_reply_rating') {
                const currentCount = parseInt(replyRatingCountSpan.textContent, 10) || 0;
                replyRatingCountSpan.textContent = Math.max(currentCount - 1, 0); // Decrement count
                replyRatingIcon.classList.remove('bi-hand-thumbs-up-fill');
                replyRatingIcon.classList.add('bi-hand-thumbs-up');

            } else {
                console.error('Error updating the rating: ', data.status);
            }
        }

        // determines whether to add/remove follow on question/reply user
        function updateFollow(data, accountId) {
            const followIcons = document.querySelectorAll(`.follow-${accountId}`);
            const followTextSpans = document.querySelectorAll(`.follow-text-${accountId}`);
            const followSubmitButtons = document.querySelectorAll(`.follow-submit-${accountId}`);
            
            if (data.status === 'add_user_follow') {
                followIcons.forEach(icon => {
                    icon.classList.remove('bi-plus-lg');
                    icon.classList.add('bi-person-fill-check');
                });
                followTextSpans.forEach(span => {
                    span.textContent = "";
                });
                followSubmitButtons.forEach(button => {
                    button.classList.remove('follow-button');
                    button.classList.add('unfollow-button');
                });
            } else if (data.status === 'remove_user_follow') {
                followIcons.forEach(icon => {
                    icon.classList.remove('bi-person-fill-check');
                    icon.classList.add('bi-plus-lg');
                });
                followTextSpans.forEach(span => {
                    span.textContent = "Follow";
                });
                followSubmitButtons.forEach(button => {
                    button.classList.remove('unfollow-button');
                    button.classList.add('follow-button');
                });
            } else {
                console.error('Error updating the follow: ', data.status);
            }
        }

        // determines whether to add/remove bookmark on question/reply
        function updateBookmark(data) {
            if (data.status === 'add_question_bookmark') {
                questionBookmarkIcon.classList.remove('bi-bookmark-plus');
                questionBookmarkIcon.classList.add('bi-bookmark-check-fill');

            } else if (data.status === 'remove_question_bookmark') {
                questionBookmarkIcon.classList.remove('bi-bookmark-check-fill');
                questionBookmarkIcon.classList.add('bi-bookmark-plus');
            
            } else if (data.status === 'add_reply_bookmark') {
                replyBookmarkIcon.classList.remove('bi-bookmark-plus');
                replyBookmarkIcon.classList.add('bi-bookmark-check-fill');

            } else if (data.status === 'remove_reply_bookmark') {
                replyBookmarkIcon.classList.remove('bi-bookmark-check-fill');
                replyBookmarkIcon.classList.add('bi-bookmark-plus');

            } else {
                console.error('Error updating the bookmark: ', data.status);
            }
        }
    });
}


// handle openai api responses
function initializeOpenAI_ResponseHandling() {
    const updateSummaryForm = document.querySelector('.summaryForm');
    if (updateSummaryForm) {
        const formUrl = updateSummaryForm.getAttribute('data-url');
        const csrfToken = updateSummaryForm.getAttribute('data-csrf-token');
        const summaryTextSpan = updateSummaryForm.querySelector('.summary-text-span');
        const loadButton = updateSummaryForm.querySelector('#loadButton');
        const loader = updateSummaryForm.querySelector('#loader');

        updateSummaryForm.addEventListener('submit', function (e) {
            e.preventDefault();
            
            loadButton.disabled = true;
            loader.style.display = 'inline-block';

            // post data to wisqerbot view
            fetch(formUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                //body: JSON.stringify({})

            // handle response from view
            }).then(response => {
                handleAPI_Response(response);       
                return response.json();
            
            // process data (openai api response message)
            }).then(data => {
                handleAPI_Data(data);

            }).catch(error => {
                console.error('Error generating summary:', error);
                loadButton.disabled = false;
                loader.style.display = 'none';
            });
        });


        // handle api response
        function handleAPI_Response(response) {
            if (!response.ok) {
                summaryTextSpan.style.color = "red";
                loadButton.style.borderColor = "red";

                // NOT CURRENTLY IN USE
                if (response.status === 401) {
                    summaryTextSpan.textContent = "Please login to use this feature";
                    loadButton.disabled = true;

                    throw new Error('User not logged-in');

                } else if (response.status === 429) {
                    // handle throttling of api requests
                    return response.json().then(data => {
                        // prepare message for throttled user
                        const waitTime = data.wait_time || 60*60;
                        console.log(`${data.wait_time}, waitTime = ${waitTime}`);
                        summaryTextSpan.textContent = `Please wait ${Math.floor(waitTime/60)} minutes before requesting another summary.`;

                        loadButton.disabled = true;

                        // disable button until wait time is over
                        setTimeout(() => {
                            loadButton.disabled = false;
                            summaryTextSpan.textContent = 'Generate new summary';
                            summaryTextSpan.style.color = "darkmagenta";
                            loadButton.style.borderColor = "darkmagenta";
                        }, waitTime * 1000);
                        throw new Error('Too many requests');
                    });
                                 
                } else {
                    throw new Error(`HTTP error! Status: ${response.status}`)
                }
            }
        }


        // handle api response message
        function handleAPI_Data(data) {
            if (data.message) {
                const text = data.message;
                summaryTextSpan.style.color = "darkmagenta";

                // display with typewriter effect
                function displayGeneratedText(summaryTextSpan, text, i=0) {
                    if (i === 0) { summaryTextSpan.textContent = ''; }

                    // add each character from data text to summary span text content
                    summaryTextSpan.textContent += text[i];

                    // if end of string
                    if (i === text.length - 1) { return; }

                    setTimeout(() => displayGeneratedText(summaryTextSpan, text, i+1), 10);
                }
                displayGeneratedText(summaryTextSpan, text);

            } else if (data.error) {
                summaryTextSpan.textContent = data.error;
            }
            loadButton.disabled = false;
            loader.style.display = 'none'
        }
    }
}


// applies rounded corners conditionally
function initializeImageStyling() {
    const imageHolders = document.querySelectorAll('.image-holder');
    imageHolders.forEach(holder => {
        const img = holder.querySelector('.question-image');
        if (img) {
            img.onload = function() {
                if (img.naturalWidth >= holder.clientWidth) {
                    img.classList.add('rounded');
                } else {
                    img.classList.remove('rounded');
                }
            };
            // Trigger the load event in case the image is already loaded
            if (img.complete) {
                img.onload();
            }
        }
    });
}


function initializeQuestionInputForm() {
    // collapse question body field
    var questionBodyCollapse = new bootstrap.Collapse(
        document.getElementById('questionBodyCollapse'), {
            toggle: false
        });

    // show character count upon form focus
    var charCountToggle = new bootstrap.Collapse(
        document.querySelector('.countChars-question-value'), {
            toggle: false
    });
    
    const charCountQuestionForms = document.querySelectorAll('.countChars');
    const questionFormContainer = document.querySelector('.question-form-container');
    const charCount = document.querySelector('.countChars-question-value');
    charCountQuestionForms.forEach(countForm => {
        countForm.addEventListener('focus', function() {
            questionBodyCollapse.show();
            // delay character count toggle to allow question input time to expand
            setTimeout(function() {
                charCountToggle.show();
            }, 300)
        });

        // add background color to question input upon mouseover
        questionFormContainer.addEventListener('mouseover', () => {
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


/* initAppPage - INITIALIZE ALL ABOVE FUNCTIONS UPON CONTENT LOAD */
document.addEventListener('DOMContentLoaded', initAppPage);


// TOOLTIPS
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// POPOVERS
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})
    