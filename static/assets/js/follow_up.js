$(document).ready(function () {
    const followUpCheckbox = $("#followUpTask");
    const followUpActionModal = new bootstrap.Modal(document.getElementById('followUpActionModal'));
    const saveFollowUpAction = $("#saveFollowUpAction");

    // Handle Follow-Up Task Checkbox
    followUpCheckbox.change(function () {
        if (this.checked) {
            followUpActionModal.show();
        }
    });

    // Save Follow-Up Action
    saveFollowUpAction.click(function () {
        const note = $("#followUpNote").val().trim();

        if (!note) {
            alert("Please provide a follow-up note.");
            return;
        }

        // Send data to the backend
        fetch("{% url 'update-lead-follow-up' lead.id %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: JSON.stringify({ note: note }),
        })
            .then((response) => {
                if (response.ok) {
                    alert("Follow-up action saved successfully!");

                    // Disable the checkbox and hide the modal
                    followUpCheckbox.prop("checked", true).prop("disabled", true);
                    followUpActionModal.hide();
                } else {
                    alert("An error occurred while saving the follow-up action.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("A network error occurred. Please try again.");
            });
    });

    // Disable the follow-up checkbox if already marked as done
    if (followUpCheckbox.data("done") === "true") {
        followUpCheckbox.prop("checked", true).prop("disabled", true);
    }
});
