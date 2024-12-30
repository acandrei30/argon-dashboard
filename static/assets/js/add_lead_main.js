document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const btnStillProspecting = document.getElementById('btnStillProspecting');
    const btnReadyForConsultation = document.getElementById('btnReadyForConsultation');
    const statusInput = document.getElementById('lead_status'); // Hidden input for status

    // Function to validate the form
    function validateForm() {
        const isFormValid = form.checkValidity();
        btnStillProspecting.disabled = !isFormValid;
        btnReadyForConsultation.disabled = !isFormValid;
    }

    // Attach validation logic
    form.addEventListener('input', validateForm);
    form.addEventListener('change', validateForm);

    // Handle "Still Prospecting" button click
    btnStillProspecting.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default behavior

        if (!form.checkValidity()) {
            form.reportValidity(); // Show validation errors
            return;
        }

        // Set the status for "Still Prospecting"
        statusInput.value = btnStillProspecting.getAttribute('data-status');

        // Submit the form via AJAX
        const formData = new FormData(form);

        fetch('/sales-pipeline/add_lead/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const event = new CustomEvent('leadCreated', { detail: data.lead_id });
                    document.dispatchEvent(event); // Dispatch leadCreated event
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error during lead creation:', error);
                alert('An unexpected error occurred.');
            });
    });

    // Handle "Ready for Consultation" button click
    btnReadyForConsultation.addEventListener('click', function () {
        if (!form.checkValidity()) {
            form.reportValidity(); // Show validation errors
            return;
        }

        // Set the status for "Ready for Consultation"
        statusInput.value = btnReadyForConsultation.getAttribute('data-status');
        form.submit(); // Submit the form normally
    });

    // Perform initial validation
    validateForm();
});
