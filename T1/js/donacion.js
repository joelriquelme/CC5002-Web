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

// Validar formulario de donación (Contacto)
const validatorDonationContact = () => {

    const validateName = (name) => name && name.length > 3 && name.length < 80;

    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };

    const validatePhone = (phone) => {
        return String(phone).match(/^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/);
    };

    const validateRegion = (region) => region && region !== '';
    const validateComuna = (comuna) => comuna && comuna !== '';

    let nameInput = document.getElementById('nombre');
    let emailInput = document.getElementById('email');
    let phoneInput = document.getElementById('celular');
    let regionSelect = document.getElementById('region');
    let comunaSelect = document.getElementById('comuna');

    let isValid = false;
    let msg = '';

    if (!validateName(nameInput.value)) {
        msg += 'Nombre inválido.\n';
        nameInput.style.borderColor = 'red';
    } else {
        nameInput.style.borderColor = '';
    };

    if (!validateEmail(emailInput.value)) {
        msg += 'Email inválido.\n';
        emailInput.style.borderColor = 'red';
    } else {
        emailInput.style.borderColor = '';
    };

    if (!validatePhone(phoneInput.value)) {
        msg += 'Teléfono inválido.\n';
        phoneInput.style.borderColor = 'red';
    } else {
        phoneInput.style.borderColor = '';
    };

    if (!validateRegion(regionSelect.value)) {
        msg += 'Debe seleccionar una región.\n';
        regionSelect.style.borderColor = 'red';
    } else {
        regionSelect.style.borderColor = '';
    };

    if (!validateComuna(comunaSelect.value)) {
        msg += 'Debe seleccionar una comuna.\n';
        comunaSelect.style.borderColor = 'red';
    } else {
        comunaSelect.style.borderColor = '';
    };

    if (msg === '') {
        isValid = true;
        document.getElementById('error-message').textContent = msg;
    } else {
        isValid = false;
        document.getElementById('error-message').textContent = msg;
        document.getElementById('error-message').classList.remove('hidden');
    };
};

// Validar formulario de donación (Dispositivos)
const validatorDonationDevices = () => {

    const validateDeviceName = (name) => name && name.length > 3 && name.length < 80;

    const validateDeviceType = (type) => type && type !== '';

    const validateDeviceYears = (years) => years && years > 1 && years < 99;

    const validateDeviceCondition = (condition) => condition && condition !== '';

    // Validar cantidad de archivos de fotos subidas (mínimo 1 y maximo 3)
    const validateDeviceImages = (images) => images && images.length >= 1 && images.length <= 3;
    
    let deviceInfos = document.querySelectorAll('.device-info');
    console.log(deviceInfos);
    let isValid = false;
    let msg = '';


    deviceInfos.forEach((deviceInfo, index) => {
        let deviceNameInput = deviceInfo.querySelector('.device-name');
        console.log(deviceNameInput);
        let deviceTypeSelect = deviceInfo.querySelector('.device-type');
        let deviceYearsInput = deviceInfo.querySelector('.device-years');
        let deviceConditionSelect = deviceInfo.querySelector('.device-condition');
        let deviceImagesInput = deviceInfo.querySelector('.device-images');

        alert(deviceNameInput.value);

        if (!validateDeviceName(deviceNameInput.value)) {
            alet("hola");
            msg += `Nombre del dispositivo ${index + 1} inválido.\n`;
            deviceNameInput.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceNameInput.style.borderColor = '';
        };

        if (!validateDeviceType(deviceTypeSelect.value)) {
            msg += `Debe seleccionar un tipo para el dispositivo ${index + 1}.\n`;
            deviceTypeSelect.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceTypeSelect.style.borderColor = '';
        };

        if (!validateDeviceYears(deviceYearsInput.value)) {
            msg += `Años del dispositivo ${index + 1} inválidos.\n`;
            deviceYearsInput.style.borderColor = 'red';
            isValid = false;
        };

        if (!validateDeviceCondition(deviceConditionSelect.value)) {
            msg += `Debe seleccionar una condición para el dispositivo ${index + 1}.\n`;
            deviceConditionSelect.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceConditionSelect.style.borderColor = '';
        };

        if (!validateDeviceImages(deviceImagesInput.files)) {
            msg += `Debe subir al menos una imagen para el dispositivo ${index + 1}.\n`;
            isValid = false;
        } else {
            deviceImagesInput.style.borderColor = '';
        };
    });

    if (msg === '') {
        isValid = true;
        document.getElementById('error-message').textContent = msg;
    } else {
        isValid = false;
        document.getElementById('error-message').textContent = msg;
        document.getElementById('error-message').classList.remove('hidden');
    };
};
    
// Eventos
document.addEventListener('DOMContentLoaded', () => {
    const deviceContainer = document.getElementById('device-container');
    const addDeviceButton = document.getElementById('add-device');
    const removeDeviceButton = document.getElementById('remove-device');
    const publishDonationButton = document.getElementById('publish-donation');
    const confirmationMessage = document.getElementById('confirmation-message');
    const thankYouMessage = document.getElementById('thank-you-message');
    const confirmPublishButton = document.getElementById('confirm-publish');
    const cancelPublishButton = document.getElementById('cancel-publish');

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

    publishDonationButton.addEventListener('click', () => {
        validatorDonationContact();
        validatorDonationDevices();
        if (isValid) {
            confirmationMessage.classList.remove('hidden');
        }
    });

    confirmPublishButton.addEventListener('click', () => {
        confirmationMessage.classList.add('hidden');
        thankYouMessage.classList.remove('hidden');
    });

    cancelPublishButton.addEventListener('click', () => {
        confirmationMessage.classList.add('hidden');
    });
});

