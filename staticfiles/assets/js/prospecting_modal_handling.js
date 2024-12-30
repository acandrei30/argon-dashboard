document.addEventListener('DOMContentLoaded', function () {
    const btnStillProspecting = document.getElementById('btnStillProspecting');
    const stillProspectingModal = new bootstrap.Modal(document.getElementById('stillProspectingModal'));
    const saveStillProspectingButton = document.getElementById('saveStillProspecting');

    let leadId = null; // Will store the lead ID after creation

    // Handle "Still Prospecting" button click
    btnStillProspecting.addEventListener('click', function (event) {
        event.preventDefault();

        if (leadId) {
            stillProspectingModal.show(); // Open the modal if lead ID exists
        } else {
            alert('Lead ID is missing. Please ensure the lead is properly created before continuing.');
            console.error('Lead ID is missing.');
        }
    });

    // Handle "Save" button in the modal
    saveStillProspectingButton.addEventListener('click', function (event) {
        event.preventDefault();

        const reason = document.getElementById('reason').value.trim();
        const followUpSelected = document.querySelector('input[name="follow_up"]:checked');

        if (!reason) {
            alert('Please provide a reason for still prospecting.');
            return;
        }

        if (!followUpSelected) {
            alert('Please select a follow-up option.');
            return;
        }

        if (!leadId) {
            alert('Lead ID is missing. Please ensure the lead is properly created.');
            console.error('Lead ID is missing.');
            return;
        }

        const data = {
            lead_id: leadId,
            reason: reason,
            follow_up: followUpSelected.value,
        };

        fetch('/sales-pipeline/save-still-prospecting/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    stillProspectingModal.hide(); // Close the modal
                    alert(data.message); // Show success message
                    location.reload(); // Optionally reload the page
                } else {
                    alert('Error: ' + data.message);
                    console.error('Error saving still prospecting:', data.message);
                }
            })
            .catch(error => {
                console.error('Error during still prospecting save:', error);
                alert('An unexpected error occurred.');
            });
    });

    // This function should be called from the main script to set the lead ID
    window.setLeadId = function (id) {
        leadId = id;
        btnStillProspecting.setAttribute('data-lead-id', id);
    };
});
