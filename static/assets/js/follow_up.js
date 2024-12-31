$(document).ready(function () {
    const followUpCheckbox = $("#followUpTask");
    const followUpActionModal = new bootstrap.Modal(document.getElementById("followUpActionModal"));
    const saveFollowUpAction = $("#saveFollowUpAction");

    followUpCheckbox.change(function () {
        if (this.checked) {
            followUpActionModal.show();
        }
    });

    saveFollowUpAction.click(function () {
        const note = $("#followUpNote").val().trim();
        const followUpDate = $("#followUpDate").val().trim();

        if (!note || !followUpDate) {
            alert("Please provide both a follow-up date and note.");
            return;
        }

        fetch(updateFollowUpUrl, { // Use the global variable
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken, // Use the global variable
            },
            body: JSON.stringify({ note: note, follow_up_date: followUpDate }),
        })
            .then((response) => {
                if (response.ok) {
                    Swal.fire({
                        title: "Follow-Up Saved!",
                        text: "Your follow-up has been saved.",
                        icon: "success",
                        confirmButtonText: "Ok",
                    }).then(() => location.reload());
                } else {
                    Swal.fire({
                        title: "Error",
                        text: "Failed to save follow-up.",
                        icon: "error",
                        confirmButtonText: "Ok",
                    });
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                Swal.fire({
                    title: "Network Error",
                    text: "Failed to connect to the server.",
                    icon: "error",
                    confirmButtonText: "Ok",
                });
            });
    });
});
