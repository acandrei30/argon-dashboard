$(document).ready(function () {
  // Initialize variables
  const followUpCheckbox = $("#followUpTask");
  const followUpModal = new bootstrap.Modal(document.getElementById("followUpModal"));
  const saveFollowUpButton = $("#saveFollowUp");

  // Open modal when checkbox is clicked
  followUpCheckbox.change(function () {
      if (this.checked) {
          followUpModal.show();
      }
  });

  // Save follow-up note
  saveFollowUpButton.click(function () {
      const note = $("#followUpNote").val().trim(); // Get the note input value
      const url = followUpCheckbox.data("url"); // URL for the AJAX request
      const csrfToken = followUpCheckbox.data("csrf"); // CSRF token

      // Validate the note
      if (!note) {
          Swal.fire({
              title: "Error",
              text: "Please enter a note before saving.",
              icon: "error",
              confirmButtonText: "Ok",
          });
          return;
      }

      // Perform AJAX request to save the note
      $.ajax({
          url: url,
          method: "POST",
          data: {
              action: "add_note",
              note: note,
              csrfmiddlewaretoken: csrfToken,
          },
          success: function (response) {
              Swal.fire({
                  title: "Success!",
                  text: "The follow-up note has been added.",
                  icon: "success",
                  confirmButtonText: "Ok",
              }).then(() => {
                  location.reload(); // Reload the page to reflect the updates
              });
          },
          error: function (xhr, status, error) {
              let errorMessage = "There was an error updating the follow-up task.";
              if (xhr.responseJSON && xhr.responseJSON.error) {
                  errorMessage = xhr.responseJSON.error;
              }

              Swal.fire({
                  title: "Error",
                  text: errorMessage,
                  icon: "error",
                  confirmButtonText: "Ok",
              });
          },
      });
  });
});
