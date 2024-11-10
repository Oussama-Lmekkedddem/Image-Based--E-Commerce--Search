function handleFileSelect() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const imageData = e.target.result;
            sendToFlask(imageData);
        };

        reader.readAsDataURL(file);
    }
}

function sendToFlask(imageData) {
    // Use Fetch to send the image data to Flask
    fetch('/process_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageData }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from Flask:', data);
        // After receiving the response, you can redirect to the new URL
        window.location.href = data.redirect_url;
    })
    .catch(error => {
        console.error('Error sending image data to Flask:', error);
    });
}
