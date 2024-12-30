document.addEventListener('DOMContentLoaded', function () {
    const stillProspectingModal = new bootstrap.Modal(document.getElementById('stillProspectingModal'));
    const saveStillProspectingButton = document.getElementById('saveStillProspecting');

    // Open modal after lead creation
    document.addEventListener('leadCreated', function (event) {
        const leadId = event.detail.leadId; // Get the lead ID
        stillProspectingModal.show(); // Show modal for additional details

        // Save additional details on modal "Save" click
        saveStillProspectingButton.addEventListener('click', function () {
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
                        stillProspectingModal.hide();
                        alert(data.message);
                        location.reload(); // Optionally reload the page
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error saving still prospecting:', error);
                    alert('An unexpected error occurred.');
                });
        });
    });
});
