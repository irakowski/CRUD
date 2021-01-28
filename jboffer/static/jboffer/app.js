document.addEventListener("DOMContentLoaded", function() {
    console.log('Dom loaded and parsed')
    
    const CvButton = document.getElementById('save_cv')
    const inputCv = document.getElementById('save_cv_field');
    
    CvButton.addEventListener('click', function(e) {
        e.preventDefault();
        inputCv.toggleAttribute('hidden');
    });
        
    const coverButton = document.getElementById('cover_letter');
    const inputCover = document.getElementById('save_cover_field');

    coverButton.addEventListener('click', function(e) {
        e.preventDefault();
        inputCover.toggleAttribute('hidden');
    });

    const commentButton = document.getElementById('comment');
    const inputComment = document.getElementById('save_comment_field');

    commentButton.addEventListener('click', function (e) {
        e.preventDefault();
        inputComment.toggleAttribute('hidden');
    });
});