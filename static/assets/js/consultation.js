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

    // Initialize Flatpickr for time selection
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

    // Save Consultation
    $("#save-consultation").click(function () {
        const consultationDate = $("#selected-date").val();
        const consultationTime = $("#selected-time").val();
        const consultationDatetime = consultationDate + " " + consultationTime;

        $.ajax({
            url: '{% url "update-lead-consultation" lead.id %}',
            method: "POST",
            data: {
                consultation_datetime: consultationDatetime,
                csrfmiddlewaretoken: "{{ csrf_token }}",
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

    // Edit Consultation
    $(document).on("click", "#edit-consultation", function () {
        const currentDatetime = $("#consultation-datetime").text().trim();
        const editHtml = `
            <input id="edit-date" class="form-control mb-2" type="date" value="${currentDatetime.split(' ')[0]}">
            <input id="edit-time" class="form-control mb-2" type="time" value="${currentDatetime.split(' ')[1]}">
            <button id="save-edited-consultation" class="btn btn-sm btn-success">Save</button>
        `;
        $("#consultation-datetime").html(editHtml);
    });

    // Save Edited Consultation
    $(document).on("click", "#save-edited-consultation", function () {
        const newDate = $("#edit-date").val();
        const newTime = $("#edit-time").val();
        const newDatetime = `${newDate} ${newTime}`;

        $.ajax({
            url: '{% url "update-lead-consultation" lead.id %}',
            method: "POST",
            data: {
                consultation_datetime: newDatetime,
                csrfmiddlewaretoken: "{{ csrf_token }}",
            },
            success: function () {
                Swal.fire({
                    title: "Updated!",
                    text: "The consultation date and time have been updated.",
                    icon: "success",
                    confirmButtonText: "Ok",
                }).then(() => location.reload());
            },
            error: function () {
                Swal.fire({
                    title: "Error",
                    text: "There was an error updating the consultation.",
                    icon: "error",
                    confirmButtonText: "Ok",
                });
            },
        });
    });
});
