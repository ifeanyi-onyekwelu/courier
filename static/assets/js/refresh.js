// refresh.js
function refreshPage() {
    location.reload();
}

function checkForUpdates() {
    // Make an AJAX request to the server to check for updates
    // You can use jQuery or other libraries to simplify the AJAX request

    // Example using jQuery:
    $.ajax({
        url: '/check_updates/',  // Replace with the actual URL for checking updates
        method: 'GET',
        success: function (response) {
            if (response.has_updates) {
                refreshPage();  // Refresh the page if there are updates
            }
        },
        error: function (xhr, status, error) {
            console.log('Error checking for updates:', error);
        }
    });
}

// Call the checkForUpdates function every 3 seconds
setInterval(checkForUpdates, 3000);
