document.addEventListener('DOMContentLoaded', function () {
    const readyButton = document.getElementById('btnReadyForConsultation');
    const form = document.getElementById('leadForm');
    const hiddenStatusField = document.getElementById('lead_status');

    // Service Type and End Date Fields
    const serviceType = document.getElementById("service-type");
    const endDateGroup = document.getElementById("end-date-group");
    const endDateInput = document.getElementById("end-date");

    // Ensure the button cannot be clicked multiple times during a single submission
    let isSubmitting = false;

    // Function to update the visibility and behavior of the End Date field
    function updateEndDateVisibility() {
        if (serviceType && serviceType.value === "short-term") {
            endDateGroup.style.display = "block"; // Show the End Date field
            endDateInput.required = true;        // Make it required
            endDateInput.disabled = false;       // Enable the field for input
        } else {
            endDateGroup.style.display = "none"; // Hide the End Date field
            endDateInput.required = false;       // Remove the required attribute
            endDateInput.disabled = true;        // Disable the field
            endDateInput.value = "";             // Clear the value
        }
    }

    // Initial visibility check when the page loads
    if (serviceType) {
        updateEndDateVisibility();

        // Event listener for changes to the Service Type dropdown
        serviceType.addEventListener("change", updateEndDateVisibility);
    }

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

        // Ensure the end_date field is excluded if "Undetermined" is selected
        if (serviceType && serviceType.value === "undetermined") {
            formData.delete("end_date"); // Exclude end_date from the submission
        }

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
