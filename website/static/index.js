function deleteNote(noteID) {
    console.log('Attempting to delete note with ID:', noteID);
    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ noteID: noteID }),
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.result === 'success') {
            console.log('Note deleted successfully');
            location.reload();
        } else {
            console.error('Failed to delete note:', data.error);
            alert('Failed to delete note: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the note');
    });
}
