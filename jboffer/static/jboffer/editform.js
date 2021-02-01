document.addEventListener("DOMContentLoaded", function() {
    console.log('Dom loaded and parsed')
    
    const showEditIcon = document.getElementById('show-edit')
    const editForm = document.getElementById('edit-form');
    const deleteIcon = document.getElementById("show-delete");
    const deleteForm = document.getElementById('delete-form');
    

    showEditIcon.addEventListener('click', function(e) {
        e.preventDefault();
        editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
    })
    deleteIcon.addEventListener('click', function(e) {
        e.preventDefault();
        deleteForm.style.display = deleteForm.style.display === 'none' ? 'block' : 'none';
    })
    
    const discardButton = document.getElementById('discard-edit');
    discardButton.addEventListener('click', function(e) {
        e.preventDefault();
        editForm.style.display = 'none';
      }) 

    const discardDelete = document.getElementById('discard-delete');
    discardDelete.addEventListener('click', function(e) {
        e.preventDefault();
        deleteForm.style.display = 'none';
      })
});
