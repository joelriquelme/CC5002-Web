// Cargar el JSON
fetch('region_comuna.json')
    .then(response => response.json())
    .then(data => {
        const regionSelect = document.getElementById('region');
        const comunaSelect = document.getElementById('comuna');

        // Poblar regiones
        data.regiones.forEach(region => {
            const option = document.createElement('option');
            option.value = region.id;
            option.textContent = region.nombre;
            regionSelect.appendChild(option);
        });

        // Poblar comunas según la región seleccionada
        regionSelect.addEventListener('change', function() {
            comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
            
            const selectedRegion = data.regiones.find(region => region.id == this.value);
            if (selectedRegion) {
                selectedRegion.comunas.forEach(comuna => {
                    const option = document.createElement('option');
                    option.value = comuna.id;
                    option.textContent = comuna.nombre;
                    comunaSelect.appendChild(option);
                });
            }
        });
    })
    .catch(error => console.error('Error loading the JSON:', error));

document.addEventListener('DOMContentLoaded', () => {
    const deviceContainer = document.getElementById('device-container');
    const addDeviceButton = document.getElementById('add-device');
    const removeDeviceButton = document.getElementById('remove-device');
    const publishDonationButton = document.getElementById('publish-donation');
    const confirmationMessage = document.getElementById('confirmation-message');
    const thankYouMessage = document.getElementById('thank-you-message');
    const confirmPublishButton = document.getElementById('confirm-publish');
    const cancelPublishButton = document.getElementById('cancel-publish');
    const donationForm = document.getElementById('donation-form');

    addDeviceButton.addEventListener('click', (e) => {
        e.preventDefault();

        // Clonar el conjunto de campos para un nuevo dispositivo
        const newDevice = document.querySelector('.device-info').cloneNode(true);
        
        // Limpiar los campos del nuevo dispositivo
        newDevice.querySelectorAll('input, textarea').forEach(input => {
            input.value = '';
        });

        deviceContainer.appendChild(newDevice);
    });

    removeDeviceButton.addEventListener('click', (e) => {
        e.preventDefault();

        // Eliminar el último conjunto de campos para el dispositivo
        const deviceInfos = deviceContainer.querySelectorAll('.device-info');
        if (deviceInfos.length > 1) {
            deviceContainer.removeChild(deviceInfos[deviceInfos.length - 1]);
        } else {
            alert('Debe haber al menos un dispositivo.');
        }
    });

    publishDonationButton.addEventListener('click', (e) => {
        e.preventDefault();
            confirmationMessage.classList.remove('hidden');
    });

    confirmPublishButton.addEventListener('click', () => {
        confirmationMessage.classList.add('hidden');
        thankYouMessage.classList.remove('hidden');
    });

    cancelPublishButton.addEventListener('click', () => {
        confirmationMessage.classList.add('hidden');
    });
});

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
