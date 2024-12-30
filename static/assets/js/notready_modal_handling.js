document.addEventListener('DOMContentLoaded', function () {
    const notReadyButton = document.getElementById('btnNotReadyForConsultation');
    const notReadyModal = new bootstrap.Modal(document.getElementById('notReadyForConsultationModal'));
    const form = document.getElementById('leadForm');
    const hiddenStatusField = document.getElementById('lead_status');
    const saveNotReadyButton = document.getElementById('saveNotReadyForConsultation');

    // Initialize Flatpickr for manual date selection
    if (typeof flatpickr !== 'undefined') {
        flatpickr("#manualFollowUpDate", {
            dateFormat: "Y-m-d",
            minDate: "today", // Prevent selecting past dates
        });
    } else {
        console.warn('Flatpickr is not defined. Ensure the library is loaded.');
    }

    // Function to check if all form fields are filled
    function areFormFieldsComplete(form) {
        const requiredFields = form.querySelectorAll('[required]');
        for (const field of requiredFields) {
            if (!field.value.trim()) {
                field.focus(); // Focus on the first incomplete field
                return false;
            }
        }
        return true;
    }

    // Handle Not Ready for Consultation Button Click
    notReadyButton.addEventListener('click', function () {
        // Check if all form fields are completed
        if (!areFormFieldsComplete(form)) {
            alert('Please fill out all required fields in the form before proceeding.');
            return;
        }

        // Update the hidden field for the status
        hiddenStatusField.value = this.dataset.status;

        // Open the Not Ready for Consultation modal
        notReadyModal.show();
    });

    // Save Not Ready for Consultation Data
    saveNotReadyButton.addEventListener('click', function () {
        const reason = document.getElementById('reason').value;
        const followUpDays = document.querySelector('input[name="follow_up"]:checked')?.value;
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
                    });
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
