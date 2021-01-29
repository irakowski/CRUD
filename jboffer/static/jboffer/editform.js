document.addEventListener("DOMContentLoaded", function() {
    console.log('Dom loaded and parsed')
    
    const showEditIcon = document.getElementById('show-edit')
    const editForm = document.getElementById('edit-form');
    
    showEditIcon.addEventListener('click', function(e) {
        e.preventDefault();
        editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
    
    const discardButton = document.getElementById('discard-edit');
    discardButton.addEventListener('click', function(e) {
        e.preventDefault();
        editForm.style.display = 'none'
        })
    });    
});
