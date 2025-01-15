document.addEventListener('DOMContentLoaded', function () {
    const readyButton = document.getElementById('btnReadyForConsultation');
    const form = document.getElementById('leadForm');
    const hiddenStatusField = document.getElementById('lead_status');

    // Ensure the button cannot be clicked multiple times during a single submission
    let isSubmitting = false;

    readyButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Prevent duplicate submissions
        if (isSubmitting) {
            return;
        }
        isSubmitting = true; // Set flag to prevent further submissions

        // Update the hidden field for the status
        hiddenStatusField.value = this.dataset.status;

        // Submit the form via AJAX
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json(); // Parse JSON response
            })
            .then(data => {
                if (data.lead_id) {
                    // Redirect to consultation options page
                    window.location.href = `/sales-pipeline/consultation-options/${data.lead_id}/`;
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                alert("An unexpected error occurred. Please try again.");
            })
            .finally(() => {
                isSubmitting = false; // Reset flag after completion
            });
    });
});
