function deleteNote(noteID) {
    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ noteID: noteID }),
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.result === 'success') {
            location.reload();
        } else {
            alert('Failed to delete note: ' + data.error);
        }
    })
    .catch(error => {
        alert('An error occurred while deleting the note');
    });
}
