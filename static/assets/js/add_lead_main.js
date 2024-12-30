document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("leadForm");
    const btnNotReadyForConsultation = document.getElementById("btnNotReadyForConsultation");
    const stillProspectingModal = new bootstrap.Modal(document.getElementById("stillProspectingModal"));
    const saveStillProspectingButton = document.getElementById("saveStillProspecting");

    // Handle "Not Ready for Consultation" button click
    btnNotReadyForConsultation.addEventListener("click", function (event) {
        event.preventDefault();

        // Validate the form first
        if (!form.checkValidity()) {
            form.reportValidity(); // Show browser validation messages
            return;
        }

        // Show the modal if validation is successful
        stillProspectingModal.show();
    });

    // Handle modal "Save" button click
    saveStillProspectingButton.addEventListener("click", function (event) {
        const reason = document.getElementById("reason").value.trim();
        const followUpSelected = document.querySelector('input[name="follow_up"]:checked');

        if (!reason) {
            alert("Please provide a reason for still prospecting.");
            return;
        }

        if (!followUpSelected) {
            alert("Please select a follow-up option.");
            return;
        }

        // Add the modal data to the form and submit
        const hiddenReasonInput = document.createElement("input");
        hiddenReasonInput.type = "hidden";
        hiddenReasonInput.name = "reason";
        hiddenReasonInput.value = reason;
        form.appendChild(hiddenReasonInput);

        const hiddenFollowUpInput = document.createElement("input");
        hiddenFollowUpInput.type = "hidden";
        hiddenFollowUpInput.name = "follow_up";
        hiddenFollowUpInput.value = followUpSelected.value;
        form.appendChild(hiddenFollowUpInput);

        const hiddenStatusInput = document.createElement("input");
        hiddenStatusInput.type = "hidden";
        hiddenStatusInput.name = "status";
        hiddenStatusInput.value = btnNotReadyForConsultation.getAttribute("data-status");
        form.appendChild(hiddenStatusInput);

        // Submit the form
        form.submit();
    });
});
