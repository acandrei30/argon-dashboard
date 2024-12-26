let draggedCaregiverId = null;

// Handle drag start
function handleDragStart(event, caregiverId) {
    console.log(`Drag started for caregiver: ${caregiverId}`);
    draggedCaregiverId = caregiverId;
    event.dataTransfer.setData("text/plain", caregiverId);
}

// Allow drop
function allowDrop(event) {
    console.log("Allowing drop...");
    event.preventDefault();
}

// Handle drop
function handleDrop(event, newStage) {
    event.preventDefault();

    const caregiverId = event.dataTransfer.getData("text/plain");
    console.log(`Dropped caregiver ${caregiverId} into stage ${newStage}`);

    // Send the update to the backend
    fetch(`/recruitment/update/${caregiverId}/${newStage}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // Add CSRF token for security
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.ok) {
                console.log(`Successfully moved caregiver ${caregiverId} to ${newStage}`);
                // Move the caregiver card visually
                const draggedElement = document.getElementById(`caregiver-${caregiverId}`);
                const newStageElement = document.getElementById(`stage-${newStage}`);
                newStageElement.appendChild(draggedElement);
            } else {
                console.error("Failed to update caregiver stage", response);
                alert("Failed to update caregiver stage.");
            }
        })
        .catch((error) => console.error("Error:", error));
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
