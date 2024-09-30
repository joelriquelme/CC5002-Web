document.addEventListener('DOMContentLoaded', () => {
    const mainImage = document.getElementById('main-image');
    const commenterName = document.getElementById('commenter-name');
    const addCommentButton = document.getElementById('add-comment');
    const commentMessage = document.getElementById('comment-message');
    const commentText = document.getElementById('comment-text');
    const commentForm = document.getElementById('comment-form');

    const validateName = (name) => name && name !== '' && name.length <= 80 && name.length >= 3;
    const validateComment = (comment) => comment && comment !== '' && comment.length >= 5;

    mainImage.addEventListener('click', () => {
        if (mainImage.classList.contains('large-img')) {
            mainImage.classList.remove('large-img');
        } else {
            mainImage.classList.add('large-img');
        }
    });

    addCommentButton.addEventListener('click', () => {
        if (validateName(commenterName.value) && validateComment(commentText.value)) {
            commentMessage.textContent = 'Comentario agregado con éxito.';
            commentMessage.classList.remove('hidden');
            commentForm.reset();
        } else {
            commentMessage.textContent = 'Por favor, ingrese un nombre valido y un comentario.';
            commentMessage.classList.remove('hidden');
        }
    });
});