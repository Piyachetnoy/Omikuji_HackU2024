document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', () => {
        const filename = button.getAttribute('data-filename');
        if (confirm(`Are you sure you want to delete ${filename}?`)) {
            fetch('/delete_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filename }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Image deleted successfully');
                    location.reload();
                } else {
                    alert(`Error: ${data.error}`);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the image.');
            });
        }
    });
});