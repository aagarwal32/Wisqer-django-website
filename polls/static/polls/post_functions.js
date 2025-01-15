// update question and reply rating
document.addEventListener('DOMContentLoaded', function() {
    const updateRatingForms = document.querySelectorAll('.ratingForm');
    updateRatingForms.forEach(form => {

        const formUrl = form.getAttribute('data-url');
        const csrfToken = form.getAttribute('data-csrf-token');
        const questionId = form.getAttribute('data-question-id');
        const ratingCountSpan = form.querySelector('.rating-count');
        const ratingIcon = document.getElementById(`icon-${questionId}`);

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
                if (data.status === 'add_rating') {
                    const currentCount = parseInt(ratingCountSpan.textContent, 10) || 0;
                    ratingCountSpan.textContent = currentCount + 1; // Increment count
                    ratingIcon.classList.remove('bi-hand-thumbs-up');
                    ratingIcon.classList.add('bi-hand-thumbs-up-fill');

                } else if (data.status === 'remove_rating') {
                    const currentCount = parseInt(ratingCountSpan.textContent, 10) || 0;
                    ratingCountSpan.textContent = Math.max(currentCount - 1, 0); // Decrement count
                    ratingIcon.classList.remove('bi-hand-thumbs-up-fill');
                    ratingIcon.classList.add('bi-hand-thumbs-up');

                } else {
                    console.error('Error updating the rating: ', data.status);
                }
            }).catch(error => {
                console.error('Error updating the rating: ', error);
            });
        });
    });
});
    

    