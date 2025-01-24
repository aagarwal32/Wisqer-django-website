// update question and reply rating
document.addEventListener('DOMContentLoaded', function() {
    const updateRatingForms = document.querySelectorAll('.ratingForm');
    updateRatingForms.forEach(form => {

        const formUrl = form.getAttribute('data-url');
        const csrfToken = form.getAttribute('data-csrf-token');

        const questionId = form.getAttribute('data-question-id');
        const replyId = form.getAttribute('data-reply-id');
        const questionRatingCountSpan = form.querySelector('.question-rating-count');
        const replyRatingCountSpan = form.querySelector('.reply-rating-count');
        const questionRatingIcon = document.getElementById(`icon-${questionId}`);
        const replyRatingIcon = document.getElementById(`icon-${replyId}`);

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            fetch(formUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                }
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`)
                }
                return response.json();
            })
            .then(data => {
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
            }).catch(error => {
                console.error('Error updating the rating: ', error);
            });
        });
    });
});
    

// handle openai api responses
document.addEventListener('DOMContentLoaded', function() {
    const updateSummaryForm = document.querySelector('.summaryForm');
    if (updateSummaryForm) {
        const formUrl = updateSummaryForm.getAttribute('data-url');
        const csrfToken = updateSummaryForm.getAttribute('data-csrf-token');
        const summaryTextSpan = updateSummaryForm.querySelector('.summary-text-span');

        updateSummaryForm.addEventListener('submit', function (e) {
            e.preventDefault();

            fetch(formUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                //body: JSON.stringify({})
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`)
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    const icon = document.createElement('i');
                    icon.className = 'bi-stars';
                    icon.style.marginRight = '5px';

                    const text = 'WisqerAI: ' + data.message;
                    summaryTextSpan.style.color = "darkmagenta";
                    summaryTextSpan.appendChild(icon);

                    function displayGeneratedText(summaryTextSpan, text, i=0) {
                        if (i === 0) {
                            summaryTextSpan.textContent = '';
                        }
                        
                        summaryTextSpan.textContent += text[i];

                        // if end of string
                        if (i === text.length - 1) {
                            return;
                        }

                        setTimeout(() => displayGeneratedText(summaryTextSpan, text, i+1), 10);
                    }
                    displayGeneratedText(summaryTextSpan, text);

                } else if (data.error) {
                    summaryTextSpan.textContent = data.error;
                }
            }).catch(error => {
                console.error('Error generating summary:', error);
            });
        });
    }
});
    