document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript loaded");

    const notReadyButton = document.getElementById('btnNotReadyForConsultation');
    const notReadyModal = new bootstrap.Modal(document.getElementById('notReadyForConsultationModal'));
    const form = document.getElementById('leadForm');
    const hiddenStatusField = document.getElementById('lead_status');
    const saveNotReadyButton = document.getElementById('saveNotReadyForConsultation');

    if (!notReadyButton || !notReadyModal) {
        console.error("Button or Modal not found");
        return;
    }

    // Handle Not Ready for Consultation Button Click
    notReadyButton.addEventListener('click', function () {
        console.log("Not Ready button clicked");
        hiddenStatusField.value = this.dataset.status;
        notReadyModal.show();
    });

    // Save Not Ready for Consultation Data
    saveNotReadyButton.addEventListener('click', function () {
        const reason = document.getElementById('reason').value;
        const followUp = document.querySelector('input[name="follow_up"]:checked')?.value;

        if (!reason || !followUp) {
            alert('Please fill out all fields before saving.');
            return;
        }

        const formData = new FormData(form);
        formData.append('reason', reason);
        formData.append('follow_up', followUp);

        console.log("Submitting form data:", [...formData]);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => {
                if (response.ok) {
                    console.log('Lead saved successfully!');
                    notReadyModal.hide();
                    window.location.reload(); // Optionally reload or redirect
                } else {
                    return response.json().then(data => {
                        console.error('Error saving lead:', data.message || 'Unknown error');
                        alert('Error saving lead: ' + (data.message || 'Unknown error'));
                    });
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
