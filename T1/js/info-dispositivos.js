document.addEventListener('DOMContentLoaded', () => {
    const mainImage = document.getElementById('main-image');
    const commentForm = document.getElementById('comment-form');
    const addCommentButton = document.getElementById('add-comment');
    const commentMessage = document.getElementById('comment-message');

    mainImage.addEventListener('click', () => {
        if (mainImage.classList.contains('large-img')) {
            mainImage.classList.remove('large-img');
        } else {
            mainImage.classList.add('large-img');
        }
    });

    addCommentButton.addEventListener('click', () => {
        if (commentForm.checkValidity()) {
            commentMessage.textContent = 'Comentario agregado con éxito.';
            commentMessage.classList.remove('hidden');
            commentForm.reset();
        } else {
            commentMessage.textContent = 'Por favor, complete todos los campos correctamente.';
            commentMessage.classList.remove('hidden');
        }
    });
});