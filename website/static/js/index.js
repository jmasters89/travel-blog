function deleteNote(noteId) {
  console.log("Attempting to delete note with ID:", noteId);
  if (!noteId) {
    console.error('Invalid note ID');
    return;
  }

  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId }),
    headers: { 'Content-Type': 'application/json' },
  })
    .then((res) => {
      if (res.ok) return res.json();
      return res.text().then(text => {
        throw new Error(`Server error: ${res.status} ${res.statusText}\n${text}`);
      });
    })
    .then((data) => {
      if (data.success) {
        const noteElement = document.getElementById(`note-${noteId}`);
        if (noteElement) noteElement.remove();
      } else {
        console.error('Failed to delete note:', data.error);
      }
    })
    .catch((error) => console.error('Error:', error));
}

function createNote(content) {
  fetch("/create-note", {
    method: "POST",
    body: JSON.stringify({ content }),
    headers: { 'Content-Type': 'application/json' },
  })
  .then((res) => {
    if (res.ok) return res.json();
    return res.text().then(text => {
      throw new Error(`Server error: ${res.status} ${res.statusText}\n${text}`);
    });
  })
  .then((data) => {
    if (data.success) {
      const noteList = document.getElementById("notes");
      const li = document.createElement("li");
      li.className = "list-group-item";
      li.id = `note-${data.note.id}`;
      li.innerHTML = `
        <div class="row align-items-center">
          <div class="col note-content">${data.note.data}</div>
          <div class="col-auto note-metadata">
            <small class="text-muted mr-2">${new Date(data.note.date).toLocaleString()}</small>
            <button type="button" class="btn btn-danger btn-sm delete-btn" onclick="deleteNote('${data.note.id}')" title="Delete">
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
        </div>
      `;
      noteList.appendChild(li);
    } else {
      console.error('Failed to create note:', data.error);
    }
  })
  .catch((error) => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
  const noteForm = document.getElementById('add-note-form');
  const noteInput = document.getElementById('new-note');

  if (noteForm && noteInput) {
    noteForm.addEventListener('submit', function(e) {
      e.preventDefault(); // Prevent the default form submission
      const noteContent = noteInput.value.trim();
      if (noteContent) {
        createNote(noteContent);
        noteInput.value = ''; // Clear the input field
      } else {
        alert('Please enter a note before submitting.');
      }
    });
  }

  function loadNotes() {
    const noteList = document.getElementById("notes");
    if (!noteList) {
      console.error("Element with ID 'notes' not found");
      return;
    }

    fetch("/get-notes")
      .then((response) => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then((data) => {
        noteList.innerHTML = "";
        data.forEach((note) => {
          console.log("Rendering note with ID:", note.id);
          const li = document.createElement("li");
          li.className = "list-group-item";
          li.id = `note-${note.id}`;
          li.innerHTML = `
            <div class="row align-items-center">
              <div class="col note-content">${note.data}</div>
              <div class="col-auto note-metadata">
                <small class="text-muted mr-2">${new Date(note.date).toLocaleString()}</small>
                <small class="text-muted">by ${note.author}</small>
                <button type="button" class="btn btn-danger btn-sm delete-btn" onclick="deleteNote('${note.id}')" title="Delete">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </div>
          `;
          noteList.appendChild(li);
        });
      })
      .catch((error) => console.error('Error loading notes:', error));
  }

  // Call loadNotes after a short delay to ensure DOM is ready
  setTimeout(loadNotes, 100);
});