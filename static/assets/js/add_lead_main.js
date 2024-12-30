document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("leadForm");
    const readyButton = document.getElementById("btnReadyForConsultation");
    const notReadyButton = document.getElementById("btnNotReadyForConsultation");
    const notReadyModal = new bootstrap.Modal(document.getElementById("notReadyForConsultationModal"));
    const saveNotReadyButton = document.getElementById("saveNotReadyForConsultation");
    const hiddenStatusField = document.getElementById("lead_status");

    // Initialize Flatpickr for manual date selection
    if (typeof flatpickr !== 'undefined') {
        flatpickr("#manualFollowUpDate", {
            dateFormat: "Y-m-d",
            minDate: "today", // Prevent selecting past dates
        });
    } else {
        console.warn('Flatpickr is not defined. Ensure the library is loaded.');
    }

    // Function to check if required fields are filled
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

    // Handle "Ready for Consultation" button click
    readyButton.addEventListener("click", function () {
        hiddenStatusField.value = "ready_for_consultation"; // Set status
        if (!areFormFieldsComplete(form)) {
            alert("Please fill out all required fields.");
            return;
        }
        form.submit(); // Submit the form directly
    });

    // Handle "Not Ready for Consultation" button click
    notReadyButton.addEventListener("click", function () {
        hiddenStatusField.value = "not_ready_for_consultation"; // Set status
        if (!areFormFieldsComplete(form)) {
            alert("Please fill out all required fields.");
            return;
        }
        notReadyModal.show(); // Open the modal
    });

    // Handle "Save" button in modal
    saveNotReadyButton.addEventListener("click", function () {
        const reason = document.getElementById("reason").value.trim();
        const followUpDays = document.querySelector('input[name="follow_up"]:checked')?.value;
        const manualFollowUpDate = document.getElementById("manualFollowUpDate")?.value;

        // Validate modal fields
        if (!reason) {
            alert("Please provide a reason for not being ready.");
            return;
        }

        if (!followUpDays && !manualFollowUpDate) {
            alert("Please select either a number of days or a manual follow-up date.");
            return;
        }

        // Determine follow-up date
        let followUpDate = manualFollowUpDate;
        if (!followUpDate && followUpDays) {
            const today = new Date();
            today.setDate(today.getDate() + parseInt(followUpDays));
            followUpDate = today.toISOString().split("T")[0]; // Format as YYYY-MM-DD
        }

        // Add follow-up data to the form
        const followUpInput = document.createElement("input");
        followUpInput.type = "hidden";
        followUpInput.name = "follow_up_date";
        followUpInput.value = followUpDate;
        form.appendChild(followUpInput);

        const reasonInput = document.createElement("input");
        reasonInput.type = "hidden";
        reasonInput.name = "reason";
        reasonInput.value = reason;
        form.appendChild(reasonInput);

        // Submit the form
        form.submit();
    });
});
