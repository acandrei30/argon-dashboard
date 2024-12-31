$(document).ready(function () {
    // Initialize Flatpickr for date selection
    flatpickr("#selected-date", {
        dateFormat: "Y-m-d",
        onChange: function (selectedDates, dateStr) {
            $("#selected-time").prop("disabled", false);
            $("#selected-date-text").text("You have selected: " + dateStr);
            updateSaveButtonState();
        },
    });

    flatpickr("#selected-time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        onChange: updateSaveButtonState,
    });

    function updateSaveButtonState() {
        const dateSelected = $("#selected-date").val();
        const timeSelected = $("#selected-time").val();
        $("#save-consultation").prop("disabled", !dateSelected || !timeSelected);
    }

    $("#save-consultation").click(function () {
        const consultationDate = $("#selected-date").val();
        const consultationTime = $("#selected-time").val();
        const consultationDatetime = consultationDate + " " + consultationTime;

        $.ajax({
            url: updateConsultationUrl, // Use the global variable
            method: "POST",
            data: {
                consultation_datetime: consultationDatetime,
                csrfmiddlewaretoken: csrfToken, // Use the global variable
            },
            success: function () {
                Swal.fire({
                    title: "Consultation Scheduled!",
                    text: "The consultation has been scheduled.",
                    icon: "success",
                    confirmButtonText: "Ok",
                }).then(() => location.reload());
            },
            error: function () {
                Swal.fire({
                    title: "Error",
                    text: "There was an error scheduling the consultation.",
                    icon: "error",
                    confirmButtonText: "Ok",
                });
            },
        });
    });
});
