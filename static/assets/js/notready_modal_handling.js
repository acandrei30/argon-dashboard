document.addEventListener('DOMContentLoaded', function () {
    const notReadyButton = document.getElementById('btnNotReadyForConsultation');
    const notReadyModal = new bootstrap.Modal(document.getElementById('notReadyForConsultationModal'));
    const form = document.getElementById('leadForm');
    const hiddenStatusField = document.getElementById('lead_status');
    const saveNotReadyButton = document.getElementById('saveNotReadyForConsultation');
    let isSubmitting = false; // Flag to prevent multiple submissions

    // Initialize Flatpickr for manual date selection
    if (typeof flatpickr !== 'undefined') {
        flatpickr("#manualFollowUpDate", {
            dateFormat: "Y-m-d",
            minDate: "today", // Prevent selecting past dates
        });
    } else {
        console.warn('Flatpickr is not defined. Ensure the library is loaded.');
    }

    // Prevent default form submission when opening the modal
    notReadyButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent form submission
        // Update the hidden field for the status
        hiddenStatusField.value = this.dataset.status;
        // Open the Not Ready for Consultation modal
        notReadyModal.show();
    });

    // Save "Not Ready for Consultation" Data
    saveNotReadyButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default button action

        if (isSubmitting) {
            console.log('Form is already being submitted...');
            return; // Prevent further action if the form is already being submitted
        }

        const reason = document.getElementById('reason').value;
        const followUpDays = document.querySelector('input[name="follow_up_days"]:checked')?.value;
        const manualFollowUpDate = document.getElementById('manualFollowUpDate')?.value;

        // Validate that either follow-up days or manual follow-up date is provided
        if (!reason) {
            alert('Please provide a reason for not being ready.');
            return;
        }

        if (!followUpDays && !manualFollowUpDate) {
            alert('Please select either "Number of Days" or "Follow-Up Date."');
            return;
        }

        // Determine follow-up date
        let followUpDate = manualFollowUpDate;
        if (!followUpDate && followUpDays) {
            const today = new Date();
            today.setDate(today.getDate() + parseInt(followUpDays));
            followUpDate = today.toISOString().split("T")[0]; // Format as YYYY-MM-DD
        }

        // Mark the form as being submitted
        isSubmitting = true;

        // Submit the form via AJAX
        const formData = new FormData(form);
        formData.append('reason', reason);
        formData.append('follow_up_date', followUpDate);

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
                    // Redirect to the pipeline
                    window.location.href = '/sales-pipeline/pipeline';
                } else {
                    return response.json().then(data => {
                        alert('Error saving lead: ' + (data.message || 'Unknown error'));
                        isSubmitting = false; // Reset the flag on error
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                isSubmitting = false; // Reset the flag on error
            });
    });
});
