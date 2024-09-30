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
        if (phone !== '') {
            return String(phone).match(/^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/);
        }
        return true;
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
    const validateDeviceYears = (years) => years && years >= 1 && years < 99;
    const validateDeviceCondition = (condition) => condition && condition !== '';
    const validateDeviceImages = (images) => images && images.length >= 1 && images.length <= 3;
    
    let deviceInfos = document.querySelectorAll('.device-info');
    let isValid = true;
    let msgDevices = '';

    deviceInfos.forEach((deviceInfo, index) => {
        let deviceNameInput = deviceInfo.querySelector('[id^="device-name"]');
        let deviceTypeSelect = deviceInfo.querySelector('[id^="device-type"]');
        let deviceYearsInput = deviceInfo.querySelector('[id^="device-years"]');
        let deviceConditionSelect = deviceInfo.querySelector('[id^="device-condition"]');
        let deviceImagesInput = deviceInfo.querySelector('[id^="device-photos"]');
    
        if (!deviceNameInput || !deviceTypeSelect || !deviceYearsInput || !deviceConditionSelect || !deviceImagesInput) {
            console.error(`Error: No se pudo encontrar uno o más campos en el dispositivo ${index + 1}.`);
            return;
        }
    
        if (!validateDeviceName(deviceNameInput.value)) {
            msgDevices += `Nombre del dispositivo ${index + 1} inválido.\n`;
            deviceNameInput.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceNameInput.style.borderColor = '';
        }
    
        if (!validateDeviceType(deviceTypeSelect.value)) {
            msgDevices += `Debe seleccionar un tipo para el dispositivo ${index + 1}.\n`;
            deviceTypeSelect.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceTypeSelect.style.borderColor = '';
        }
    
        if (!validateDeviceYears(deviceYearsInput.value)) {
            msgDevices += `Años del dispositivo ${index + 1} inválidos.\n`;
            deviceYearsInput.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceYearsInput.style.borderColor = '';
        }
    
        if (!validateDeviceCondition(deviceConditionSelect.value)) {
            msgDevices += `Debe seleccionar una condición para el dispositivo ${index + 1}.\n`;
            deviceConditionSelect.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceConditionSelect.style.borderColor = '';
        }
    
        if (!validateDeviceImages(deviceImagesInput.files)) {
            msgDevices += `Debe subir entre 1 y 3 imagenes en el dispositivo ${index + 1}.\n`;
            deviceImagesInput.style.borderColor = 'red';
            isValid = false;
        } else {
            deviceImagesInput.style.borderColor = '';
        }
    });

    // Mostrar errores si existen
    if (msgDevices !== '') {
        document.getElementById('error-message-device').textContent = msgDevices;
        document.getElementById('error-message-device').classList.remove('hidden');
    } else {
        document.getElementById('error-message-device').classList.add('hidden');
    }
    console.log(msgDevices);
    return isValid;
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
    const errorMessages = document.getElementById('.error-message');

    // Agregar evento para clonar y modificar IDs
addDeviceButton.addEventListener('click', (e) => {
    e.preventDefault();

    // Clonar el conjunto de campos para un nuevo dispositivo
    const newDevice = document.querySelector('.device-info').cloneNode(true);
    
    // Limpiar los campos del nuevo dispositivo
    newDevice.querySelectorAll('input, textarea').forEach(input => {
        input.value = '';
        input.removeAttribute('id');
    });

    // Asignar nuevos IDs y nombres únicos a los campos del dispositivo clonado
    let deviceIndex = document.querySelectorAll('.device-info').length;
    newDevice.querySelectorAll('input, textarea, select').forEach((input, i) => {
        let newId = input.getAttribute('name').replace('[]', '') + deviceIndex;
        input.setAttribute('id', newId);
        input.setAttribute('name', input.getAttribute('name').replace('[]', `[${deviceIndex}]`));
    });

    deviceContainer.appendChild(newDevice);
});

    removeDeviceButton.addEventListener('click', (e) => {
        e.preventDefault();

        // Eliminar el último conjunto de campos para el dispositivo
        const deviceInfos = deviceContainer.querySelectorAll('.device-info');
        if (deviceInfos.length > 1) {
            deviceContainer.removeChild(deviceInfos[deviceInfos.length - 1]);
        }
    });

    publishDonationButton.addEventListener('click', () => {
        let isValid = true;
        isValid = validatorDonationContact();
        isValid = validatorDonationDevices();
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

