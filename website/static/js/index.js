function deleteNote(noteId) {
  console.log("Attempting to delete note with ID:", noteId);
  if (!noteId) {
    console.error('Invalid note ID');
    return;
  }
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
    headers: {
      'Content-Type': 'application/json'
    },
  }).then((res) => {
    if (res.ok) {
      return res.json();
    }
    return res.text().then(text => {
      throw new Error(`Server error: ${res.status} ${res.statusText}\n${text}`);
    });
  }).then((data) => {
    if (data.success) {
      const noteElement = document.getElementById(`note-${noteId}`);
      if (noteElement) {
        noteElement.remove();
      }
    } else {
      console.error('Failed to delete note:', data.error);
    }
  }).catch((error) => {
    console.error('Error:', error);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const noteForm = document.querySelector('form');
  const noteInput = document.getElementById('note');

  if (noteForm) {
    noteForm.addEventListener('submit', function(e) {
      if (!noteInput.value.trim()) {
        e.preventDefault();
        alert('Please enter a note before submitting.');
      }
    });
  }

  function loadNotes() {
    fetch("/get-notes")
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        const noteList = document.getElementById("notes");
        noteList.innerHTML = "";
        data.forEach((note) => {
          console.log("Rendering note with ID:", note._id);
          const li = document.createElement("li");
          li.className = "list-group-item";
          li.id = `note-${note._id}`;
          li.innerHTML = `
            <div class="row align-items-center">
              <div class="col note-content">
                ${note.data}
              </div>
              <div class="col-auto note-metadata">
                <small class="text-muted mr-2">${new Date(note.date).toLocaleString()}</small>
                <button type="button" class="close delete-note" onclick="deleteNote('${note._id}')">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
            </div>
          `;
          noteList.appendChild(li);
        });
      })
      .catch((error) => {
        console.error('Error loading notes:', error);
      });
  }

  loadNotes();
});